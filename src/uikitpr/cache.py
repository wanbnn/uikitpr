"""Entrega e invalidação de assets web do UIKitPR."""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import re
from dataclasses import asdict, dataclass
from importlib.resources import files
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from pyreact import h

from .core import component_props


@dataclass(frozen=True)
class CachePolicy:
    """Política usada pelo Service Worker gerado."""

    name: str = "uikitpr"
    version: str = "1"
    strategy: str = "stale-while-revalidate"
    navigation_strategy: str = "network-first"
    offline_fallback: str | None = None
    cache_navigations: bool = True
    runtime_cache_paths: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        strategies = {"cache-first", "network-first", "stale-while-revalidate"}
        if self.strategy not in strategies:
            raise ValueError(f"Estratégia de cache inválida: {self.strategy}")
        if self.navigation_strategy not in strategies:
            raise ValueError(
                f"Estratégia de navegação inválida: {self.navigation_strategy}"
            )
        for value in self.runtime_cache_paths:
            if not isinstance(value, str) or not value.startswith("/") or "://" in value:
                raise ValueError(
                    "runtime_cache_paths deve conter apenas prefixos de caminho same-origin iniciados por '/'."
                )


@dataclass(frozen=True)
class CachedAsset:
    """Entrada imutável de um manifesto de assets."""

    source: str
    path: str
    digest: str
    integrity: str
    size: int
    content_type: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CacheManager:
    """Cria assets com fingerprint, manifesto e Service Worker versionado.

    O nome final depende do conteúdo. Uma alteração de CSS ou JavaScript gera
    uma URL nova, eliminando colisões com caches do navegador e de CDNs.
    """

    def __init__(
        self,
        output: str | Path,
        *,
        policy: CachePolicy = CachePolicy(),
        assets_dir: str = "assets",
        hash_length: int = 12,
    ) -> None:
        if not 8 <= hash_length <= 64:
            raise ValueError("hash_length deve estar entre 8 e 64")
        self.output = Path(output).resolve()
        self.policy = policy
        self.assets_dir = self._safe_relative(assets_dir).as_posix().rstrip("/")
        self.hash_length = hash_length
        self._assets: dict[str, CachedAsset] = {}

    @staticmethod
    def _safe_relative(value: str) -> PurePosixPath:
        path = PurePosixPath(value.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError(f"Caminho de asset inválido: {value}")
        return path

    @property
    def assets(self) -> dict[str, CachedAsset]:
        return dict(self._assets)

    @property
    def cache_id(self) -> str:
        safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", self.policy.name).strip("-")
        safe_version = re.sub(
            r"[^a-zA-Z0-9_.-]+", "-", self.policy.version
        ).strip("-")
        return f"{safe_name or 'uikitpr'}-{safe_version or '1'}"

    def add_bytes(
        self,
        name: str,
        content: bytes,
        *,
        content_type: str | None = None,
    ) -> CachedAsset:
        logical = self._safe_relative(name)
        digest_bytes = hashlib.sha256(content).digest()
        digest = digest_bytes.hex()
        suffix = logical.suffix
        stem = logical.name[: -len(suffix)] if suffix else logical.name
        fingerprinted = logical.with_name(
            f"{stem}.{digest[:self.hash_length]}{suffix}"
        )
        public_path = PurePosixPath(self.assets_dir) / fingerprinted
        destination = self.output.joinpath(*public_path.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        mime = content_type or mimetypes.guess_type(logical.name)[0]
        asset = CachedAsset(
            source=logical.as_posix(),
            path=public_path.as_posix(),
            digest=digest,
            integrity="sha256-"
            + base64.b64encode(digest_bytes).decode("ascii"),
            size=len(content),
            content_type=mime or "application/octet-stream",
        )
        self._assets[logical.as_posix()] = asset
        return asset

    def add_text(
        self,
        name: str,
        content: str,
        *,
        content_type: str | None = None,
    ) -> CachedAsset:
        return self.add_bytes(
            name,
            content.encode("utf-8"),
            content_type=content_type,
        )

    def add_file(
        self,
        name: str,
        source: str | Path,
        *,
        content_type: str | None = None,
    ) -> CachedAsset:
        return self.add_bytes(
            name,
            Path(source).read_bytes(),
            content_type=content_type,
        )

    def asset_url(self, name: str, *, prefix: str = "") -> str:
        logical = self._safe_relative(name).as_posix()
        try:
            path = self._assets[logical].path
        except KeyError as error:
            raise KeyError(f"Asset ainda não registrado: {logical}") from error
        return f"{prefix.rstrip('/')}/{path}" if prefix else path

    def manifest(self) -> dict[str, Any]:
        return {
            "schema": 1,
            "cache": {
                "id": self.cache_id,
                "name": self.policy.name,
                "version": self.policy.version,
                "strategy": self.policy.strategy,
                "navigationStrategy": self.policy.navigation_strategy,
                "cacheNavigations": self.policy.cache_navigations,
                "runtimeCachePaths": list(self.policy.runtime_cache_paths),
            },
            "assets": {
                name: asset.to_dict()
                for name, asset in sorted(self._assets.items())
            },
        }

    def write_manifest(self, name: str = "asset-manifest.json") -> Path:
        relative = self._safe_relative(name)
        destination = self.output.joinpath(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.manifest(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return destination

    def service_worker_script(
        self,
        *,
        precache: Iterable[str] = (),
    ) -> str:
        urls = ["./" + asset.path for asset in self._assets.values()]
        urls.extend(str(item) for item in precache)
        if self.policy.offline_fallback:
            urls.append(self.policy.offline_fallback)
        unique_urls = list(dict.fromkeys(urls))
        configuration = {
            "cacheName": self.cache_id,
            "cachePrefix": re.sub(
                r"[^a-zA-Z0-9_-]+", "-", self.policy.name
            ).strip("-")
            or "uikitpr",
            "assets": unique_urls,
            "strategy": self.policy.strategy,
            "navigationStrategy": self.policy.navigation_strategy,
            "offlineFallback": self.policy.offline_fallback,
            "cacheNavigations": self.policy.cache_navigations,
            "runtimeCachePaths": list(self.policy.runtime_cache_paths),
        }
        return (
            "/* Generated by UIKitPR Cache. */\n"
            f"const CONFIG = {json.dumps(configuration, separators=(',', ':'))};\n"
            + _SERVICE_WORKER_RUNTIME
        )

    def write_service_worker(
        self,
        name: str = "sw.js",
        *,
        precache: Iterable[str] = (),
    ) -> Path:
        relative = self._safe_relative(name)
        destination = self.output.joinpath(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            self.service_worker_script(precache=precache),
            encoding="utf-8",
        )
        return destination

    def finalize(
        self,
        *,
        manifest_name: str = "asset-manifest.json",
        service_worker_name: str = "sw.js",
        precache: Iterable[str] = (),
    ) -> tuple[Path, Path]:
        return (
            self.write_manifest(manifest_name),
            self.write_service_worker(service_worker_name, precache=precache),
        )


def cache_script(*, minified: bool = False) -> str:
    """Retorna o cliente de cache distribuído com a biblioteca."""
    source = (
        files("uikitpr")
        .joinpath("assets/uikitpr-cache.js")
        .read_text(encoding="utf-8")
    )
    if not minified:
        return source
    source = re.sub(r"/\*[\s\S]*?\*/", "", source)
    return "\n".join(
        line.strip()
        for line in source.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )


def CacheRuntime(props: Any = None, *children: Any, **kwargs: Any):
    """Inclui o cliente que registra, atualiza e invalida o Service Worker."""
    p = component_props(props, children, **kwargs)
    source = p.get("src")
    if not source:
        payload = base64.b64encode(
            cache_script(minified=p.get("minified", True)).encode("utf-8")
        ).decode("ascii")
        source = f"data:text/javascript;base64,{payload}"
    script_props = {
        "src": source,
        "defer": p.get("defer", True),
        "data-uipr-cache-runtime": "true",
        "data-service-worker": p.get("service_worker", "sw.js"),
        "data-manifest": p.get("manifest", "asset-manifest.json"),
        "data-version": str(p.get("version", "1")),
        "data-cache-name": p.get("cache_name", "uikitpr"),
        "data-auto": str(bool(p.get("auto", True))).lower(),
    }
    if p.get("scope"):
        script_props["data-scope"] = p["scope"]
    if p.get("nonce"):
        script_props["nonce"] = p["nonce"]
    return h("script", script_props)


_SERVICE_WORKER_RUNTIME = r"""
const STATIC_DESTINATIONS = new Set([
  "style", "script", "image", "font", "worker", "manifest", "audio", "video"
]);
const PRECACHE_URLS = new Set(
  CONFIG.assets.map((value) => new URL(value, self.registration.scope).href)
);

const requestFor = (value) => new Request(
  new URL(value, self.registration.scope).href,
  { cache: "reload" }
);

const currentCache = () => caches.open(CONFIG.cacheName);

const responseIsCacheable = (response) => {
  if (!response || !response.ok) return false;
  const cacheControl = (response.headers.get("cache-control") || "").toLowerCase();
  if (cacheControl.includes("no-store") || cacheControl.includes("private")) return false;
  return response.headers.get("vary") !== "*";
};

const isExplicitRuntimePath = (url) =>
  CONFIG.runtimeCachePaths.some((prefix) => url.pathname.startsWith(prefix));

const shouldHandleRequest = (request) => {
  if (request.method !== "GET") return false;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return false;
  if (request.headers.has("authorization")) return false;
  if (request.mode === "navigate") return CONFIG.cacheNavigations;
  return STATIC_DESTINATIONS.has(request.destination)
    || PRECACHE_URLS.has(url.href)
    || isExplicitRuntimePath(url);
};

self.addEventListener("install", (event) => {
  event.waitUntil(
    currentCache()
      .then((cache) => cache.addAll(CONFIG.assets.map(requestFor)))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names
          .filter((name) => name.startsWith(`${CONFIG.cachePrefix}-`) && name !== CONFIG.cacheName)
          .map((name) => caches.delete(name))
      ))
      .then(() => self.clients.claim())
  );
});

const cacheFirst = async (request) => {
  const cache = await currentCache();
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (responseIsCacheable(response)) await cache.put(request, response.clone());
  return response;
};

const networkFirst = async (request) => {
  const cache = await currentCache();
  try {
    const response = await fetch(request);
    if (responseIsCacheable(response)) await cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) return cached;
    if (CONFIG.offlineFallback) {
      return cache.match(new URL(CONFIG.offlineFallback, self.registration.scope).href);
    }
    throw error;
  }
};

const staleWhileRevalidate = async (request, event) => {
  const cache = await currentCache();
  const cached = await cache.match(request);
  const update = fetch(request).then(async (response) => {
    if (responseIsCacheable(response)) await cache.put(request, response.clone());
    return response;
  });
  if (cached) {
    event.waitUntil(update.catch(() => undefined));
    return cached;
  }
  return update;
};

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (!shouldHandleRequest(request)) return;
  const strategy = request.mode === "navigate"
    ? CONFIG.navigationStrategy
    : CONFIG.strategy;
  if (strategy === "network-first") event.respondWith(networkFirst(request));
  else if (strategy === "cache-first") event.respondWith(cacheFirst(request));
  else event.respondWith(staleWhileRevalidate(request, event));
});

self.addEventListener("message", (event) => {
  const type = event.data && event.data.type;
  if (type === "UIKITPR_SKIP_WAITING") self.skipWaiting();
  if (type === "UIKITPR_CLEAR") {
    event.waitUntil(
      caches.keys()
        .then((names) => Promise.all(
          names
            .filter((name) => name.startsWith(`${CONFIG.cachePrefix}-`))
            .map((name) => caches.delete(name))
        ))
        .then(() => event.source && event.source.postMessage({ type: "UIKITPR_CLEARED" }))
    );
  }
});
"""
