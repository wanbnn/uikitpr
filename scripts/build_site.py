"""Gera o site estático do UIKitPR usando PyReact e o próprio UIKitPR."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pyreact import h  # noqa: E402
from pyreact.server import render_to_static_markup  # noqa: E402
from uikitpr import (  # noqa: E402
    Alert,
    Avatar,
    Badge,
    BarsLoader,
    Box,
    Button,
    CacheManager,
    CachePolicy,
    CacheRuntime,
    Card,
    CardBody,
    CardFooter,
    CardHeader,
    Checkbox,
    Container,
    Grid,
    Heading,
    Input,
    Motion,
    MotionGroup,
    MotionRuntime,
    OrbitLoader,
    PulseLoader,
    Progress,
    RingLoader,
    Skeleton,
    SkeletonCard,
    Spring,
    Stack,
    Switch,
    Text,
    Textarea,
    Transition,
    WaveLoader,
    __version__ as UIKITPR_VERSION,
    cache_script,
    cx,
    motion_script,
    stylesheet,
)


def Icon(name: str, class_name: str = "icon"):
    paths = {
        "arrow": h("path", {"d": "M5 12h14M13 6l6 6-6 6"}),
        "check": h("path", {"d": "m5 12 4 4L19 6"}),
        "copy": h(
            "g",
            None,
            h("rect", {"x": "9", "y": "9", "width": "11", "height": "11", "rx": "2"}),
            h("path", {"d": "M15 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h3"}),
        ),
        "grid": h(
            "g",
            None,
            h("rect", {"x": "3", "y": "3", "width": "7", "height": "7", "rx": "1"}),
            h("rect", {"x": "14", "y": "3", "width": "7", "height": "7", "rx": "1"}),
            h("rect", {"x": "3", "y": "14", "width": "7", "height": "7", "rx": "1"}),
            h("rect", {"x": "14", "y": "14", "width": "7", "height": "7", "rx": "1"}),
        ),
        "moon": h("path", {"d": "M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z"}),
        "spark": h("path", {"d": "m12 3-1.6 5.4L5 10l5.4 1.6L12 17l1.6-5.4L19 10l-5.4-1.6L12 3Z"}),
        "terminal": h(
            "g",
            None,
            h("path", {"d": "m4 6 5 5-5 5"}),
            h("path", {"d": "M11 18h9"}),
        ),
    }
    return h(
        "svg",
        {
            "className": class_name,
            "viewBox": "0 0 24 24",
            "fill": "none",
            "stroke": "currentColor",
            "stroke-width": "1.8",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "aria-hidden": "true",
        },
        paths[name],
    )


def Logo():
    return h(
        "a",
        {"className": "site-logo", "href": "#top", "aria-label": "UIKitPR — início"},
        h(
            "span",
            {"className": "logo-mark"},
            h("span", {"className": "logo-dot logo-dot-a"}),
            h("span", {"className": "logo-dot logo-dot-b"}),
            h("span", {"className": "logo-dot logo-dot-c"}),
        ),
        h("span", None, "UIKit", h("strong", None, "PR")),
    )


def CodeBlock(command: str, label: str = "terminal"):
    return h(
        "div",
        {"className": "code-block"},
        h(
            "div",
            {"className": "code-bar"},
            h("span", None, label),
            h(
                "button",
                {
                    "className": "copy-button",
                    "type": "button",
                    "data-copy": command,
                    "aria-label": f"Copiar {command}",
                },
                Icon("copy"),
                h("span", None, "Copiar"),
            ),
        ),
        h("pre", None, h("code", None, h("span", {"className": "prompt"}, "$"), f" {command}")),
    )


def FeatureCard(icon: str, title: str, body: str, accent: str):
    return Card(
        CardBody(
            Stack(
                h("span", {"className": cx("feature-icon", accent)}, Icon(icon)),
                Heading(title, level=3, size="xl"),
                Text(body, tone="muted"),
                gap=4,
            )
        ),
        class_name="feature-card",
    )


def ComponentPreview():
    return h(
        "div",
        {"className": "preview-shell", "aria-label": "Prévia de componentes UIKitPR"},
        h(
            "div",
            {"className": "preview-toolbar"},
            h("span", {"className": "window-dots"}, h("i"), h("i"), h("i")),
            Badge("live preview", tone="success", pill=True),
        ),
        h(
            "div",
            {"className": "preview-body"},
            Stack(
                Stack(
                    Stack(
                        Avatar(name="Ana Costa", size="md"),
                        Box(
                            Heading("Olá, Ana", level=3, size="lg"),
                            Text("Seu workspace está pronto.", tone="muted", size="sm"),
                        ),
                        direction="row",
                        align="center",
                        gap=3,
                    ),
                    Badge("Pro", tone="primary", pill=True),
                    direction="row",
                    align="center",
                    justify="between",
                ),
                Grid(
                    Box(Text("Projetos", tone="muted", size="xs"), Heading("24", level=4, size="2xl"), class_name="metric-mini"),
                    Box(Text("Deploys", tone="muted", size="xs"), Heading("148", level=4, size="2xl"), class_name="metric-mini"),
                    cols=2,
                    gap=3,
                ),
                Progress(value=72, label="Meta mensal"),
                Stack(
                    Button("Novo projeto", variant="primary", size="sm"),
                    Button("Explorar", variant="outline", size="sm"),
                    direction="row",
                    gap=2,
                ),
                gap=5,
            )
        ),
        h("span", {"className": "preview-glow"}),
    )


def ComponentsSection():
    return h(
        "section",
        {"className": "section section-components", "id": "components"},
        Container(
            Stack(
                Box(
                    Badge("Biblioteca", tone="primary", pill=True),
                    Heading("Tudo para compor interfaces reais.", level=2, size="4xl", class_name="section-title"),
                    Text(
                        "Primitivas pequenas, variantes previsíveis e props que continuam sendo PyReact.",
                        tone="muted",
                        size="lg",
                        class_name="section-lead",
                    ),
                    class_name="section-heading",
                ),
                Grid(
                    Card(
                        CardHeader(
                            Stack(
                                Box(
                                    Heading("Formulário", level=3, size="xl"),
                                    Text("Estados e feedback incluídos.", tone="muted", size="sm"),
                                ),
                                Badge("Acessível", tone="success"),
                                direction="row",
                                justify="between",
                                align="start",
                            )
                        ),
                        CardBody(
                            Stack(
                                Input(label="E-mail", type="email", value="ana@empresa.dev"),
                                Textarea("Quero construir com Python.", label="Mensagem", rows="3"),
                                Stack(
                                    Checkbox(label="Receber novidades", checked=True),
                                    Switch(label="Modo avançado", checked=True),
                                    direction="row",
                                    justify="between",
                                    wrap=True,
                                ),
                                Button("Enviar mensagem", block=True),
                                gap=4,
                            )
                        ),
                        class_name="showcase-card",
                    ),
                    Stack(
                        Alert(
                            "Sua aplicação foi publicada com sucesso.",
                            tone="success",
                            title="Deploy concluído",
                        ),
                        Card(
                            CardBody(
                                Stack(
                                    Badge("Component API", tone="info", pill=True),
                                    Heading("Python por inteiro.", level=3, size="2xl"),
                                    Text(
                                        "Sem DSL paralela. Eventos, props e composição continuam familiares.",
                                        tone="muted",
                                    ),
                                    CodeBlock('Button("Publicar", variant="primary")', "componente.py"),
                                    gap=4,
                                )
                            ),
                            class_name="code-card",
                        ),
                        Grid(
                            Button("Primary", variant="primary"),
                            Button("Outline", variant="outline"),
                            Button("Ghost", variant="ghost"),
                            Button("Danger", variant="danger"),
                            cols=2,
                            gap=2,
                            class_name="button-grid",
                        ),
                        gap=4,
                    ),
                    cols=2,
                    gap=6,
                    class_name="component-grid",
                ),
                gap=10,
            )
        ),
    )


def UtilitiesSection():
    utilities = [
        ("flex", "display: flex"),
        ("items-center", "align-items: center"),
        ("gap-4", "gap: 1rem"),
        ("p-6", "padding: 1.5rem"),
        ("rounded-lg", "border-radius"),
        ("shadow", "box-shadow"),
        ("text-primary", "color: token"),
        ("md-grid-cols-3", "responsive grid"),
    ]
    return h(
        "section",
        {"className": "section section-utilities", "id": "utilities"},
        Container(
            Grid(
                Stack(
                    Badge("Utility-first", tone="info", pill=True),
                    Heading("Pense em layout. Escreva Python.", level=2, size="4xl", class_name="section-title"),
                    Text(
                        "Uma camada de utilitários inspirada no fluxo do Tailwind, pronta no wheel e sem build Node.",
                        tone="muted",
                        size="lg",
                    ),
                    CodeBlock('Box("Olá", class_name="flex items-center gap-4 p-6")', "app.py"),
                    Stack(
                        Badge("Sem Node.js", tone="success"),
                        Badge("CSS no wheel", tone="primary"),
                        Badge("Responsivo", tone="info"),
                        direction="row",
                        wrap=True,
                        gap=2,
                    ),
                    gap=5,
                    class_name="utility-copy",
                ),
                h(
                    "div",
                    {"className": "utility-board"},
                    *[
                        h(
                            "div",
                            {"className": "utility-token"},
                            h("code", None, name),
                            h("span", None, value),
                        )
                        for name, value in utilities
                    ],
                ),
                cols=2,
                gap=10,
                class_name="utility-layout",
            )
        ),
    )


def MotionSection():
    return h(
        "section",
        {"className": "section section-motion", "id": "motion"},
        Container(
            Stack(
                Box(
                    Badge(Icon("spark"), "UIKitPR Motion", tone="primary", pill=True),
                    Heading(
                        "Movimento também é parte da interface.",
                        level=2,
                        size="4xl",
                        class_name="section-title",
                    ),
                    Text(
                        "Um runtime próprio para spring physics, timelines, scroll, in-view, stagger e eventos — distribuído no mesmo wheel.",
                        tone="muted",
                        size="lg",
                        class_name="section-lead",
                    ),
                    class_name="section-heading",
                ),
                Grid(
                    Stack(
                        h(
                            "div",
                            {"className": "motion-stage"},
                            h("span", {"className": "motion-grid"}),
                            Motion(
                                h(
                                    "div",
                                    {"className": "motion-core"},
                                    h("span", {"className": "motion-core-ring"}),
                                    h("strong", None, "M"),
                                ),
                                preset="pop",
                                trigger="in-view",
                                transition=Transition(
                                    duration=0.8,
                                    spring=Spring(stiffness=155, damping=14),
                                ),
                                while_hover={"transform": "scale(1.08) rotate(5deg)"},
                                while_tap={"transform": "scale(.92)"},
                                motion_id="motion-lab-card",
                                class_name="motion-lab-target",
                            ),
                            Motion(
                                Badge("spring", tone="success", pill=True),
                                preset="slide-right",
                                trigger="in-view",
                                transition=Transition(delay=0.15),
                                class_name="motion-float-label label-a",
                            ),
                            Motion(
                                Badge("timeline", tone="info", pill=True),
                                preset="slide-left",
                                trigger="in-view",
                                transition=Transition(delay=0.25),
                                class_name="motion-float-label label-b",
                            ),
                            Motion(
                                Badge("in-view", tone="warning", pill=True),
                                preset="fade-up",
                                trigger="in-view",
                                transition=Transition(delay=0.35),
                                class_name="motion-float-label label-c",
                            ),
                            h(
                                "div",
                                {"className": "runtime-monitors"},
                                h(
                                    "div",
                                    {"className": "motion-event-monitor"},
                                    h("span", {"className": "event-light"}),
                                    h("code", {"data-motion-event": "true"}, "motion: carregando"),
                                ),
                                h(
                                    "div",
                                    {"className": "cache-event-monitor"},
                                    h("span", {"className": "event-light"}),
                                    h("code", {"data-cache-status": "true"}, "cache: verificando"),
                                ),
                            ),
                        ),
                        Stack(
                            Text("Experimente um preset", tone="muted", size="sm", weight="semibold"),
                            Stack(
                                Button("Pop", size="sm", **{"data-motion-preset": "pop"}),
                                Button("Shake", variant="outline", size="sm", **{"data-motion-preset": "shake"}),
                                Button("Flip", variant="outline", size="sm", **{"data-motion-preset": "flip"}),
                                Button("Blur", variant="ghost", size="sm", **{"data-motion-preset": "blur"}),
                                Button(
                                    "Atualizar assets",
                                    variant="ghost",
                                    size="sm",
                                    **{"data-cache-refresh": "true"},
                                ),
                                direction="row",
                                gap=2,
                                wrap=True,
                                class_name="motion-controls",
                            ),
                            gap=3,
                        ),
                        gap=4,
                    ),
                    Stack(
                        Card(
                            CardBody(
                                Stack(
                                    Badge("Declarativo", tone="info", pill=True),
                                    Heading("Motion é um VNode.", level=3, size="2xl"),
                                    Text(
                                        "Defina estado inicial, destino, trigger e física diretamente em Python.",
                                        tone="muted",
                                    ),
                                    CodeBlock(
                                        'Motion(Card(...), preset="fade-up", trigger="in-view")',
                                        "motion.py",
                                    ),
                                    Stack(
                                        Badge("mount", tone="primary"),
                                        Badge("hover", tone="success"),
                                        Badge("tap", tone="warning"),
                                        Badge("scroll", tone="info"),
                                        Badge("custom events", tone="neutral"),
                                        direction="row",
                                        gap=2,
                                        wrap=True,
                                    ),
                                    gap=4,
                                )
                            ),
                            class_name="motion-code-card",
                        ),
                        Grid(
                            Box(
                                Heading("60", level=3, size="3xl"),
                                Text("amostras spring", tone="muted", size="xs"),
                                class_name="motion-stat",
                            ),
                            Box(
                                Heading("0", level=3, size="3xl"),
                                Text("dependências JS", tone="muted", size="xs"),
                                class_name="motion-stat",
                            ),
                            cols=2,
                            gap=3,
                        ),
                        gap=4,
                    ),
                    cols=2,
                    gap=7,
                    class_name="motion-layout",
                ),
                Box(
                    Stack(
                        Box(
                            Heading("Loaders & estados", level=3, size="2xl"),
                            Text(
                                "Feedback visual pronto para qualquer contexto.",
                                tone="muted",
                            ),
                        ),
                        Badge("reduced-motion ready", tone="success", pill=True),
                        direction="row",
                        justify="between",
                        align="start",
                    ),
                    MotionGroup(
                        Box(OrbitLoader(size="lg"), Text("Orbit", tone="muted", size="sm"), class_name="loader-demo"),
                        Box(RingLoader(size="lg", tone="info"), Text("Ring", tone="muted", size="sm"), class_name="loader-demo"),
                        Box(BarsLoader(size="lg", tone="success"), Text("Bars", tone="muted", size="sm"), class_name="loader-demo"),
                        Box(PulseLoader(size="lg", tone="danger"), Text("Pulse", tone="muted", size="sm"), class_name="loader-demo"),
                        Box(WaveLoader(size="lg", tone="warning"), Text("Wave", tone="muted", size="sm"), class_name="loader-demo"),
                        SkeletonCard(class_name="loader-skeleton-card"),
                        preset="fade-up",
                        stagger=0.08,
                        class_name="loader-gallery",
                    ),
                    class_name="loader-panel",
                ),
                gap=10,
            )
        ),
    )


def ThemeSection():
    return h(
        "section",
        {"className": "section", "id": "themes"},
        Container(
            Grid(
                h(
                    "div",
                    {"className": "theme-visual"},
                    h("span", {"className": "orb orb-a"}),
                    h("span", {"className": "orb orb-b"}),
                    Card(
                        CardBody(
                            Stack(
                                Stack(
                                    h("span", {"className": "theme-swatch swatch-primary"}),
                                    h("span", {"className": "theme-swatch swatch-success"}),
                                    h("span", {"className": "theme-swatch swatch-danger"}),
                                    direction="row",
                                    gap=2,
                                ),
                                Heading("Sua marca, seus tokens.", level=3, size="2xl"),
                                Text("CSS variables deixam o sistema consistente.", tone="muted"),
                                Progress(value=84, label="Cobertura do design system"),
                                gap=4,
                            )
                        ),
                        class_name="theme-card",
                    ),
                ),
                Stack(
                    Badge("Theming", tone="warning", pill=True),
                    Heading("Claro, escuro ou totalmente seu.", level=2, size="4xl", class_name="section-title"),
                    Text(
                        "Troque o modo de cor em runtime ou declare tokens de marca em Python. O SSR entrega a primeira pintura pronta.",
                        tone="muted",
                        size="lg",
                    ),
                    h(
                        "ul",
                        {"className": "check-list"},
                        h("li", None, Icon("check"), "Tokens semânticos por CSS variables"),
                        h("li", None, Icon("check"), "Dark mode com um atributo"),
                        h("li", None, Icon("check"), "Stylesheet externo compatível com CSP"),
                    ),
                    Button(
                        Icon("moon"),
                        h("span", {"data-theme-label": "true"}, "Testar modo escuro"),
                        variant="outline",
                        class_name="theme-demo-button",
                        **{"data-theme-toggle": "true"},
                    ),
                    gap=5,
                ),
                cols=2,
                gap=10,
                class_name="theme-layout",
            )
        ),
    )


def App(asset_urls: dict[str, str], cache_version: str):
    return h(
        "div",
        {"className": "uipr-root site-root", "data-uipr-theme": "light", "data-uipr-color-mode": "light", "id": "top"},
        h(
            "header",
            {"className": "site-header"},
            Container(
                Logo(),
                h(
                    "nav",
                    {"className": "site-nav", "aria-label": "Navegação principal"},
                    h("a", {"href": "#features"}, "Recursos"),
                    h("a", {"href": "#components"}, "Componentes"),
                    h("a", {"href": "#motion"}, "Motion"),
                    h("a", {"href": "#utilities"}, "Utilitários"),
                    h("a", {"href": "#themes"}, "Temas"),
                ),
                Stack(
                    Button(
                        Icon("moon"),
                        variant="ghost",
                        size="sm",
                        class_name="header-theme",
                        **{"aria-label": "Alternar tema", "data-theme-toggle": "true"},
                    ),
                    Button(
                        "GitHub",
                        Icon("arrow"),
                        variant="outline",
                        size="sm",
                        as_="a",
                        href="https://github.com/wanbnn/uikitpr",
                    ),
                    direction="row",
                    gap=2,
                    align="center",
                    class_name="header-actions",
                ),
                class_name="header-inner",
            ),
        ),
        h(
            "main",
            None,
            h(
                "section",
                {"className": "hero"},
                h("span", {"className": "hero-grid"}),
                h("span", {"className": "hero-orb hero-orb-a"}),
                h("span", {"className": "hero-orb hero-orb-b"}),
                Container(
                    Grid(
                        Stack(
                            Badge(Icon("spark"), "Framework visual para PyReact", tone="primary", pill=True, class_name="hero-badge"),
                            Heading(
                                "Interfaces bonitas.",
                                h("span", {"className": "gradient-text"}, "Python de verdade."),
                                level=1,
                                class_name="hero-title",
                            ),
                            Text(
                                "A velocidade de um framework utility-first, a consistência de um design system e a simplicidade do ecossistema PyReact.",
                                tone="muted",
                                class_name="hero-lead",
                            ),
                            Stack(
                                Button(
                                    "Começar agora",
                                    Icon("arrow"),
                                    size="lg",
                                    as_="a",
                                    href="#install",
                                    class_name="hero-primary",
                                ),
                                Button(
                                    "Ver componentes",
                                    variant="outline",
                                    size="lg",
                                    as_="a",
                                    href="#components",
                                ),
                                direction="row",
                                gap=3,
                                wrap=True,
                            ),
                            CodeBlock("prpm add uikitpr"),
                            Stack(
                                Text("MIT", tone="muted", size="sm"),
                                Text("Python 3.9+", tone="muted", size="sm"),
                                Text("PyReact 1.0.5+", tone="muted", size="sm"),
                                direction="row",
                                gap=4,
                                wrap=True,
                                class_name="hero-meta",
                            ),
                            gap=6,
                            class_name="hero-copy",
                        ),
                        ComponentPreview(),
                        cols=2,
                        gap=10,
                        class_name="hero-layout",
                    )
                ),
            ),
            h(
                "section",
                {"className": "trust-strip", "aria-label": "Características principais"},
                Container(
                    h("span", None, "Feito para o ecossistema"),
                    h("strong", None, "PyReact"),
                    h("i"),
                    h("strong", None, "PRPM"),
                    h("i"),
                    h("strong", None, "SSR"),
                    h("i"),
                    h("strong", None, "GitHub Pages"),
                    class_name="trust-inner",
                ),
            ),
            h(
                "section",
                {"className": "section", "id": "features"},
                Container(
                    Stack(
                        Box(
                            Badge("Por que UIKitPR?", tone="primary", pill=True),
                            Heading("Uma fundação visual, não uma caixa-preta.", level=2, size="4xl", class_name="section-title"),
                            Text(
                                "Você mantém o controle do VNode, do CSS e da experiência.",
                                tone="muted",
                                size="lg",
                            ),
                            class_name="section-heading",
                        ),
                        Grid(
                            FeatureCard("grid", "Composição direta", "Componentes são funções Python que retornam VNodes PyReact.", "accent-purple"),
                            FeatureCard("terminal", "Zero toolchain JS", "Instale, construa e publique usando apenas Python e PRPM.", "accent-blue"),
                            FeatureCard("check", "Acessível por padrão", "Estados, foco e semântica ARIA fazem parte das primitivas.", "accent-green"),
                            cols=3,
                            gap=5,
                            class_name="feature-grid",
                        ),
                        gap=10,
                    )
                ),
            ),
            ComponentsSection(),
            MotionSection(),
            UtilitiesSection(),
            ThemeSection(),
            h(
                "section",
                {"className": "section install-section", "id": "install"},
                Container(
                    h(
                        "div",
                        {"className": "install-panel"},
                        h("span", {"className": "install-grid"}),
                        Grid(
                            Stack(
                                Badge("Comece em segundos", tone="success", pill=True),
                                Heading("Do PRPM ao primeiro componente.", level=2, size="4xl", class_name="section-title"),
                                Text(
                                    "Adicione a dependência, importe as primitivas e deixe o UIKitPR cuidar da camada visual.",
                                    tone="muted",
                                    size="lg",
                                ),
                                Stack(
                                    Button("Abrir no PyPI", as_="a", href="https://pypi.org/project/uikitpr/", size="lg"),
                                    Button("Ler o README", as_="a", href="https://github.com/wanbnn/uikitpr#readme", variant="outline", size="lg"),
                                    direction="row",
                                    gap=3,
                                    wrap=True,
                                ),
                                gap=5,
                            ),
                            Stack(
                                CodeBlock("prpm add uikitpr", "1 · instalar"),
                                CodeBlock("from uikitpr import Button, UIProvider", "2 · importar"),
                                CodeBlock('UIProvider(Button("Olá, PyReact!"))', "3 · criar"),
                                gap=3,
                            ),
                            cols=2,
                            gap=8,
                            class_name="install-layout",
                        ),
                    )
                ),
            ),
        ),
        h(
            "footer",
            {"className": "site-footer"},
            Container(
                Stack(
                    Logo(),
                    Text("Framework visual utility-first para PyReact.", tone="muted", size="sm"),
                    gap=2,
                ),
                Stack(
                    h("a", {"href": "https://github.com/wanbnn/uikitpr"}, "GitHub"),
                    h("a", {"href": "https://pypi.org/project/uikitpr/"}, "PyPI"),
                    h("a", {"href": "https://github.com/wanbnn/pyreact"}, "PyReact"),
                    direction="row",
                    gap=5,
                ),
                Text("MIT · 2026", tone="muted", size="sm"),
                class_name="footer-inner",
            ),
        ),
        h("div", {"className": "toast", "role": "status", "aria-live": "polite"}),
        MotionRuntime(src=asset_urls["uikitpr-motion.js"]),
        CacheRuntime(
            src=asset_urls["uikitpr-cache.js"],
            service_worker="sw.js",
            manifest="asset-manifest.json",
            version=cache_version,
            cache_name="uikitpr-site",
        ),
        h("script", {"src": asset_urls["app.js"], "defer": True}),
    )


def Document(asset_urls: dict[str, str], cache_version: str):
    return h(
        "html",
        {"lang": "pt-BR"},
        h(
            "head",
            None,
            h("meta", {"charset": "utf-8"}),
            h("meta", {"name": "viewport", "content": "width=device-width, initial-scale=1"}),
            h("meta", {"name": "theme-color", "content": "#0d0b16"}),
            h("meta", {"name": "uikitpr-cache-version", "content": cache_version}),
            h(
                "meta",
                {
                    "name": "description",
                    "content": "UIKitPR é o framework visual utility-first feito para aplicações PyReact.",
                },
            ),
            h("title", None, "UIKitPR — Framework visual para PyReact"),
            h("link", {"rel": "preconnect", "href": "https://fonts.googleapis.com"}),
            h("link", {"rel": "preconnect", "href": "https://fonts.gstatic.com", "crossorigin": ""}),
            h(
                "link",
                {
                    "href": "https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter+Tight:wght@400;500;600;700;800&display=swap",
                    "rel": "stylesheet",
                },
            ),
            h("link", {"rel": "stylesheet", "href": asset_urls["uikitpr.css"]}),
            h("link", {"rel": "stylesheet", "href": asset_urls["site.css"]}),
        ),
        h("body", None, App(asset_urls, cache_version)),
    )


def build(output: Path) -> Path:
    output = output.resolve()
    cache = CacheManager(
        output,
        policy=CachePolicy(
            name="uikitpr-site",
            version=UIKITPR_VERSION,
            strategy="cache-first",
            navigation_strategy="network-first",
        ),
    )
    cache.add_text("uikitpr.css", stylesheet(), content_type="text/css")
    cache.add_text(
        "uikitpr-motion.js",
        motion_script(),
        content_type="text/javascript",
    )
    cache.add_text(
        "uikitpr-cache.js",
        cache_script(),
        content_type="text/javascript",
    )
    cache.add_file("site.css", ROOT / "site" / "assets" / "site.css")
    cache.add_file("app.js", ROOT / "site" / "assets" / "app.js")
    asset_urls = {name: asset.path for name, asset in cache.assets.items()}
    (output / "index.html").write_text(
        "<!doctype html>\n"
        + render_to_static_markup(Document(asset_urls, UIKITPR_VERSION)),
        encoding="utf-8",
    )
    cache.finalize(precache=["./"])
    (output / ".nojekyll").write_text("", encoding="utf-8")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera o site estático do UIKitPR.")
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args(argv)
    destination = build(args.output)
    print(f"Site gerado em {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
