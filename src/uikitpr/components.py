"""Componentes PyReact acessíveis e customizáveis do UIKitPR."""

from __future__ import annotations

from typing import Any

from pyreact import h

from .core import children_of, component_props, cx, element


def _simple(name: str, default_tag: str = "div"):
    def component(props: Any = None, *children: Any, **kwargs: Any):
        p = component_props(props, children, **kwargs)
        return element(p.get("as_", default_tag), p, base_class=f"uipr-{name}")

    component.__name__ = "".join(part.title() for part in name.split("-"))
    return component


Box = _simple("box")
Card = _simple("card", "article")
CardHeader = _simple("card-header", "header")
CardBody = _simple("card-body", "div")
CardFooter = _simple("card-footer", "footer")
Navbar = _simple("navbar", "nav")
NavbarBrand = _simple("navbar-brand", "a")
NavbarContent = _simple("navbar-content")
Table = _simple("table", "table")
TableContainer = _simple("table-container")
Breadcrumb = _simple("breadcrumb", "nav")


def Container(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    size = p.get("size", "xl")
    return element(
        p.get("as_", "div"),
        p,
        base_class=cx("uipr-container", f"uipr-container-{size}"),
        internal={"size"},
    )


def Stack(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    direction = p.get("direction", "column")
    gap = str(p.get("gap", "4"))
    align = p.get("align")
    justify = p.get("justify")
    return element(
        p.get("as_", "div"),
        p,
        base_class=cx(
            "uipr-stack",
            direction in ("row", "horizontal") and "flex-row",
            direction in ("column", "vertical") and "flex-col",
            f"gap-{gap}",
            align and f"items-{align}",
            justify and f"justify-{justify}",
            p.get("wrap") and "flex-wrap",
        ),
        internal={"direction", "gap", "align", "justify", "wrap"},
    )


def Grid(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    cols = max(1, min(12, int(p.get("cols", 1))))
    gap = str(p.get("gap", "4"))
    return element(
        p.get("as_", "div"),
        p,
        base_class=cx("uipr-grid", f"grid-cols-{cols}", f"gap-{gap}"),
        internal={"cols", "gap"},
    )


def Text(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    tone = p.get("tone")
    size = p.get("size")
    weight = p.get("weight")
    return element(
        p.get("as_", "p"),
        p,
        base_class=cx(
            "uipr-text",
            tone and f"text-{tone}",
            size and f"text-{size}",
            weight and f"font-{weight}",
        ),
        internal={"tone", "size", "weight"},
    )


def Heading(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    level = max(1, min(6, int(p.get("level", 2))))
    size = p.get("size")
    return element(
        p.get("as_", f"h{level}"),
        p,
        base_class=cx("uipr-heading", size and f"text-{size}"),
        internal={"level", "size"},
    )


def Button(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    variant = p.get("variant", "primary")
    size = p.get("size", "md")
    loading = bool(p.get("loading"))
    content = children_of(p)
    if loading:
        content.insert(0, Spinner({"size": "sm", "aria-hidden": "true"}))
    button = element(
        p.get("as_", "button"),
        p,
        base_class=cx(
            "uipr-button",
            f"uipr-button-{variant}",
            f"uipr-button-{size}",
            p.get("block") and "w-full",
        ),
        internal={"variant", "size", "block"},
        children=content,
    )
    if loading:
        button.props["aria-busy"] = "true"
        button.props["disabled"] = True
    elif p.get("as_", "button") == "button" and "type" not in button.props:
        button.props["type"] = "button"
    return button


def IconButton(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    p["className"] = cx("uipr-icon-button", p.get("className"))
    if not p.get("aria-label") and p.get("label"):
        p["aria-label"] = p["label"]
    p.pop("label", None)
    return Button(p)


def Badge(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    tone = p.get("tone", "neutral")
    return element(
        p.get("as_", "span"),
        p,
        base_class=cx("uipr-badge", f"uipr-badge-{tone}", p.get("pill") and "rounded-full"),
        internal={"tone", "pill"},
    )


def Alert(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    tone = p.get("tone", "info")
    content = children_of(p)
    if p.get("title"):
        content.insert(0, h("strong", {"className": "uipr-alert-title"}, str(p["title"])))
    node = element(
        p.get("as_", "div"),
        p,
        base_class=cx("uipr-alert", f"uipr-alert-{tone}"),
        internal={"tone", "title"},
        children=content,
    )
    node.props.setdefault("role", "alert")
    return node


def Divider(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    if children_of(p):
        return h(
            "div",
            {"className": cx("uipr-divider-label", p.get("className")), "role": "separator"},
            h("span", None, *children_of(p)),
        )
    return element("hr", p, base_class="uipr-divider")


def Spinner(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    size = p.get("size", "md")
    node = element(
        "span",
        p,
        base_class=cx("uipr-spinner", f"uipr-spinner-{size}"),
        internal={"size"},
        children=[],
    )
    node.props.setdefault("role", "status")
    node.props.setdefault("aria-label", "Carregando")
    return node


def Progress(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    value = max(0.0, min(100.0, float(p.get("value", 0))))
    label = p.get("label")
    bar = h(
        "div",
        {"className": "uipr-progress-track"},
        h("div", {"className": "uipr-progress-bar", "style": {"width": f"{value:g}%"}}),
    )
    content = [h("span", {"className": "uipr-progress-label"}, str(label)), bar] if label else [bar]
    node = element(
        "div",
        p,
        base_class="uipr-progress",
        internal={"value", "label"},
        children=content,
    )
    node.props.update(
        {"role": "progressbar", "aria-valuemin": "0", "aria-valuemax": "100", "aria-valuenow": f"{value:g}"}
    )
    return node


def _field_control(kind: str, p: dict[str, Any], tag: str):
    label = p.get("label")
    help_text = p.get("help_text")
    error = p.get("error")
    control_id = p.get("id") or p.get("name")
    control = element(
        tag,
        p,
        base_class=cx("uipr-control", f"uipr-{kind}", error and "uipr-control-error"),
        internal={"label", "help_text", "error"},
        children=children_of(p) if tag in {"select", "textarea"} else [],
    )
    if error:
        control.props["aria-invalid"] = "true"
    if not any((label, help_text, error)):
        return control
    parts = []
    if label:
        parts.append(h("label", {"className": "uipr-label", "htmlFor": control_id}, str(label)))
    parts.append(control)
    if error or help_text:
        parts.append(
            h(
                "small",
                {"className": cx("uipr-field-message", error and "text-danger")},
                str(error or help_text),
            )
        )
    return h("div", {"className": "uipr-field"}, *parts)


def Input(props: Any = None, *children: Any, **kwargs: Any):
    return _field_control("input", component_props(props, children, **kwargs), "input")


def Textarea(props: Any = None, *children: Any, **kwargs: Any):
    return _field_control("textarea", component_props(props, children, **kwargs), "textarea")


def Select(props: Any = None, *children: Any, **kwargs: Any):
    return _field_control("select", component_props(props, children, **kwargs), "select")


def Checkbox(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    label = p.get("label")
    control = element(
        "input",
        {**p, "type": "checkbox"},
        base_class="uipr-checkbox",
        internal={"label", "wrapper_class"},
        children=[],
    )
    label_content = (
        [h("span", None, str(label))] if label is not None else children_of(p)
    )
    return h(
        "label",
        {"className": cx("uipr-check-label", p.get("wrapper_class"))},
        control,
        *label_content,
    )


def Switch(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    p["className"] = cx("uipr-switch-input", p.get("className"))
    label = p.get("label")
    control = element(
        "input",
        {**p, "type": "checkbox", "role": "switch"},
        internal={"label"},
        children=[],
    )
    return h(
        "label",
        {"className": "uipr-switch"},
        control,
        h("span", {"className": "uipr-switch-track"}, h("span", {"className": "uipr-switch-thumb"})),
        h("span", None, str(label)) if label else None,
    )


def Avatar(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    size = p.get("size", "md")
    src = p.get("src")
    name = str(p.get("name", ""))
    initials = p.get("initials") or "".join(part[:1] for part in name.split()[:2]).upper()
    base = cx("uipr-avatar", f"uipr-avatar-{size}")
    if src:
        return element(
            "img",
            {**p, "alt": p.get("alt", name)},
            base_class=base,
            internal={"size", "name", "initials"},
            children=[],
        )
    return element(
        "span",
        p,
        base_class=base,
        internal={"size", "src", "name", "initials", "alt"},
        children=[str(initials)],
    )


def Modal(props: Any = None, *children: Any, **kwargs: Any):
    p = component_props(props, children, **kwargs)
    if not p.get("open", False):
        return None
    title = p.get("title")
    content = []
    if title:
        content.append(h("h2", {"className": "uipr-modal-title"}, str(title)))
    content.extend(children_of(p))
    dialog = h("div", {"className": "uipr-modal", "role": "dialog", "aria-modal": "true"}, *content)
    return element(
        "div",
        p,
        base_class="uipr-modal-backdrop",
        internal={"open", "title"},
        children=[dialog],
    )
