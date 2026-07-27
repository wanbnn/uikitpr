"""Dashboard SSR demonstrando componentes e utilitários UIKitPR."""

from pyreact import h
from pyreact.server import render_to_static_markup

from uikitpr import (
    Avatar,
    Badge,
    Button,
    Card,
    CardBody,
    Container,
    Grid,
    Heading,
    Navbar,
    NavbarBrand,
    NavbarContent,
    Progress,
    Stack,
    Text,
    UIProvider,
)


def Metric(title, value, change):
    return Card(
        CardBody(
            Stack(
                Text(title, tone="muted", size="sm"),
                Heading(value, level=3, size="2xl"),
                Badge(change, tone="success"),
                gap=2,
            )
        )
    )


def App(props=None):
    navigation = Navbar(
        NavbarBrand("UIKitPR", href="/"),
        NavbarContent(
            Button("Documentação", variant="ghost", as_="a", href="/docs"),
            Avatar(name="Py React", size="sm"),
        ),
    )
    content = Container(
        Stack(
            Stack(
                Heading("Visão geral", level=1, size="3xl"),
                Text("Componentes PyReact com uma camada visual consistente.", tone="muted"),
                gap=2,
            ),
            Grid(
                Metric("Receita", "R$ 48.250", "+12,4%"),
                Metric("Clientes", "1.842", "+8,1%"),
                Metric("Conversão", "6,7%", "+1,3%"),
                cols=3,
                gap=4,
                class_name="md-grid-cols-3",
            ),
            Card(
                CardBody(
                    Stack(
                        Heading("Meta mensal", level=2, size="xl"),
                        Progress(value=72, label="72% alcançado"),
                        gap=4,
                    )
                )
            ),
            gap=6,
            class_name="py-6",
        )
    )
    return UIProvider(navigation, content, full_height=True)


if __name__ == "__main__":
    print(render_to_static_markup(h(App, None)))

