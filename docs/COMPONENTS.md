# Componentes

Todo componente aceita `className`, `class_name`, `style`, eventos e atributos
HTML. Os valores abaixo são específicos do UIKitPR.

| Componente | Propriedades principais |
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

## Composição

Construtores diretos são a forma mais natural de expressar árvores em Python:

```python
Card(
    CardHeader(Heading("Conta", level=2)),
    CardBody(Text("Preferências do usuário.")),
    CardFooter(Button("Salvar")),
)
```

Para um componente dentro de `h`, forneça filhos em `props`:

```python
h(Button, {"children": "Salvar", "variant": "primary"})
```

## Acessibilidade

- `Button(loading=True)` define `disabled` e `aria-busy`.
- `Alert` usa `role="alert"`.
- `Spinner` usa `role="status"` e rótulo configurável.
- `Progress` expõe todos os atributos ARIA de faixa.
- `Modal` usa `role="dialog"` e `aria-modal`.
- campos com `error` recebem `aria-invalid`.

