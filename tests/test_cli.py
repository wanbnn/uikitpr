from uikitpr.cli import main


def test_cli_exports_css(tmp_path):
    destination = tmp_path / "assets" / "app.css"
    assert main(["css", "-o", str(destination), "--minify"]) == 0
    assert destination.is_file()
    assert ".uipr-root" in destination.read_text(encoding="utf-8")


def test_cli_exports_motion_runtime(tmp_path):
    destination = tmp_path / "assets" / "motion.js"
    assert main(["motion", "-o", str(destination), "--minify"]) == 0
    source = destination.read_text(encoding="utf-8")
    assert "UIKitPRMotion" in source
    assert "MutationObserver" in source
