import importlib.util
import json
from pathlib import Path
import re


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
    assert re.search(r'href="assets/uikitpr\.[a-f0-9]{12}\.css"', html)
    assert re.search(r'src="assets/uikitpr-motion\.[a-f0-9]{12}\.js"', html)
    assert re.search(r'src="assets/uikitpr-cache\.[a-f0-9]{12}\.js"', html)
    assert re.search(r'src="assets/app\.[a-f0-9]{12}\.js"', html)
    assert html.count("data-uipr-motion-control=") == 4
    assert "data-motion-preset" not in html
    assert "prpm add uikitpr" in html
    manifest = json.loads(
        (output / "asset-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["cache"]["id"] == "uikitpr-site-0.3.2"
    assert "loop ambiente · carregando" in html
    assert (output / manifest["assets"]["uikitpr.css"]["path"]).stat().st_size > 10_000
    assert (output / manifest["assets"]["site.css"]["path"]).is_file()
    site_css = (output / manifest["assets"]["site.css"]["path"]).read_text(
        encoding="utf-8"
    )
    assert "@keyframes motion-core-idle" in site_css
    app_js = (output / manifest["assets"]["app.js"]["path"]).read_text(
        encoding="utf-8"
    )
    assert "event.detail.preset" in app_js
    assert "loop ambiente" in app_js
    assert (output / manifest["assets"]["uikitpr-motion.js"]["path"]).stat().st_size > 10_000
    assert (output / "sw.js").is_file()
    assert "network-first" in (output / "sw.js").read_text(encoding="utf-8")
    assert (output / ".nojekyll").is_file()
