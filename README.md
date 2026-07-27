<div align="center">

# UIKitPR

The utility-first visual framework built for PyReact.

[![PyPI](https://img.shields.io/pypi/v/uikitpr?logo=pypi&logoColor=white)](https://pypi.org/project/uikitpr/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyReact](https://img.shields.io/badge/PyReact-1.0.5%2B-6D4AFF)](https://github.com/wanbnn/pyreact)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/wanbnn/uikitpr/blob/main/LICENSE)
[![Docs](https://readthedocs.org/projects/uikitpr/badge/?version=latest)](https://uikitpr.readthedocs.io/en/latest/)

Accessible components, themes, utility classes, and a native motion engine in
one Python package, with no mandatory Node pipeline.

**Website:** <https://wanbnn.github.io/uikitpr/>

</div>

## Why UIKitPR?

UIKitPR brings Tailwind-like composition and ready-made components to PyReact:

- predictable utility classes such as `flex`, `gap-4`, and `grid-cols-3`;
- Python components that return PyReact VNodes;
- light, dark, and custom themes powered by CSS variables;
- SSR, handlers, and properties compatible with PyReact's `h()`;
- CSS bundled in the wheel and exportable through the CLI;
- motion with springs, timelines, stagger, scroll, events, and lifecycle;
- fingerprinted web assets, manifests, updates, and Service Workers;
- loaders, skeletons, and ready-to-use visual states;
- no JavaScript dependency or compilation step.

## Installation

```bash
prpm add uikitpr
```

You can also use `pip install uikitpr`.

## Quick start

```python
from uikitpr import Button, Card, CardBody, Heading, Stack, UIProvider


def App(props):
    return UIProvider(
        Card(
            CardBody(
                Stack(
                    Heading("Hello, PyReact!", level=1),
                    Button("Get started", variant="primary"),
                    gap=4,
                )
            )
        ),
        class_name="p-6",
        full_height=True,
    )
```

Components accept children directly or through
`h(Component, {"children": ...})`. The explicit `children` property is
important with current PyReact functional components.

## Utilities

Use classes in `className` or `class_name`:

```python
from uikitpr import Box, cx

Box(
    "Content",
    class_name=cx(
        "flex items-center gap-4 p-6 rounded shadow",
        {"bg-primary-soft": highlighted, "hidden": not visible},
    ),
)
```

The stylesheet includes flex/grid layout, spacing, sizing, typography, colors,
borders, shadows, and responsive variants such as `md-grid-cols-3`.

## Components

| Group | Components |
| --- | --- |
| Layout | `Box`, `Container`, `Stack`, `Grid`, `Divider` |
| Typography | `Heading`, `Text`, `Badge` |
| Actions | `Button`, `IconButton` |
| Forms | `Input`, `Textarea`, `Select`, `Checkbox`, `Switch` |
| Feedback | `Alert`, `Spinner`, `Progress`, `Modal` |
| Data and navigation | `Card`, `Table`, `Navbar`, `Breadcrumb`, `Avatar` |

Unconsumed properties are forwarded to the DOM VNode, including `onClick`,
`aria-*`, `data-*`, `style`, `id`, and `name`. See the
[component reference](https://uikitpr.readthedocs.io/en/latest/COMPONENTS.html).

## Themes

`UIProvider` includes the CSS and selects a theme:

```python
UIProvider(AppContent(), theme="dark", full_height=True)
```

Create a branded theme with tokens:

```python
from uikitpr import create_theme

brand = create_theme(
    "my-brand",
    primary="#ff006e",
    primary_hover="#d9005d",
    radius="1rem",
)

UIProvider(AppContent(), theme=brand)
```

## Motion and interaction

`UIProvider` includes the UIKitPR Motion runtime by default:

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

The engine supports mount, in-view, click, hover, tap, focus, and scroll
animations; presets and custom keyframes; spring physics; staggered groups;
timelines; lifecycle events; declarative controls; dynamically added VNodes;
and `prefers-reduced-motion`. See the
[Motion guide](https://uikitpr.readthedocs.io/en/latest/MOTION.html).

## Web cache and deployment

`CacheManager` writes SHA-256-fingerprinted assets, an inspectable manifest, and
a versioned Service Worker:

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
```

The browser exposes `window.UIKitPRCache.register()`, `refresh()`, `manifest()`,
`status()`, and `clear()`. See the
[cache guide](https://uikitpr.readthedocs.io/en/latest/CACHE.html).

## Loaders and visual states

```python
from uikitpr import OrbitLoader, Skeleton, SkeletonCard

OrbitLoader(size="lg")
Skeleton(lines=3)
SkeletonCard()
```

`DotsLoader`, `BarsLoader`, `RingLoader`, `PulseLoader`, `WaveLoader`, and
`PageLoader` are also available.

## External CSS and CSP

For strict Content Security Policy deployments, export and serve assets
separately:

```bash
uikitpr css -o static/uikitpr.css
uikitpr css -o static/uikitpr.min.css --minify
uikitpr motion -o static/uikitpr-motion.js
uikitpr cache -o static/uikitpr-cache.js
```

```python
from uikitpr import Styles

Styles(href="/static/uikitpr.css")
UIProvider(AppContent(), with_styles=False)
```

Client-only rendering also supports `Styles(inline=True, nonce="...")`.

## Development

```bash
prpm install
prpm test
prpm pack
prpm verify dist
```

The complete example is available in
[`examples/dashboard.py`](https://github.com/wanbnn/uikitpr/blob/main/examples/dashboard.py).
Build and serve the official
website with `prpm run site` and `prpm run serve`.

## Documentation

The complete English documentation is available on
[Read the Docs](https://uikitpr.readthedocs.io/en/latest/).

## License

MIT. See [LICENSE](https://github.com/wanbnn/uikitpr/blob/main/LICENSE).
