# Components

Every component accepts `className`, `class_name`, `style`, events, and HTML
attributes. The values below are specific to UIKitPR.

| Component | Main properties |
| --- | --- |
| `Container` | `size=sm/md/lg/xl/full` |
| `Stack` | `direction`, `gap`, `align`, `justify`, `wrap` |
| `Grid` | `cols=1..12`, `gap` |
| `Heading` | `level=1..6`, `size`, `as_` |
| `Text` | `tone`, `size`, `weight`, `as_` |
| `Button` | `variant`, `size`, `loading`, `block`, `as_` |
| `Badge` | `tone`, `pill` |
| `Alert` | `tone`, `title` |
| `Input` / `Textarea` / `Select` | `label`, `help_text`, `error` |
| `Avatar` | `src`, `name`, `initials`, `size` |
| `Progress` | `value`, `label` |
| `Modal` | `open`, `title` |
| `UIProvider` | `theme`, `color_mode`, `with_styles`, `full_height` |
| `Motion` | `preset`, `trigger`, `transition`, `while_hover`, `while_tap` |
| `MotionGroup` | `preset`, `stagger`, `delay`, `trigger` |
| `MotionTimeline` | `timeline=Timeline(...)` |
| Loaders | `size`, `tone`, `label` |
| `Skeleton` | `variant`, `lines` |
| `PageLoader` | `loader`, `overlay`, `label` |

## Composition

Direct constructors are the most natural way to express trees in Python:

```python
Card(
    CardHeader(Heading("Account", level=2)),
    CardBody(Text("User preferences.")),
    CardFooter(Button("Save")),
)
```

When using a component inside `h`, provide children through `props`:

```python
h(Button, {"children": "Save", "variant": "primary"})
```

## Accessibility

- `Button(loading=True)` sets `disabled` and `aria-busy`.
- `Alert` uses `role="alert"`.
- `Spinner` uses `role="status"` and a configurable label.
- `Progress` exposes the complete range ARIA attributes.
- `Modal` uses `role="dialog"` and `aria-modal`.
- Fields with an `error` receive `aria-invalid`.
