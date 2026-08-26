import json

import pytest
from pyreact.server import render_to_static_markup

from uikitpr import (
    CacheManager,
    CachePolicy,
    CacheRuntime,
    cache_script,
)


def test_cache_manager_fingerprints_assets_and_writes_manifest(tmp_path):
    manager = CacheManager(
        tmp_path,
        policy=CachePolicy(name="my-app", version="7"),
    )
    first = manager.add_text("app.js", "console.log('one')")
    repeated = manager.add_text("copy.js", "console.log('one')")
    changed = manager.add_text("theme.css", "body { color: blue }")

    assert first.digest == repeated.digest
    assert first.path.startswith("assets/app.")
    assert first.path.endswith(".js")
    assert changed.path != first.path
    assert (tmp_path / first.path).read_text(encoding="utf-8") == "console.log('one')"
    assert manager.asset_url("app.js") == first.path

    manifest_path, worker_path = manager.finalize(precache=["./"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["cache"]["id"] == "my-app-7"
    assert manifest["cache"]["cacheNavigations"] is True
    assert manifest["cache"]["runtimeCachePaths"] == []
    assert manifest["assets"]["app.js"]["integrity"].startswith("sha256-")
    assert first.path in worker_path.read_text(encoding="utf-8")
    assert '"./"' in worker_path.read_text(encoding="utf-8")


def test_cache_manager_rejects_unsafe_paths_and_invalid_policy(tmp_path):
    manager = CacheManager(tmp_path)
    with pytest.raises(ValueError):
        manager.add_text("../outside.js", "bad")
    with pytest.raises(ValueError):
        CachePolicy(strategy="forever")
    with pytest.raises(ValueError, match="runtime_cache_paths"):
        CachePolicy(runtime_cache_paths=("https://example.com/api",))
    with pytest.raises(ValueError, match="runtime_cache_paths"):
        CachePolicy(runtime_cache_paths=("api/public",))
    with pytest.raises(KeyError):
        manager.asset_url("missing.js")


def test_service_worker_limits_runtime_cache_to_safe_requests(tmp_path):
    manager = CacheManager(tmp_path)
    manager.add_text("app.js", "console.log('safe')")
    worker = manager.service_worker_script()

    assert 'STATIC_DESTINATIONS.has(request.destination)' in worker
    assert 'request.headers.has("authorization")' in worker
    assert 'cacheControl.includes("no-store")' in worker
    assert 'cacheControl.includes("private")' in worker
    assert 'PRECACHE_URLS.has(url.href)' in worker
    assert 'cache.match(request)' in worker
    assert 'caches.match(request)' not in worker
    assert '"runtimeCachePaths":[]' in worker


def test_service_worker_supports_explicit_public_runtime_paths(tmp_path):
    policy = CachePolicy(
        cache_navigations=False,
        runtime_cache_paths=("/api/public/", "/content/"),
    )
    manager = CacheManager(tmp_path, policy=policy)
    worker = manager.service_worker_script()
    manifest = manager.manifest()

    assert manifest["cache"]["cacheNavigations"] is False
    assert manifest["cache"]["runtimeCachePaths"] == ["/api/public/", "/content/"]
    assert '"cacheNavigations":false' in worker
    assert '"runtimeCachePaths":["/api/public/","/content/"]' in worker
    assert 'CONFIG.runtimeCachePaths.some' in worker


def test_cache_runtime_and_packaged_script():
    html = render_to_static_markup(
        CacheRuntime(
            src="/assets/cache.js",
            service_worker="/sw.js",
            version="release-3",
            cache_name="my-app",
        )
    )
    assert 'data-uipr-cache-runtime="true"' in html
    assert 'data-service-worker="/sw.js"' in html
    assert 'data-version="release-3"' in html
    assert 'data-cache-name="my-app"' in html
    source = cache_script()
    assert "window.UIKitPRCache" in source
    assert "updateViaCache" in source
    assert len(cache_script(minified=True)) < len(source)
