from pyreact.server import render_to_static_markup

import uikitpr.cache as cache_module
import uikitpr.creative as creative_module
import uikitpr.motion as motion_module
import uikitpr.theme as theme_module


def test_stylesheet_data_url_is_materialized_once_per_variant():
    theme_module.stylesheet.cache_clear()
    theme_module.stylesheet_data_url.cache_clear()

    first = theme_module.stylesheet_data_url(minified=True)
    second = theme_module.stylesheet_data_url(minified=True)

    assert first == second
    info = theme_module.stylesheet_data_url.cache_info()
    assert info.misses == 1
    assert info.hits == 1
    assert theme_module.stylesheet.cache_info().misses == 1


def test_provider_reuses_embedded_runtime_payloads_across_renders(monkeypatch):
    calls = {"motion": 0, "creative": 0, "cache": 0}

    def fake_motion(*, minified=False):
        calls["motion"] += 1
        return f"motion:{minified}"

    def fake_creative(*, minified=False):
        calls["creative"] += 1
        return f"creative:{minified}"

    def fake_cache(*, minified=False):
        calls["cache"] += 1
        return f"cache:{minified}"

    monkeypatch.setattr(motion_module, "motion_script", fake_motion)
    monkeypatch.setattr(creative_module, "creative_script", fake_creative)
    monkeypatch.setattr(cache_module, "cache_script", fake_cache)
    theme_module._runtime_data_url.cache_clear()

    props = {
        "with_styles": False,
        "with_cache": True,
        "minified": True,
    }
    first = render_to_static_markup(theme_module.UIProvider("App", **props))
    second = render_to_static_markup(theme_module.UIProvider("App", **props))

    assert first == second
    assert calls == {"motion": 1, "creative": 1, "cache": 1}
    info = theme_module._runtime_data_url.cache_info()
    assert info.misses == 3
    assert info.hits == 3


def test_external_runtime_sources_do_not_materialize_embedded_assets(monkeypatch):
    theme_module._runtime_data_url.cache_clear()

    def unexpected(*args, **kwargs):
        raise AssertionError("embedded runtime should not be materialized")

    monkeypatch.setattr(theme_module, "_runtime_data_url", unexpected)
    html = render_to_static_markup(
        theme_module.UIProvider(
            "App",
            with_styles=False,
            motion_src="/motion.js",
            creative_src="/creative.js",
            with_cache=True,
            cache_src="/cache.js",
        )
    )

    assert 'src="/motion.js"' in html
    assert 'src="/creative.js"' in html
    assert 'src="/cache.js"' in html
