"""Temas, tokens e entrega do stylesheet."""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
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


def stylesheet(*, minified: bool = False) -> str:
    """Lê o CSS distribuído junto do pacote."""
    css = files("uikitpr").joinpath("assets/uikitpr.css").read_text(encoding="utf-8")
    if not minified:
        return css
    return " ".join(line.strip() for line in css.splitlines() if line.strip())


def stylesheet_data_url(*, minified: bool = True) -> str:
    """Retorna uma URL ``data:`` que permanece íntegra no SSR do PyReact."""
    payload = base64.b64encode(stylesheet(minified=minified).encode("utf-8")).decode("ascii")
    return f"data:text/css;base64,{payload}"


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
    from .motion import MotionRuntime

    p = component_props(props, children, **kwargs)
    theme = p.get("theme", "light")
    theme_name = theme.name if isinstance(theme, Theme) else str(theme)
    color_mode = p.get("color_mode", theme_name)
    content = children_of(p)
    if p.get("with_styles", True):
        content.insert(0, Styles({"minified": p.get("minified", False)}))
    if p.get("with_motion", True):
        motion_props = {"minified": p.get("minified", False)}
        if p.get("motion_src"):
            motion_props["src"] = p["motion_src"]
        content.insert(1 if p.get("with_styles", True) else 0, MotionRuntime(motion_props))
    if isinstance(theme, Theme) and theme.tokens:
        insert_at = int(bool(p.get("with_styles", True))) + int(
            bool(p.get("with_motion", True))
        )
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
            "minified",
            "full_height",
        },
    )
    root_props["data-uipr-theme"] = theme_name
    root_props["data-uipr-color-mode"] = color_mode
    return h(p.get("as_", "div"), root_props, *content)
