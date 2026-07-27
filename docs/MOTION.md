# UIKitPR Motion

UIKitPR Motion é o motor de animações web declarativo do ecossistema PyReact.
O runtime usa a Web Animations API do navegador, mas orchestration, presets,
spring physics, triggers, timelines, eventos e lifecycle pertencem ao UIKitPR.

## Começando

`UIProvider` inclui CSS e runtime automaticamente:

```python
from uikitpr import Motion, UIProvider

UIProvider(
    Motion(
        "Entra quando ficar visível",
        preset="fade-up",
        trigger="in-view",
    )
)
```

Para servir o runtime externamente:

```bash
uikitpr motion -o static/uikitpr-motion.js
```

```python
UIProvider(App(), motion_src="/static/uikitpr-motion.js")
```

## Estados e interação

```python
from uikitpr import Motion, Spring, Transition

Motion(
    Card(...),
    initial={"opacity": 0, "transform": "translateY(30px)"},
    animate={"opacity": 1, "transform": "translateY(0)"},
    while_hover={"transform": "translateY(-6px) scale(1.02)"},
    while_tap={"transform": "scale(.97)"},
    while_focus={"boxShadow": "0 0 0 4px var(--uipr-focus)"},
    transition=Transition(
        duration=.7,
        spring=Spring(stiffness=170, damping=18),
    ),
)
```

Triggers disponíveis:

- `mount`
- `in-view`
- `click`
- `scroll`, através da propriedade `scroll`
- eventos imperativos pela API web

## Presets

`fade`, `fade-up`, `fade-down`, `slide-left`, `slide-right`, `scale`, `pop`,
`blur`, `flip`, `shake`, `pulse` e `float`.

## Stagger

```python
from uikitpr import MotionGroup

MotionGroup(
    Card(...),
    Card(...),
    Card(...),
    preset="fade-up",
    stagger=.08,
)
```

## Timeline

```python
from uikitpr import MotionTimeline, Timeline, TimelineStep, Transition

intro = Timeline(
    id="intro",
    steps=[
        TimelineStep("hero", "fade-up"),
        TimelineStep(
            ".feature-card",
            "scale",
            transition=Transition(duration=.35),
            at="-=.15",
        ),
    ],
)

MotionTimeline(Page(), timeline=intro)
```

## Runtime web e eventos

O runtime fica disponível como `window.UIKitPRMotion`:

```javascript
UIKitPRMotion.play("hero", "pop");
UIKitPRMotion.pause("hero");
UIKitPRMotion.resume("hero");
UIKitPRMotion.reverse("hero");
UIKitPRMotion.cancel("hero");
UIKitPRMotion.timeline("intro");
UIKitPRMotion.registerPreset("brand-pop", definition);
```

Eventos DOM:

- `uipr:motion:start`
- `uipr:motion:update`
- `uipr:motion:finish`
- `uipr:motion:cancel`
- `uipr:motion:ready`

O runtime observa VNodes adicionados depois do carregamento, respeita
`prefers-reduced-motion` e remove listeners e animações quando nós saem do DOM.

