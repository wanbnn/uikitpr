from collections import Counter

from pyreact.server import render_to_static_markup

import uikitpr
from uikitpr import CreativeRuntime, creative, creative_script


def test_catalog_has_the_frozen_135_component_baseline():
    counts = Counter(item.category for item in uikitpr.CREATIVE_CATALOG)
    assert counts == {
        "text": 22,
        "animation": 28,
        "component": 38,
        "background": 47,
    }
    assert len(uikitpr.CREATIVE_CATALOG) == 135
    assert len({(item.category, item.name) for item in uikitpr.CREATIVE_CATALOG}) == 135


def test_every_catalog_entry_is_callable_and_renders():
    for item in uikitpr.CREATIVE_CATALOG:
        component = getattr(creative, item.name)
        kwargs = {"items": ["One", "Two"]} if item.category == "component" else {}
        html = render_to_static_markup(component("Preview", **kwargs))
        assert html
        assert item.slug in html or item.name in html or "uipr-" in html


def test_catalog_names_are_exported_and_stack_conflict_is_explicit():
    for item in uikitpr.CREATIVE_CATALOG:
        if item.name != "Stack":
            assert hasattr(uikitpr, item.name), item.name
    assert uikitpr.CreativeStack is creative.Stack
    assert uikitpr.Stack is not uikitpr.CreativeStack


def test_shared_runtime_is_ssr_safe_and_packaged():
    source = creative_script()
    assert "window.UIKitPRCreative" in source
    assert "MutationObserver" in source
    assert "ResizeObserver" in source
    html = render_to_static_markup(CreativeRuntime())
    assert 'data-uipr-creative-runtime="true"' in html
    assert "data:text/javascript;base64," in html
