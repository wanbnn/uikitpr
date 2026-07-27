"""Primitivas compartilhadas pelo UIKitPR."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from pyreact import h

_EMPTY = (None, False, "")


def cx(*values: Any) -> str:
    """Combina classes de forma condicional, no estilo clsx/classnames."""
    classes: list[str] = []
    for value in values:
        if value in _EMPTY:
            continue
        if isinstance(value, str):
            classes.extend(value.split())
        elif isinstance(value, Mapping):
            classes.extend(str(name) for name, enabled in value.items() if enabled)
        elif isinstance(value, Iterable):
            classes.extend(cx(*value).split())
        else:
            classes.append(str(value))
    return " ".join(dict.fromkeys(classes))


def component_props(
    props: Any = None, children: tuple[Any, ...] = (), **kwargs: Any
) -> dict[str, Any]:
    """Normaliza uso direto e uso via ``h(Component, props)``."""
    if isinstance(props, Mapping):
        result = dict(props)
    else:
        result = {}
        if props is not None:
            children = (props, *children)
    result.update(kwargs)
    if children:
        result["children"] = list(children) if len(children) > 1 else children[0]
    return result


def children_of(props: Mapping[str, Any]) -> list[Any]:
    children = props.get("children", [])
    if children is None:
        return []
    if isinstance(children, (list, tuple)):
        return list(children)
    return [children]


def dom_props(
    props: Mapping[str, Any],
    *,
    base_class: str = "",
    internal: Iterable[str] = (),
) -> dict[str, Any]:
    """Remove propriedades internas e prepara atributos para o DOM PyReact."""
    hidden = {
        "children",
        "as_",
        "class_name",
        "class_",
        "loading",
        *internal,
    }
    result = {key: value for key, value in props.items() if key not in hidden}
    extra_class = (
        props.get("className") or props.get("class_name") or props.get("class_") or ""
    )
    result["className"] = cx(base_class, extra_class)
    if not result["className"]:
        result.pop("className")
    return result


def element(
    tag: str,
    props: Mapping[str, Any],
    *,
    base_class: str = "",
    internal: Iterable[str] = (),
    children: list[Any] | None = None,
):
    return h(
        tag,
        dom_props(props, base_class=base_class, internal=internal),
        *(children if children is not None else children_of(props)),
    )


def utility(*classes: Any) -> str:
    """Alias semântico de :func:`cx` para montar utilitários UIKitPR."""
    return cx(*classes)

