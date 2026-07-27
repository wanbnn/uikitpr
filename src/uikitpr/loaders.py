"""Loaders e estados visuais do UIKitPR."""

from __future__ import annotations

from typing import Any

from pyreact import h

from .core import children_of, component_props, cx, element


def _loader(
    name: str,
    props: Any = None,
    children: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
    *,
    parts: int = 0,
):
    p = component_props(props, children, **(kwargs or {}))
    size = p.get("size", "md")
    tone = p.get("tone", "primary")
    label = p.get("label", "Carregando")
    content = [
        h("span", {"className": f"uipr-loader-part uipr-loader-part-{index + 1}"})
        for index in range(parts)
    ]
    content.extend(children_of(p))
    node = element(
        p.get("as_", "span"),
        p,
        base_class=cx(
            "uipr-loader",
            f"uipr-{name}-loader",
            f"uipr-loader-{size}",
            f"uipr-loader-{tone}",
        ),
        internal={"size", "tone", "label"},
        children=content,
    )
    node.props.setdefault("role", "status")
    node.props.setdefault("aria-label", label)
    return node


def DotsLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("dots", props, children, kwargs, parts=3)


def BarsLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("bars", props, children, kwargs, parts=5)


def RingLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("ring", props, children, kwargs, parts=1)


def PulseLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("pulse", props, children, kwargs, parts=2)


def OrbitLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("orbit", props, children, kwargs, parts=3)


def WaveLoader(props: Any = None, *children: Any, **kwargs: Any):
    return _loader("wave", props, children, kwargs, parts=5)


def Skeleton(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    variant = p.get("variant", "text")
    lines = max(1, int(p.get("lines", 1)))
    if lines > 1:
        return h(
            p.get("as_", "div"),
            {"className": cx("uipr-skeleton-group", p.get("className"))},
            *[
                h(
                    "span",
                    {
                        "className": cx(
                            "uipr-skeleton",
                            "uipr-skeleton-text",
                            index == lines - 1 and "uipr-skeleton-short",
                        ),
                        "aria-hidden": "true",
                    },
                )
                for index in range(lines)
            ],
        )
    node = element(
        p.get("as_", "span"),
        p,
        base_class=cx("uipr-skeleton", f"uipr-skeleton-{variant}"),
        internal={"variant", "lines"},
        children=[],
    )
    node.props["aria-hidden"] = "true"
    return node


def SkeletonCard(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    return h(
        p.get("as_", "div"),
        {"className": cx("uipr-skeleton-card", p.get("className"))},
        Skeleton(variant="rectangle"),
        h(
            "div",
            {"className": "uipr-skeleton-card-body"},
            Skeleton(variant="text"),
            Skeleton(lines=3),
        ),
    )


def PageLoader(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    loader_type = p.get("loader", "orbit")
    loaders = {
        "dots": DotsLoader,
        "bars": BarsLoader,
        "ring": RingLoader,
        "pulse": PulseLoader,
        "orbit": OrbitLoader,
        "wave": WaveLoader,
    }
    loader = loaders.get(loader_type, OrbitLoader)
    label = p.get("label", "Carregando aplicação")
    return h(
        p.get("as_", "div"),
        {
            "className": cx(
                "uipr-page-loader",
                p.get("overlay", True) and "uipr-page-loader-overlay",
                p.get("className"),
            ),
            "role": "status",
            "aria-live": "polite",
        },
        loader({"size": p.get("size", "lg"), "tone": p.get("tone", "primary"), "label": label}),
        h("span", {"className": "uipr-page-loader-label"}, str(label)),
    )

