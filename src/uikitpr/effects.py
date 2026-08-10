"""Efeitos visuais prontos e sem dependências para aplicações PyReact."""

from __future__ import annotations

from typing import Any

from pyreact import h

from .core import children_of, component_props, cx, element


def _duration(value: Any, default: float) -> str:
    """Normaliza segundos/números e valores CSS para custom properties."""
    value = default if value is None else value
    return f"{value}s" if isinstance(value, (int, float)) else str(value)


def AnimatedText(props: Any = None, *children: Any, **kwargs: Any):
    """Texto segmentado com animações ``blur``, ``rise``, ``wave`` ou ``reveal``."""
    p = component_props(props, children, **kwargs)
    content = "".join(str(child) for child in children_of(p))
    by = p.get("by", "word")
    effect = p.get("effect", "blur")
    segments = list(content) if by == "char" else content.split(" ")
    delay = max(0.0, float(p.get("delay", 0.045)))
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-text-duration": _duration(p.get("duration"), 0.7),
            "--uipr-text-distance": str(p.get("distance", "0.8em")),
        }
    )
    p["style"] = style
    pieces = []
    for index, segment in enumerate(segments):
        pieces.append(
            h(
                "span",
                {
                    "className": "uipr-animated-text-segment",
                    "style": {"--uipr-text-delay": f"{index * delay:g}s"},
                    "aria-hidden": "true",
                },
                segment,
                " " if by != "char" and index < len(segments) - 1 else None,
            )
        )
    return element(
        p.get("as_", "span"),
        p,
        base_class=cx("uipr-animated-text", f"uipr-text-effect-{effect}"),
        internal={"effect", "by", "delay", "duration", "distance"},
        children=[h("span", {"className": "sr-only"}, content), *pieces],
    )


def BlurText(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    p.setdefault("effect", "blur")
    return AnimatedText(p)


def SplitText(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    p.setdefault("effect", "rise")
    p.setdefault("by", "char")
    return AnimatedText(p)


def ShinyText(props: Any = None, *children: Any, **kwargs: Any):
    """Texto com brilho contínuo, inspirado em superfícies metálicas."""
    p = component_props(props, children, **kwargs)
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-shine-color": str(p.get("color", "currentColor")),
            "--uipr-shine-highlight": str(p.get("highlight", "#ffffff")),
            "--uipr-shine-duration": _duration(p.get("duration"), 2.5),
        }
    )
    p["style"] = style
    return element(
        p.get("as_", "span"),
        p,
        base_class="uipr-shiny-text",
        internal={"color", "highlight", "duration"},
    )


def GradientText(props: Any = None, *children: Any, **kwargs: Any):
    """Texto com gradiente animado configurável por cores e velocidade."""
    p = component_props(props, children, **kwargs)
    colors = p.get("colors", ("#6d4aff", "#26c6da", "#ff5ca8", "#6d4aff"))
    if isinstance(colors, str):
        colors = [colors]
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-gradient-colors": ", ".join(str(color) for color in colors),
            "--uipr-gradient-duration": _duration(p.get("duration"), 5),
        }
    )
    p["style"] = style
    return element(
        p.get("as_", "span"),
        p,
        base_class="uipr-gradient-text",
        internal={"colors", "duration"},
    )


def _background(name: str, p: dict[str, Any]):
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-bg-color": str(p.get("color", "var(--uipr-primary)")),
            "--uipr-bg-secondary": str(p.get("secondary", "#26c6da")),
            "--uipr-bg-size": str(p.get("size", "2rem")),
            "--uipr-bg-speed": _duration(p.get("speed"), 12),
            "--uipr-bg-opacity": str(p.get("opacity", 0.28)),
        }
    )
    p["style"] = style
    return element(
        p.get("as_", "div"),
        p,
        base_class=cx("uipr-background", f"uipr-background-{name}"),
        internal={"color", "secondary", "size", "speed", "opacity"},
        children=[h("span", {"className": "uipr-background-layer", "aria-hidden": "true"}), *children_of(p)],
    )


def AuroraBackground(props: Any = None, *children: Any, **kwargs: Any):
    return _background("aurora", component_props(props, children, **kwargs))


def DotBackground(props: Any = None, *children: Any, **kwargs: Any):
    return _background("dots", component_props(props, children, **kwargs))


def GridBackground(props: Any = None, *children: Any, **kwargs: Any):
    return _background("grid", component_props(props, children, **kwargs))


def BeamBackground(props: Any = None, *children: Any, **kwargs: Any):
    return _background("beams", component_props(props, children, **kwargs))


def SpotlightCard(props: Any = None, *children: Any, **kwargs: Any):
    """Superfície que revela um foco suave ao passar o ponteiro."""
    p = component_props(props, children, **kwargs)
    style = dict(p.get("style") or {})
    style["--uipr-spotlight-color"] = str(p.get("spotlight", "var(--uipr-primary)"))
    p["style"] = style
    return element(
        p.get("as_", "article"),
        p,
        base_class="uipr-spotlight-card",
        internal={"spotlight"},
    )


def StarBorder(props: Any = None, *children: Any, **kwargs: Any):
    """Contorno luminoso animado para ações e cartões em destaque."""
    p = component_props(props, children, **kwargs)
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-star-color": str(p.get("color", "var(--uipr-primary)")),
            "--uipr-star-speed": _duration(p.get("speed"), 4),
        }
    )
    p["style"] = style
    return element(
        p.get("as_", "div"),
        p,
        base_class="uipr-star-border",
        internal={"color", "speed"},
        children=[h("span", {"className": "uipr-star-border-content"}, *children_of(p))],
    )


def Marquee(props: Any = None, *children: Any, **kwargs: Any):
    """Faixa contínua que duplica o conteúdo para formar um loop sem corte."""
    p = component_props(props, children, **kwargs)
    content = children_of(p)
    style = dict(p.get("style") or {})
    style.update(
        {
            "--uipr-marquee-duration": _duration(p.get("duration"), 20),
            "--uipr-marquee-gap": str(p.get("gap", "2rem")),
        }
    )
    p["style"] = style
    track = [
        h("div", {"className": "uipr-marquee-group"}, *content),
        h("div", {"className": "uipr-marquee-group", "aria-hidden": "true"}, *content),
    ]
    return element(
        p.get("as_", "div"),
        p,
        base_class=cx("uipr-marquee", p.get("reverse") and "uipr-marquee-reverse"),
        internal={"duration", "gap", "reverse"},
        children=[h("div", {"className": "uipr-marquee-track"}, *track)],
    )
