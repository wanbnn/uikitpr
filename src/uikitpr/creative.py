"""Catálogo criativo nativo com 135 componentes UIKitPR.

The public names belong to UIKitPR and share a small set of rendering
primitives so the catalog can grow without duplicating runtime infrastructure.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from importlib.resources import files
import re
from typing import Any

from pyreact import h

from .core import children_of, component_props, cx, element
from .effects import (
    BlurText as _BlurText,
    GradientText as _GradientText,
    ShinyText as _ShinyText,
    SplitText as _SplitText,
    SpotlightCard as _SpotlightCard,
    StarBorder as _StarBorder,
)


TEXT_ANIMATIONS = (
    "ASCIIText", "BlurText", "CircularText", "CountUp", "CurvedLoop",
    "DecryptedText", "FallingText", "FuzzyText", "GlitchText", "GradientText",
    "RotatingText", "ScrambledText", "ScrollFloat", "ScrollReveal",
    "ScrollVelocity", "ShinyText", "SplitText", "TextCursor", "TextPressure",
    "TextTrail", "TrueFocus", "VariableProximity",
)

ANIMATIONS = (
    "AnimatedContent", "Antigravity", "BlobCursor", "ClickSpark", "Crosshair",
    "Cubes", "ElectricBorder", "FadeContent", "GhostCursor", "GlareHover",
    "GradualBlur", "ImageTrail", "LaserFlow", "LogoLoop", "Magnet",
    "MagnetLines", "MetaBalls", "MetallicPaint", "Noise", "OrbitImages",
    "PixelTrail", "PixelTransition", "Ribbons", "ShapeBlur", "SplashCursor",
    "StarBorder", "StickerPeel", "TargetCursor",
)

UI_COMPONENTS = (
    "AnimatedList", "BorderGlow", "BounceCards", "BubbleMenu", "CardNav",
    "CardSwap", "Carousel", "ChromaGrid", "CircularGallery", "Counter",
    "CurvedInput", "DecayCard", "Dock", "DomeGallery", "ElasticSlider",
    "FlowingMenu", "FluidGlass", "FlyingPosters", "Folder", "GlassIcons",
    "GlassSurface", "GooeyNav", "InfiniteMenu", "Lanyard", "LineSidebar",
    "MagicBento", "Masonry", "ModelViewer", "PillNav", "PixelCard",
    "ProfileCard", "ReflectiveCard", "ScrollStack", "SpotlightCard", "Stack",
    "StaggeredMenu", "Stepper", "TiltedCard",
)

BACKGROUNDS = (
    "AcidSquares", "Aurora", "Balatro", "Ballpit", "Beams", "ColorBends",
    "DarkVeil", "Dither", "DotField", "DotGrid", "EvilEye", "FaultyTerminal",
    "Ferrofluid", "FloatingLines", "Galaxy", "GradientBlinds", "GradientWaves",
    "Grainient", "GridDistortion", "GridMotion", "GridScan", "Hyperspeed",
    "Iridescence", "LetterGlitch", "LightPillar", "LightRays", "Lightfall",
    "Lightning", "LineWaves", "LiquidChrome", "LiquidEther", "Orb", "Particles",
    "PixelBlast", "PixelSnow", "Plasma", "PlasmaWave", "Prism",
    "PrismaticBurst", "Radar", "RippleGrid", "ShapeGrid", "SideRays", "Silk",
    "SoftAurora", "Threads", "Waves",
)


@dataclass(frozen=True)
class CreativeItem:
    name: str
    category: str
    slug: str
    archetype: str


def _slug(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def _archetype(name: str, category: str) -> str:
    if category == "text":
        groups = {
            "terminal": {"ASCIIText", "DecryptedText", "ScrambledText", "TextCursor"},
            "distort": {"FuzzyText", "GlitchText", "TextPressure", "VariableProximity"},
            "path": {"CircularText", "CurvedLoop", "TextTrail"},
            "scroll": {"ScrollFloat", "ScrollReveal", "ScrollVelocity"},
            "loop": {"RotatingText", "TrueFocus"},
        }
    elif category == "animation":
        groups = {
            "cursor": {"BlobCursor", "Crosshair", "GhostCursor", "ImageTrail", "PixelTrail", "SplashCursor", "TargetCursor"},
            "field": {"Antigravity", "Cubes", "MagnetLines", "MetaBalls", "OrbitImages", "Ribbons"},
            "surface": {"ElectricBorder", "GlareHover", "MetallicPaint", "Noise", "ShapeBlur", "StickerPeel"},
            "reveal": {"AnimatedContent", "FadeContent", "GradualBlur", "PixelTransition"},
        }
    elif category == "component":
        groups = {
            "navigation": {"BubbleMenu", "CardNav", "Dock", "FlowingMenu", "GooeyNav", "LineSidebar", "PillNav", "StaggeredMenu"},
            "gallery": {"Carousel", "ChromaGrid", "CircularGallery", "DomeGallery", "FlyingPosters", "InfiniteMenu", "Masonry"},
            "glass": {"FluidGlass", "GlassIcons", "GlassSurface", "ReflectiveCard"},
            "cards": {"BorderGlow", "BounceCards", "CardSwap", "DecayCard", "MagicBento", "PixelCard", "ProfileCard", "ScrollStack", "Stack", "TiltedCard"},
            "control": {"Counter", "CurvedInput", "ElasticSlider", "Stepper"},
        }
    else:
        groups = {
            "grid": {"AcidSquares", "Dither", "DotField", "DotGrid", "FaultyTerminal", "GridDistortion", "GridMotion", "GridScan", "PixelBlast", "PixelSnow", "RippleGrid", "ShapeGrid"},
            "light": {"Beams", "LightPillar", "LightRays", "Lightfall", "Lightning", "PrismaticBurst", "SideRays"},
            "fluid": {"Aurora", "ColorBends", "DarkVeil", "Ferrofluid", "GradientBlinds", "GradientWaves", "Grainient", "Iridescence", "LiquidChrome", "LiquidEther", "Plasma", "PlasmaWave", "Silk", "SoftAurora"},
            "space": {"Ballpit", "Galaxy", "Hyperspeed", "Orb", "Particles", "Prism", "Radar"},
            "lines": {"FloatingLines", "LineWaves", "Threads", "Waves"},
        }
    for archetype, names in groups.items():
        if name in names:
            return archetype
    return "default"


CREATIVE_CATALOG = tuple(
    CreativeItem(name, category, _slug(name), _archetype(name, category))
    for category, names in (
        ("text", TEXT_ANIMATIONS),
        ("animation", ANIMATIONS),
        ("component", UI_COMPONENTS),
        ("background", BACKGROUNDS),
    )
    for name in names
)


def _style(p: dict[str, Any]) -> dict[str, Any]:
    style = dict(p.get("style") or {})
    style.update({
        "--uipr-creative-color": str(p.get("color", "var(--uipr-primary)")),
        "--uipr-creative-secondary": str(p.get("secondary", "#26c6da")),
        "--uipr-creative-speed": f"{p.get('speed', 8)}s" if isinstance(p.get("speed", 8), (int, float)) else str(p.get("speed")),
        "--uipr-creative-intensity": str(p.get("intensity", 1)),
    })
    return style


def _text(item: CreativeItem, p: dict[str, Any]):
    content = "".join(str(child) for child in children_of(p)) or str(p.get("text", item.name))
    if item.name == "BlurText":
        return _BlurText({**p, "children": content})
    if item.name == "SplitText":
        return _SplitText({**p, "children": content})
    if item.name == "ShinyText":
        return _ShinyText({**p, "children": content})
    if item.name == "GradientText":
        return _GradientText({**p, "children": content})
    if item.name == "CountUp":
        p["data-uipr-creative-from"] = str(p.get("from_", 0))
        p["data-uipr-creative-to"] = str(p.get("to", p.get("value", 100)))
        content = str(p.get("from_", 0))
    chars = [h("span", {"aria-hidden": "true", "style": {"--i": str(i)}}, char) for i, char in enumerate(content)]
    return element(
        p.get("as_", "span"), p,
        base_class=cx("uipr-creative", "uipr-creative-text", f"uipr-creative-{item.archetype}", f"uipr-creative-{item.slug}"),
        internal={"text", "color", "secondary", "speed", "intensity", "from_", "to", "value"},
        children=[h("span", {"className": "sr-only"}, content), *chars],
    )


def _items(p: dict[str, Any], fallback: str) -> list[Any]:
    values = p.get("items")
    if values is None:
        children = children_of(p)
        return children or [fallback]
    if not isinstance(values, (list, tuple)):
        values = [values]
    result = []
    for value in values:
        if isinstance(value, dict):
            result.append(value.get("content") or value.get("label") or value.get("title") or "Item")
        else:
            result.append(value)
    return result


def _ui(item: CreativeItem, p: dict[str, Any]):
    values = _items(p, item.name)
    base = cx("uipr-creative", "uipr-creative-ui", f"uipr-creative-{item.archetype}", f"uipr-creative-{item.slug}")
    internal = {"items", "color", "secondary", "speed", "intensity", "min", "max", "step", "value", "label", "placeholder"}
    if item.name == "CurvedInput":
        return element("input", {**p, "placeholder": p.get("placeholder", "Type something…")}, base_class=base, internal=internal, children=[])
    if item.name == "ElasticSlider":
        return element("input", {**p, "type": "range", "min": p.get("min", 0), "max": p.get("max", 100), "value": p.get("value", 50)}, base_class=base, internal=internal, children=[])
    if item.name == "Counter":
        p["data-uipr-creative-from"] = str(p.get("from_", 0))
        p["data-uipr-creative-to"] = str(p.get("to", p.get("value", 100)))
        return element("output", p, base_class=base, internal=internal | {"from_", "to"}, children=[str(p.get("from_", 0))])
    tag = "nav" if item.archetype == "navigation" else "div"
    child_tag = "a" if item.archetype == "navigation" else "div"
    rendered = [h(child_tag, {"className": "uipr-creative-item", **({"href": "#"} if child_tag == "a" else {})}, value) for value in values]
    return element(tag, p, base_class=base, internal=internal, children=rendered)


def Creative(props: Any = None, *children: Any, name: str, category: str, **kwargs: Any):
    """Generic renderer behind every named catalog component."""
    p = component_props(props, children, **kwargs)
    item = next(item for item in CREATIVE_CATALOG if item.name == name and item.category == category)
    p["data-uipr-creative"] = item.slug
    p["data-uipr-creative-category"] = category
    p["data-uipr-creative-archetype"] = item.archetype
    p["style"] = _style(p)
    if category == "text":
        return _text(item, p)
    if category == "component":
        return _ui(item, p)
    if category == "animation" and item.name == "StarBorder":
        return _StarBorder(p)
    content = children_of(p)
    layers = [h("span", {"className": f"uipr-creative-layer uipr-creative-layer-{i}", "aria-hidden": "true"}) for i in range(1, 4)]
    if item.archetype in {"cursor", "field", "space"}:
        layers.insert(0, h("canvas", {"className": "uipr-creative-canvas", "aria-hidden": "true"}))
    return element(
        p.get("as_", "div"), p,
        base_class=cx("uipr-creative", f"uipr-creative-{category}", f"uipr-creative-{item.archetype}", f"uipr-creative-{item.slug}"),
        internal={"color", "secondary", "speed", "intensity"},
        children=[*layers, h("div", {"className": "uipr-creative-content"}, *content) if content else None],
    )


def _factory(item: CreativeItem):
    def component(props: Any = None, *children: Any, **kwargs: Any):
        return Creative(props, *children, name=item.name, category=item.category, **kwargs)
    component.__name__ = item.name
    component.__qualname__ = item.name
    component.__doc__ = f"UIKitPR creative {item.category} component {item.name}."
    return component


for _item in CREATIVE_CATALOG:
    globals()[_item.name] = _factory(_item)


def creative_script(*, minified: bool = False) -> str:
    script = files("uikitpr").joinpath("assets/uikitpr-creative.js").read_text(encoding="utf-8")
    if not minified:
        return script
    return " ".join(line.strip() for line in script.splitlines() if line.strip() and not line.lstrip().startswith("//"))


def CreativeRuntime(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    if p.get("src"):
        return h("script", {"src": p["src"], "defer": True, "data-uipr-creative-runtime": "true"})
    payload = base64.b64encode(creative_script(minified=bool(p.get("minified"))).encode()).decode()
    return h("script", {"src": f"data:text/javascript;base64,{payload}", "defer": True, "data-uipr-creative-runtime": "true"})


__all__ = [
    *TEXT_ANIMATIONS, *ANIMATIONS, *UI_COMPONENTS, *BACKGROUNDS,
    "ANIMATIONS", "BACKGROUNDS", "CREATIVE_CATALOG", "Creative",
    "CreativeItem", "CreativeRuntime", "TEXT_ANIMATIONS", "UI_COMPONENTS",
    "creative_script",
]
