# UIKitPR Motion

UIKitPR Motion is the declarative web-animation engine for PyReact. The runtime
uses the browser Web Animations API, while orchestration, presets, spring
physics, triggers, timelines, events, and lifecycle belong to UIKitPR.

## Getting started

`UIProvider` automatically includes the CSS and runtime:

```python
from uikitpr import Motion, UIProvider

UIProvider(Motion("Enters when visible", preset="fade-up", trigger="in-view"))
```

To serve the runtime externally:

```bash
uikitpr motion -o static/uikitpr-motion.js
```

```python
UIProvider(App(), motion_src="/static/uikitpr-motion.js")
```

## States and interaction

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

Available triggers are `mount`, `in-view`, `click`, `scroll`, and imperative
events from the web API.

## Presets

Built-in presets include `fade`, `fade-up`, `fade-down`, `slide-left`,
`slide-right`, `scale`, `pop`, `blur`, `flip`, `shake`, `pulse`, and `float`.

## Stagger

```python
from uikitpr import MotionGroup

MotionGroup(Card(...), Card(...), Card(...), preset="fade-up", stagger=.08)
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

## Web runtime and events

The runtime is available as `window.UIKitPRMotion`:

```javascript
UIKitPRMotion.play("hero", "pop");
UIKitPRMotion.pause("hero");
UIKitPRMotion.resume("hero");
UIKitPRMotion.reverse("hero");
UIKitPRMotion.cancel("hero");
UIKitPRMotion.timeline("intro");
UIKitPRMotion.registerPreset("brand-pop", definition);
```

Clickable controls can remain fully declarative:

```python
from uikitpr import Button, motion_control

Button("Shake", **motion_control("hero", "shake", transition={"duration": 620}))
```

Lifecycle events are `uipr:motion:start`, `update`, `finish`, `cancel`, `ready`,
and `control`. Start, finish, and cancel details include `preset`, `animate`,
`config`, and, when applicable, `animation`.

The runtime uses event delegation, observes VNodes added after page load,
respects `prefers-reduced-motion`, and cleans up listeners and animations when
nodes leave the DOM.
