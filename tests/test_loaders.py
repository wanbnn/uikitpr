from pyreact.server import render_to_static_markup

from uikitpr import (
    BarsLoader,
    DotsLoader,
    OrbitLoader,
    PageLoader,
    PulseLoader,
    RingLoader,
    Skeleton,
    SkeletonCard,
    WaveLoader,
)


def test_all_loaders_have_status_semantics_and_parts():
    loaders = [
        (DotsLoader, 3),
        (BarsLoader, 5),
        (RingLoader, 1),
        (PulseLoader, 2),
        (OrbitLoader, 3),
        (WaveLoader, 5),
    ]
    for loader, part_count in loaders:
        node = loader(size="lg", tone="success")
        assert node.props["role"] == "status"
        assert node.props["aria-label"] == "Carregando"
        assert len(node.children) == part_count
        assert "uipr-loader-lg" in node.props["className"]


def test_skeleton_variants_and_page_loader_render():
    lines = Skeleton(lines=3)
    assert len(lines.children) == 3
    assert "uipr-skeleton-short" in lines.children[-1].props["className"]

    html = render_to_static_markup(SkeletonCard())
    assert "uipr-skeleton-card" in html
    assert 'aria-hidden="true"' in html

    page = PageLoader(loader="wave", label="Preparando interface", overlay=False)
    page_html = render_to_static_markup(page)
    assert "uipr-wave-loader" in page_html
    assert "Preparando interface" in page_html
    assert "uipr-page-loader-overlay" not in page_html

