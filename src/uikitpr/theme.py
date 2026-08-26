"""Temas, tokens e entrega do stylesheet."""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from functools import lru_cache
from importlib.resources import files
import re
from typing import Any, Mapping

from pyreact import h

from .core import children_of, component_props, cx, dom_props


@dataclass(frozen=True)
class Theme:
    """Conjunto imutável de custom properties do UIKitPR."""

    name: str = "custom"
    tokens: Mapping[str, str] = field(default_factory=dict)

    def css(self, selector: str | None = None) -> str:
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", self.name)
        target = selector or f"[data-uipr-theme={safe_name}]"
        declarations = "".join(
            f"--uipr-{key.replace('_', '-')}:{value};"
            for key, value in sorted(self.tokens.items())
        )
        return f"{target}{{{declarations}}}"


def create_theme(name: str = "custom", **tokens: str) -> Theme:
    return Theme(name=name, tokens=tokens)


@lru_cache(maxsize=2)
def stylesheet(*, minified: bool = False) -> str:
    """Lê o CSS distribuído junto do pacote uma vez por variante."""
    css = files("uikitpr").joinpath("assets/uikitpr.css").read_text(encoding="utf-8")
    if not minified:
        return css
    return " ".join(line.strip() for line in css.splitlines() if line.strip())


@lru_cache(maxsize=2)
def stylesheet_data_url(*, minified: bool = True) -> str:
    """Retorna uma URL ``data:`` SSR-safe, reutilizada entre renders."""
    payload = base64.b64encode(stylesheet(minified=minified).encode("utf-8")).decode("ascii")
    return f"data:text/css;base64,{payload}"


@lru_cache(maxsize=6)
def _runtime_data_url(kind: str, minified: bool) -> str:
    """Materializa runtimes estáticos apenas uma vez por processo e variante."""
    if kind == "motion":
        from .motion import motion_script

        source = motion_script(minified=minified)
    elif kind == "creative":
        from .creative import creative_script

        source = creative_script(minified=minified)
    elif kind == "cache":
        from .cache import cache_script

        source = cache_script(minified=minified)
    else:
        raise ValueError(f"Runtime UIKitPR desconhecido: {kind}")
    payload = base64.b64encode(source.encode("utf-8")).decode("ascii")
    return f"data:text/javascript;base64,{payload}"


def Styles(props: Any = None, *children: Any, **kwargs: Any):
    """Componente que inclui o CSS por link/data URL ou, opcionalmente, inline."""
    p = component_props(props, children, **kwargs)
    href = p.get("href")
    if p.get("inline"):
        return h(
            "style",
            {
                "data-uipr": "styles",
                **({"nonce": p["nonce"]} if p.get("nonce") else {}),
            },
            stylesheet(minified=bool(p.get("minified"))),
        )
    return h(
        "link",
        {
            "rel": "stylesheet",
            "href": href or stylesheet_data_url(minified=p.get("minified", True)),
            "data-uipr": "styles",
        },
    )


def UIProvider(props: Any = None, *children: Any, **kwargs: Any):
    """Raiz visual com tema, modo de cor e stylesheet opcionais."""
    from .cache import CacheRuntime
    from .motion import MotionRuntime
    from .creative import CreativeRuntime

    p = component_props(props, children, **kwargs)
    theme = p.get("theme", "light")
    theme_name = theme.name if isinstance(theme, Theme) else str(theme)
    color_mode = p.get("color_mode", theme_name)
    minified = bool(p.get("minified", False))
    content = children_of(p)
    if p.get("with_styles", True):
        content.insert(0, Styles({"minified": minified}))
    if p.get("with_motion", True):
        motion_props = {
            "minified": minified,
            "src": p.get("motion_src") or _runtime_data_url("motion", minified),
        }
        content.insert(1 if p.get("with_styles", True) else 0, MotionRuntime(motion_props))
    if p.get("with_creative", True):
        creative_props = {
            "minified": minified,
            "src": p.get("creative_src") or _runtime_data_url("creative", minified),
        }
        insert_at = int(bool(p.get("with_styles", True))) + int(bool(p.get("with_motion", True)))
        content.insert(insert_at, CreativeRuntime(creative_props))
    if p.get("with_cache", False):
        cache_props = {
            "src": p.get("cache_src") or _runtime_data_url("cache", True),
            "service_worker": p.get("service_worker", "sw.js"),
            "manifest": p.get("cache_manifest", "asset-manifest.json"),
            "version": p.get("cache_version", "1"),
            "cache_name": p.get("cache_name", "uikitpr"),
        }
        insert_at = int(bool(p.get("with_styles", True))) + int(
            bool(p.get("with_motion", True))
        ) + int(bool(p.get("with_creative", True)))
        content.insert(insert_at, CacheRuntime(cache_props))
    if isinstance(theme, Theme) and theme.tokens:
        insert_at = int(bool(p.get("with_styles", True))) + int(
            bool(p.get("with_motion", True))
        ) + int(bool(p.get("with_creative", True))) + int(bool(p.get("with_cache", False)))
        content.insert(insert_at, h("style", None, theme.css()))
    root_props = dom_props(
        p,
        base_class=cx("uipr-root", p.get("full_height") and "min-h-screen"),
        internal={
            "theme",
            "color_mode",
            "with_styles",
            "with_motion",
            "motion_src",
            "with_creative",
            "creative_src",
            "with_cache",
            "cache_src",
            "service_worker",
            "cache_manifest",
            "cache_version",
            "cache_name",
            "minified",
            "full_height",
        },
    )
    root_props["data-uipr-theme"] = theme_name
    root_props["data-uipr-color-mode"] = color_mode
    return h(p.get("as_", "div"), root_props, *content)
