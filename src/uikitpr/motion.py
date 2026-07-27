"""Motor declarativo de motion do UIKitPR para PyReact."""

from __future__ import annotations

import base64
import json
import re
from dataclasses import asdict, dataclass, field
from importlib.resources import files
from typing import Any, Iterable, Mapping, Sequence

from pyreact import h

from .core import children_of, component_props, cx, dom_props

MOTION_START = "uipr:motion:start"
MOTION_FINISH = "uipr:motion:finish"
MOTION_CANCEL = "uipr:motion:cancel"
MOTION_UPDATE = "uipr:motion:update"


@dataclass(frozen=True)
class Spring:
    """Parâmetros físicos de uma mola amortecida."""

    stiffness: float = 170.0
    damping: float = 26.0
    mass: float = 1.0
    velocity: float = 0.0
    precision: float = 0.001

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass(frozen=True)
class Transition:
    """Configuração temporal; duração e atraso são expressos em segundos."""

    duration: float = 0.45
    delay: float = 0.0
    easing: str = "cubic-bezier(0.22, 1, 0.36, 1)"
    repeat: int | str = 0
    direction: str = "normal"
    fill: str = "both"
    spring: Spring | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "duration": round(self.duration * 1000),
            "delay": round(self.delay * 1000),
            "easing": self.easing,
            "repeat": self.repeat,
            "direction": self.direction,
            "fill": self.fill,
        }
        if self.spring:
            data["spring"] = self.spring.to_dict()
        return data


@dataclass(frozen=True)
class TimelineStep:
    """Uma etapa de timeline dirigida por seletor ou id de motion."""

    target: str
    animate: Mapping[str, Any] | Sequence[Mapping[str, Any]] | str
    transition: Transition = field(default_factory=Transition)
    at: float | str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "target": self.target,
            "animate": self.animate,
            "transition": self.transition.to_dict(),
        }
        if self.at is not None:
            result["at"] = self.at
        return result


@dataclass(frozen=True)
class Timeline:
    """Sequência serializável executada pelo runtime UIKitPR Motion."""

    steps: Sequence[TimelineStep]
    autoplay: bool = True
    repeat: int | str = 0
    id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "autoplay": self.autoplay,
            "repeat": self.repeat,
            "steps": [step.to_dict() for step in self.steps],
        }


PRESETS: dict[str, dict[str, Any]] = {
    "fade": {"initial": {"opacity": 0}, "animate": {"opacity": 1}},
    "fade-up": {
        "initial": {"opacity": 0, "transform": "translateY(24px)"},
        "animate": {"opacity": 1, "transform": "translateY(0)"},
    },
    "fade-down": {
        "initial": {"opacity": 0, "transform": "translateY(-24px)"},
        "animate": {"opacity": 1, "transform": "translateY(0)"},
    },
    "slide-left": {
        "initial": {"opacity": 0, "transform": "translateX(36px)"},
        "animate": {"opacity": 1, "transform": "translateX(0)"},
    },
    "slide-right": {
        "initial": {"opacity": 0, "transform": "translateX(-36px)"},
        "animate": {"opacity": 1, "transform": "translateX(0)"},
    },
    "scale": {
        "initial": {"opacity": 0, "transform": "scale(.88)"},
        "animate": {"opacity": 1, "transform": "scale(1)"},
    },
    "pop": {
        "initial": {"opacity": 0, "transform": "scale(.65) rotate(-4deg)"},
        "animate": {"opacity": 1, "transform": "scale(1) rotate(0)"},
    },
    "blur": {
        "initial": {"opacity": 0, "filter": "blur(12px)"},
        "animate": {"opacity": 1, "filter": "blur(0)"},
    },
    "flip": {
        "initial": {"opacity": 0, "transform": "perspective(800px) rotateX(-70deg)"},
        "animate": {"opacity": 1, "transform": "perspective(800px) rotateX(0)"},
    },
    "shake": {
        "keyframes": [
            {"transform": "translateX(0)"},
            {"transform": "translateX(-8px)"},
            {"transform": "translateX(8px)"},
            {"transform": "translateX(-5px)"},
            {"transform": "translateX(5px)"},
            {"transform": "translateX(0)"},
        ]
    },
    "pulse": {
        "keyframes": [
            {"transform": "scale(1)", "opacity": 1},
            {"transform": "scale(1.04)", "opacity": 0.82},
            {"transform": "scale(1)", "opacity": 1},
        ]
    },
    "float": {
        "keyframes": [
            {"transform": "translateY(0)"},
            {"transform": "translateY(-10px)"},
            {"transform": "translateY(0)"},
        ]
    },
}


