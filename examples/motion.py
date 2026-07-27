"""Exemplo do motor UIKitPR Motion com SSR PyReact."""

from pyreact.server import render_to_static_markup

from uikitpr import (
    Button,
    Card,
    CardBody,
    Heading,
    Motion,
    MotionGroup,
    OrbitLoader,
    Spring,
    Stack,
    Text,
    Transition,
    UIProvider,
)


def App():
    cards = MotionGroup(
        *[
            Card(
                CardBody(
                    Stack(
                        Heading(f"Card {index}", level=2),
                        Text("Entrada coordenada por stagger.", tone="muted"),
                        gap=3,
                    )
                )
            )
            for index in range(1, 4)
        ],
        preset="fade-up",
        stagger=0.1,
    )
    hero = Motion(
        Stack(
            OrbitLoader(size="lg"),
            Heading("UIKitPR Motion", level=1),
            Text("Spring physics e eventos sem dependências.", tone="muted"),
            Button("Interaja", variant="primary"),
            gap=4,
        ),
        preset="pop",
        transition=Transition(
            duration=0.8,
            spring=Spring(stiffness=160, damping=16),
        ),
        while_hover={"transform": "translateY(-6px) scale(1.02)"},
        while_tap={"transform": "scale(.97)"},
    )
    return UIProvider(Stack(hero, cards, gap=8, class_name="p-8"))


if __name__ == "__main__":
    print(render_to_static_markup(App()))

