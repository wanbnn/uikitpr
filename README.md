<div align="center">

# UIKitPR

### O framework visual utility-first feito para PyReact.

[![PyPI](https://img.shields.io/pypi/v/uikitpr?logo=pypi&logoColor=white)](https://pypi.org/project/uikitpr/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyReact](https://img.shields.io/badge/PyReact-1.0.5%2B-6D4AFF)](https://github.com/wanbnn/pyreact)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Componentes acessíveis, temas e classes utilitárias em um pacote Python,
sem pipeline Node obrigatório.

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

## CSS externo e CSP

Por padrão, `UIProvider` inclui um `<link>` com o stylesheet em uma `data: URL`.
Esse formato evita o escaping aplicado pelo SSR do PyReact a filhos de
`<style>`. Para produção com CSP estrita, exporte e sirva o asset separadamente:

```bash
uikitpr css -o static/uikitpr.css
uikitpr css -o static/uikitpr.min.css --minify
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