def _serialize(value: Any) -> Any:
    if isinstance(value, Transition):
        return value.to_dict()
    if isinstance(value, Spring):
        return value.to_dict()
    if isinstance(value, Timeline):
        return value.to_dict()
    if isinstance(value, TimelineStep):
        return value.to_dict()
    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize(item) for item in value]
    return value


def motion_script(*, minified: bool = False) -> str:
    """Retorna o runtime JavaScript distribuído com a biblioteca."""
    source = (
        files("uikitpr")
        .joinpath("assets/uikitpr-motion.js")
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


def motion_script_data_url(*, minified: bool = True) -> str:
    payload = base64.b64encode(motion_script(minified=minified).encode("utf-8")).decode(
        "ascii"
    )
    return f"data:text/javascript;base64,{payload}"


def MotionRuntime(props: Any = None, *children: Any, **kwargs: Any):
    """Inclui o runtime, externamente ou via data URL SSR-safe."""
    p = component_props(props, children, **kwargs)
    source = p.get("src") or motion_script_data_url(minified=p.get("minified", True))
    script_props = {
        "src": source,
        "data-uipr-motion-runtime": "true",
        "defer": p.get("defer", True),
    }
    if p.get("nonce"):
        script_props["nonce"] = p["nonce"]
    return h("script", script_props)


def Motion(props: Any = None, *children: Any, **kwargs: Any):
    """Componente motion universal.

    Pode ser usado diretamente::

        Motion("Olá", preset="fade-up", trigger="in-view")

    ou por meio de ``h(Motion, {"children": ...})``.
    """

    p = component_props(props, children, **kwargs)
    transition = p.get("transition", Transition())
    config: dict[str, Any] = {
        "preset": p.get("preset"),
        "trigger": p.get("trigger", "mount"),
        "initial": p.get("initial"),
        "animate": p.get("animate"),
        "keyframes": p.get("keyframes"),
        "exit": p.get("exit"),
        "transition": _serialize(transition),
        "whileHover": p.get("while_hover"),
        "whileTap": p.get("while_tap"),
        "whileFocus": p.get("while_focus"),
        "inView": p.get("in_view"),
        "scroll": p.get("scroll"),
        "stagger": p.get("stagger"),
        "staggerSelector": p.get("stagger_selector"),
        "replay": p.get("replay", False),
        "once": p.get("once", True),
        "timeline": _serialize(p.get("timeline")) if p.get("timeline") else None,
    }
    config = {key: _serialize(value) for key, value in config.items() if value is not None}
    if p.get("motion_id"):
        config["id"] = p["motion_id"]
    node_props = dom_props(
        p,
        base_class=cx("uipr-motion", p.get("will_change", True) and "uipr-will-change"),
        internal={
            "preset",
            "trigger",
            "initial",
            "animate",
            "keyframes",
            "exit",
            "transition",
            "while_hover",
            "while_tap",
            "while_focus",
            "in_view",
            "scroll",
            "stagger",
            "stagger_selector",
            "replay",
            "once",
            "timeline",
            "motion_id",
            "will_change",
        },
    )
    node_props["data-uipr-motion"] = json.dumps(
        config, ensure_ascii=False, separators=(",", ":")
    )
    if p.get("motion_id"):
        node_props["data-uipr-motion-id"] = p["motion_id"]
    return h(p.get("as_", "div"), node_props, *children_of(p))


def MotionGroup(props: Any = None, *children: Any, **kwargs: Any):
    """Agrupa filhos para stagger, orchestration ou timeline."""
    p = component_props(props, children, **kwargs)
    config = {
        "stagger": round(float(p.get("stagger", 0.08)) * 1000),
        "delay": round(float(p.get("delay", 0)) * 1000),
        "selector": p.get("selector", ":scope > *"),
        "trigger": p.get("trigger", "in-view"),
        "preset": p.get("preset", "fade-up"),
        "once": p.get("once", True),
    }
    node_props = dom_props(
        p,
        base_class="uipr-motion-group",
        internal={"stagger", "delay", "selector", "trigger", "preset", "once"},
    )
    node_props["data-uipr-motion-group"] = json.dumps(config, separators=(",", ":"))
    return h(p.get("as_", "div"), node_props, *children_of(p))


def MotionTimeline(props: Any = None, *children: Any, **kwargs: Any):
    """Declara uma timeline que pode ser acionada pelo runtime."""
    p = component_props(props, children, **kwargs)
    timeline = p.get("timeline")
    if not isinstance(timeline, Timeline):
        raise TypeError("MotionTimeline requer timeline=Timeline(...).")
    node_props = dom_props(
        p,
        base_class="uipr-motion-timeline",
        internal={"timeline"},
    )
    node_props["data-uipr-timeline"] = json.dumps(
        timeline.to_dict(), ensure_ascii=False, separators=(",", ":")
    )
    return h(p.get("as_", "div"), node_props, *children_of(p))


def spring_keyframes(
    start: float = 0.0,
    end: float = 1.0,
    *,
    spring: Spring = Spring(),
    frames: int = 60,
) -> list[float]:
    """Amostra uma mola amortecida; útil para testes e animações customizadas."""
    if frames < 2:
        raise ValueError("frames deve ser >= 2")
    if spring.mass <= 0 or spring.stiffness <= 0 or spring.damping < 0:
        raise ValueError("Parâmetros físicos inválidos.")
    position = start
    velocity = spring.velocity
    dt = 1 / 60
    result = [start]
    for _ in range(frames - 2):
        displacement = position - end
        acceleration = (
            -spring.stiffness * displacement - spring.damping * velocity
        ) / spring.mass
        velocity += acceleration * dt
        position += velocity * dt
        result.append(position)
    result.append(end)
    return result


def stagger(
    items: Iterable[Any],
    *,
    preset: str = "fade-up",
    each: float = 0.08,
    delay: float = 0.0,
    transition: Transition | None = None,
) -> list[Any]:
    """Envolve itens em Motion com atraso incremental."""
    base = transition or Transition()
    return [
        Motion(
            item,
            preset=preset,
            transition=Transition(
                duration=base.duration,
                delay=delay + index * each,
                easing=base.easing,
                repeat=base.repeat,
                direction=base.direction,
                fill=base.fill,
                spring=base.spring,
            ),
        )
        for index, item in enumerate(items)
    ]


def motion_event(name: str, detail: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Cria uma descrição de evento customizado para integrações."""
    return {"name": name, "detail": dict(detail or {})}


def motion_control(
    target: str,
    preset: str | None = None,
    *,
    animate: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
    transition: Transition | Mapping[str, Any] | None = None,
) -> dict[str, str]:
    """Cria atributos para um controle declarativo do runtime Motion.

    Os atributos podem ser espalhados em qualquer componente clicável::

        Button("Pop", **motion_control("hero", "pop"))
    """
    if not target:
        raise ValueError("target não pode ser vazio")
    config: dict[str, Any] = {"target": target}
    if preset:
        config["preset"] = preset
    if animate is not None:
        config["animate"] = _serialize(animate)
    if transition is not None:
        config["transition"] = _serialize(transition)
    return {
        "data-uipr-motion-control": json.dumps(
            config,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    }
