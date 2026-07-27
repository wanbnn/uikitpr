from uikitpr.cli import main


def test_cli_exports_css(tmp_path):
    destination = tmp_path / "assets" / "app.css"
    assert main(["css", "-o", str(destination), "--minify"]) == 0
    assert destination.is_file()
    assert ".uipr-root" in destination.read_text(encoding="utf-8")

