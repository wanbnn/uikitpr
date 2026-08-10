from pyreact.server import render_to_static_markup

from uikitpr import (
    AnimatedText,
    AuroraBackground,
    BlurText,
    DotBackground,
    GradientText,
    GridBackground,
    Marquee,
    ShinyText,
    SplitText,
    SpotlightCard,
    StarBorder,
    stylesheet,
)


def render(node):
    return render_to_static_markup(node)


def test_animated_text_splits_content_without_repeating_it_for_screen_readers():
    html = render(BlurText("Crie mais rápido", delay=0.1, as_="strong"))
    assert html.startswith("<strong ")
    assert 'class="uipr-animated-text uipr-text-effect-blur"' in html
    assert '<span class="sr-only">Crie mais rápido</span>' in html
    assert html.count('aria-hidden="true"') == 3
    assert "--uipr-text-delay:0.2s" in html


def test_text_effect_shortcuts_apply_expected_variants_and_styles():
    assert "uipr-text-effect-rise" in render(SplitText("UI"))
    assert "uipr-text-effect-wave" in render(AnimatedText("Olá", effect="wave"))
    assert "--uipr-shine-duration:3s" in render(ShinyText("Pronto", duration=3))
    gradient = render(GradientText("Marca", colors=["red", "blue"]))
    assert "--uipr-gradient-colors:red, blue" in gradient


def test_backgrounds_keep_content_and_do_not_forward_visual_props():
    for component, name in (
        (AuroraBackground, "aurora"),
        (DotBackground, "dots"),
        (GridBackground, "grid"),
    ):
        html = render(component("Conteúdo", color="#ff00aa", opacity=0.4))
        assert f"uipr-background-{name}" in html
        assert "Conteúdo" in html
        assert " color=" not in html
        assert 'aria-hidden="true"' in html


def test_interactive_surfaces_render_composable_markup():
    spotlight = render(SpotlightCard("Card", spotlight="#00ffee"))
    border = render(StarBorder("Ação", speed=6))
    marquee = render(Marquee("UIKitPR", duration=12, reverse=True))
    assert "uipr-spotlight-card" in spotlight
    assert "--uipr-spotlight-color:#00ffee" in spotlight
    assert "uipr-star-border-content" in border
    assert "--uipr-star-speed:6s" in border
    assert "uipr-marquee-reverse" in marquee
    assert marquee.count("UIKitPR") == 2


def test_effect_styles_ship_inside_the_package_stylesheet():
    css = stylesheet()
    assert ".uipr-gradient-text" in css
    assert ".uipr-background-aurora" in css
    assert ".uipr-marquee-track" in css
    assert "prefers-reduced-motion" in css
