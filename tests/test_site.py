import importlib.util
from pathlib import Path


def load_builder():
    path = Path(__file__).parents[1] / "scripts" / "build_site.py"
    spec = importlib.util.spec_from_file_location("uikitpr_build_site", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_static_site_build(tmp_path):
    builder = load_builder()
    output = builder.build(tmp_path / "public")
    html = (output / "index.html").read_text(encoding="utf-8")

    assert html.startswith("<!doctype html>")
    assert "UIKitPR — Framework visual para PyReact" in html
    assert 'href="assets/uikitpr.css"' in html
    assert 'src="assets/app.js"' in html
    assert "prpm add uikitpr" in html
    assert (output / "assets" / "uikitpr.css").stat().st_size > 10_000
    assert (output / "assets" / "site.css").is_file()
    assert (output / ".nojekyll").is_file()

