from pyreact.server import render_to_static_markup

from uikitpr import Styles, UIProvider, create_theme, stylesheet


def test_stylesheet_contains_components_utilities_and_dark_theme():
    css = stylesheet()
    assert ".uipr-button-primary" in css
    assert ".grid-cols-12" in css
    assert '[data-uipr-theme="dark"]' in css


def test_minified_stylesheet_is_smaller():
    assert len(stylesheet(minified=True)) < len(stylesheet())


def test_custom_theme_is_rendered_in_provider():
    theme = create_theme("brand", primary="#ff006e", radius="1rem")
    html = render_to_static_markup(
        UIProvider(
            "Aplicação",
            theme=theme,
            with_styles=False,
            with_motion=False,
            full_height=True,
        )
    )
    assert 'data-uipr-theme="brand"' in html
    assert "--uipr-primary:#ff006e" in html
    assert "min-h-screen" in html


def test_default_styles_are_ssr_safe_data_url():
    html = render_to_static_markup(Styles())
    assert '<link rel="stylesheet"' in html
    assert 'href="data:text/css;base64,' in html
    assert "&quot;" not in html


def test_provider_includes_motion_runtime_by_default():
    html = render_to_static_markup(UIProvider("Aplicação", with_styles=False))
    assert 'data-uipr-motion-runtime="true"' in html


def test_provider_can_include_configured_cache_runtime():
    html = render_to_static_markup(
        UIProvider(
            "Aplicação",
            with_styles=False,
            with_motion=False,
            with_cache=True,
            cache_src="/cache.js",
            cache_name="site",
            cache_version="42",
        )
    )
    assert 'data-uipr-cache-runtime="true"' in html
    assert 'data-cache-name="site"' in html
    assert 'data-version="42"' in html
