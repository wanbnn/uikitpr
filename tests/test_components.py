from pyreact import h
from pyreact.server import render_to_static_markup

from uikitpr import (
    Alert,
    Avatar,
    Button,
    Checkbox,
    Grid,
    Input,
    Modal,
    Progress,
    Stack,
)


def render(node):
    return render_to_static_markup(node)


def test_button_direct_api_has_variant_type_and_child():
    html = render(Button("Salvar", variant="primary", class_name="meu-botao"))
    assert 'class="uipr-button uipr-button-primary uipr-button-md meu-botao"' in html
    assert 'type="button"' in html
    assert ">Salvar</button>" in html


def test_button_works_as_pyreact_component_with_children_prop():
    html = render(h(Button, {"variant": "outline"}, "Continuar"))
    assert "uipr-button-outline" in html
    assert "Continuar" in html


def test_loading_button_is_accessible():
    node = Button("Enviando", loading=True)
    assert node.props["disabled"] is True
    assert node.props["aria-busy"] == "true"
    assert node.children[0].props["role"] == "status"


def test_layout_primitives_generate_utility_classes():
    stack = Stack("conteúdo", direction="row", gap=6, align="center")
    grid = Grid("conteúdo", cols=3, gap=2)
    assert stack.props["className"] == "uipr-stack flex-row gap-6 items-center"
    assert grid.props["className"] == "uipr-grid grid-cols-3 gap-2"


def test_alert_and_progress_expose_semantics():
    alert = Alert("Tudo certo", tone="success", title="Sucesso")
    progress = Progress(value=42, label="Upload")
    assert alert.props["role"] == "alert"
    assert progress.props["role"] == "progressbar"
    assert progress.props["aria-valuenow"] == "42"


def test_fields_do_not_forward_internal_props():
    html = render(Input(label="E-mail", help_text="Nunca compartilhamos.", name="email"))
    assert "<label" in html and "E-mail" in html
    assert "help_text=" not in html
    assert 'name="email"' in html


def test_checkbox_and_avatar_fallback():
    checkbox = render(Checkbox(label="Aceito", name="terms"))
    avatar = render(Avatar(name="Maria Silva"))
    assert 'type="checkbox"' in checkbox
    assert "Aceito" in checkbox
    assert ">MS</span>" in avatar


def test_closed_modal_renders_nothing_and_open_modal_is_dialog():
    assert Modal("conteúdo") is None
    html = render(Modal("conteúdo", open=True, title="Detalhes"))
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html
