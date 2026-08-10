# Creative effects

UIKitPR includes text animations, decorative backgrounds, and interactive
surfaces in the regular package. They are Python components, ship as part of
the same stylesheet, and do not require Node.js or WebGL.

## Text animations

```python
from uikitpr import AnimatedText, BlurText, GradientText, ShinyText, SplitText

BlurText("Build without starting from zero", delay=.06)
SplitText("MOVEMENT", delay=.04)
ShinyText("Ready for production", duration=3)
GradientText("Made with Python", colors=["#6d4aff", "#26c6da"])
AnimatedText("A gentle wave", effect="wave", by="char")
```

`AnimatedText` accepts `effect=blur/rise/wave/reveal`, `by=word/char`,
`delay`, `duration`, and `distance`. The visual segments are hidden from
assistive technology and a single unbroken copy of the text remains available
to screen readers.

## Backgrounds

```python
from uikitpr import AuroraBackground, BeamBackground, DotBackground, GridBackground

AuroraBackground(
    Content(),
    color="#6d4aff",
    secondary="#26c6da",
    speed=12,
    opacity=.45,
)
```

All backgrounds accept children plus `color`, `secondary`, `size`, `speed`, and
`opacity`. The background layer is decorative and does not interfere with the
content or pointer events.

## Creative components

```python
from uikitpr import Marquee, SpotlightCard, StarBorder

SpotlightCard(CardBody(...), spotlight="#26c6da")
StarBorder(Button("Publish"), color="#ff5ca8", speed=4)
Marquee(Badge("PyReact"), Badge("SSR"), duration=18, reverse=False)
```

The marquee pauses on hover and duplicates its group only visually. All
continuous animations stop when the browser requests reduced motion.

## Live catalog

The GitHub Pages build includes a searchable catalog at `/docs/`, with live
previews and copy-ready Python snippets. Build it locally with:

```bash
prpm run site
prpm run serve
```
