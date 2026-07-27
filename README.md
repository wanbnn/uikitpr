<div align="center">

# UIKitPR

### O framework visual utility-first feito para PyReact.

[![PyPI](https://img.shields.io/pypi/v/uikitpr?logo=pypi&logoColor=white)](https://pypi.org/project/uikitpr/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyReact](https://img.shields.io/badge/PyReact-1.0.5%2B-6D4AFF)](https://github.com/wanbnn/pyreact)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Componentes acessíveis, temas, classes utilitárias e um motor próprio de
motion em um pacote Python, sem pipeline Node obrigatório.

**Site:** <https://wanbnn.github.io/uikitpr/>

</div>

## Por que UIKitPR?

Tailwind é excelente para compor layouts e Bootstrap acelera componentes
comuns. O UIKitPR leva as duas ideias ao ecossistema PyReact:

- classes utilitárias previsíveis (`flex`, `gap-4`, `grid-cols-3`, `p-6`);
- componentes Python que retornam VNodes PyReact;
- temas claro, escuro e customizados por CSS variables;
- SSR, handlers e propriedades compatíveis com `h()` do PyReact;
- CSS incluído no wheel e exportável pela CLI;
- motion com spring, timelines, stagger, scroll, eventos e lifecycle;
- cache web com fingerprint, manifesto, atualização e Service Worker;
- loaders, skeletons e estados visuais prontos;
- nenhuma dependência JavaScript ou etapa de compilação.

## Instalação com PRPM

```bash
prpm add uikitpr
```

Também é possível instalar com `pip install uikitpr`.

## Início rápido

```python
from pyreact import h
from uikitpr import Button, Card, CardBody, Heading, Stack, UIProvider


def App(props):
    return UIProvider(
        Card(
            CardBody(
                Stack(
                    Heading("Olá, PyReact!", level=1),
                    Button("Começar", variant="primary", onClick=lambda: print("oi")),
                    gap=4,
                )
            )
        ),
        class_name="p-6",
        full_height=True,
    )
```

Os componentes aceitam filhos diretamente, como acima, ou através de
`h(Component, {"children": ...})`:

```python
h(Button, {"children": "Salvar", "variant": "outline"})
```

Essa forma explícita em `props` é importante na versão atual do PyReact, cujo
renderer não transfere automaticamente os filhos de `h(Component, props, *children)`
para componentes funcionais.

## Utilitários

Use classes diretamente em `className` ou `class_name`:

```python
from uikitpr import Box, cx

Box(
    "Conteúdo",
    class_name=cx(
        "flex items-center gap-4 p-6 rounded shadow",
        {"bg-primary-soft": destaque, "hidden": not visivel},
    ),
)
```

O CSS inclui layout flex/grid, espaçamento, sizing, tipografia, cores,
bordas, sombras e variantes responsivas sem caracteres especiais, como
`md-grid-cols-3` e `lg-grid-cols-4`.

## Componentes

| Grupo | Componentes |
| --- | --- |
| Layout | `Box`, `Container`, `Stack`, `Grid`, `Divider` |
| Tipografia | `Heading`, `Text`, `Badge` |
| Ações | `Button`, `IconButton` |
| Formulários | `Input`, `Textarea`, `Select`, `Checkbox`, `Switch` |
| Feedback | `Alert`, `Spinner`, `Progress`, `Modal` |
| Dados e navegação | `Card`, `Table`, `Navbar`, `Breadcrumb`, `Avatar` |

Variantes mais usadas:

```python
Button("Primário", variant="primary")
Button("Contorno", variant="outline", size="lg")
Badge("Ativo", tone="success", pill=True)
Alert("Confira os dados.", tone="warning", title="Atenção")
Input(label="E-mail", name="email", type="email", help_text="Seu acesso.")
```

Propriedades não consumidas pelo componente são encaminhadas ao VNode DOM,
incluindo `onClick`, `aria-*`, `data-*`, `style`, `id` e `name`.

## Temas

`UIProvider` inclui o CSS e configura o tema:

```python
UIProvider(AppContent(), theme="dark", full_height=True)
```

Crie uma marca usando tokens:

```python
from uikitpr import create_theme

brand = create_theme(
    "minha-marca",
    primary="#ff006e",
    primary_hover="#d9005d",
    radius="1rem",
)

UIProvider(AppContent(), theme=brand)
```

## Motion, animações e eventos

`UIProvider` inclui o runtime UIKitPR Motion por padrão:

```python
from uikitpr import Motion, Spring, Transition

Motion(
    Card(...),
    preset="fade-up",
    trigger="in-view",
    while_hover={"transform": "translateY(-6px) scale(1.02)"},
    while_tap={"transform": "scale(.97)"},
    transition=Transition(
        duration=.7,
        spring=Spring(stiffness=170, damping=18),
    ),
)
```

O motor oferece:

- animações de mount, in-view, click, hover, tap, focus e scroll;
- presets, keyframes customizados e spring physics;
- `MotionGroup` com stagger e `MotionTimeline` para orchestration;
- lifecycle via eventos `uipr:motion:*`;
- API imperativa `window.UIKitPRMotion`;
- MutationObserver para VNodes adicionados dinamicamente;
- suporte a `prefers-reduced-motion`.

Consulte [docs/MOTION.md](docs/MOTION.md) para a API completa.

## Cache web e deploy sem assets antigos

O `CacheManager` escreve assets com fingerprint SHA-256, um manifesto
inspecionável e um Service Worker versionado. Assim, cada alteração ganha uma
URL nova e versões antigas são removidas na ativação:

```python
from pathlib import Path
from uikitpr import CacheManager, CachePolicy, cache_script, motion_script, stylesheet

cache = CacheManager(
    Path("public"),
    policy=CachePolicy(name="my-app", version="2026.07.27"),
)
css = cache.add_text("uikitpr.css", stylesheet())
motion = cache.add_text("uikitpr-motion.js", motion_script())
runtime = cache.add_text("uikitpr-cache.js", cache_script())
cache.finalize(precache=["./"])

print(css.path, motion.path, runtime.path)
```

Para registrar o Service Worker em uma árvore PyReact:

```python
from uikitpr import CacheRuntime

CacheRuntime(
    src="/assets/uikitpr-cache.js",
    service_worker="/sw.js",
    manifest="/asset-manifest.json",
    version="2026.07.27",
    cache_name="my-app",
)
```

O cliente expõe `window.UIKitPRCache.register()`, `refresh()`, `manifest()`,
`status()` e `clear()`. Consulte [docs/CACHE.md](docs/CACHE.md).

## Loaders e estados visuais

```python
from uikitpr import OrbitLoader, Skeleton, SkeletonCard

OrbitLoader(size="lg")
Skeleton(lines=3)
SkeletonCard()
```

Também estão disponíveis `DotsLoader`, `BarsLoader`, `RingLoader`,
`PulseLoader`, `WaveLoader` e `PageLoader`.

## CSS externo e CSP

Por padrão, `UIProvider` inclui um `<link>` com o stylesheet em uma `data: URL`.
Esse formato evita o escaping aplicado pelo SSR do PyReact a filhos de
`<style>`. Para produção com CSP estrita, exporte e sirva o asset separadamente:

```bash
uikitpr css -o static/uikitpr.css
uikitpr css -o static/uikitpr.min.css --minify
uikitpr motion -o static/uikitpr-motion.js
uikitpr cache -o static/uikitpr-cache.js
```

Então use:

```python
from uikitpr import Styles

Styles(href="/static/uikitpr.css")
UIProvider(AppContent(), with_styles=False)
```

Para renderização exclusivamente cliente, `Styles(inline=True, nonce="...")`
também é suportado em políticas CSP baseadas em nonce.

## Desenvolvimento

```bash
prpm install
prpm test
prpm pack
prpm verify dist
```

O exemplo completo está em [`examples/dashboard.py`](examples/dashboard.py).

### Site e GitHub Pages

O site oficial também é construído com PyReact e UIKitPR:

```bash
prpm run site
prpm run serve
```

O primeiro comando gera `_site/`; o segundo serve a página em
`http://localhost:8000`. Pushes em `main` executam testes, geram o site
estático e publicam no GitHub Pages.

## Licença

MIT. Veja [LICENSE](LICENSE).
