# Creative catalog

UIKitPR contains a native 135-component collection organized into four product
categories. The components are written for PyReact and share
UIKitPR's CSS, DOM/canvas runtime, tokens, accessibility defaults, and
`prefers-reduced-motion` behavior.

```python
from uikitpr import Aurora, ClickSpark, Dock, GlitchText

Aurora(
    GlitchText("UIKitPR"),
    color="#8b5cf6",
    secondary="#26c6da",
    speed=8,
)
```

Common visual properties are `color`, `secondary`, `speed`, and `intensity`.
UI components also accept `items`, while text components accept direct text as
their child. The searchable GitHub Pages catalog contains a live preview and a
copy-ready example for every entry.

## Text animations (22)

`ASCIIText`, `BlurText`, `CircularText`, `CountUp`, `CurvedLoop`,
`DecryptedText`, `FallingText`, `FuzzyText`, `GlitchText`, `GradientText`,
`RotatingText`, `ScrambledText`, `ScrollFloat`, `ScrollReveal`,
`ScrollVelocity`, `ShinyText`, `SplitText`, `TextCursor`, `TextPressure`,
`TextTrail`, `TrueFocus`, `VariableProximity`.

## Animations (28)

`AnimatedContent`, `Antigravity`, `BlobCursor`, `ClickSpark`, `Crosshair`,
`Cubes`, `ElectricBorder`, `FadeContent`, `GhostCursor`, `GlareHover`,
`GradualBlur`, `ImageTrail`, `LaserFlow`, `LogoLoop`, `Magnet`, `MagnetLines`,
`MetaBalls`, `MetallicPaint`, `Noise`, `OrbitImages`, `PixelTrail`,
`PixelTransition`, `Ribbons`, `ShapeBlur`, `SplashCursor`, `StarBorder`,
`StickerPeel`, `TargetCursor`.

## UI components (38)

`AnimatedList`, `BorderGlow`, `BounceCards`, `BubbleMenu`, `CardNav`,
`CardSwap`, `Carousel`, `ChromaGrid`, `CircularGallery`, `Counter`,
`CurvedInput`, `DecayCard`, `Dock`, `DomeGallery`, `ElasticSlider`,
`FlowingMenu`, `FluidGlass`, `FlyingPosters`, `Folder`, `GlassIcons`,
`GlassSurface`, `GooeyNav`, `InfiniteMenu`, `Lanyard`, `LineSidebar`,
`MagicBento`, `Masonry`, `ModelViewer`, `PillNav`, `PixelCard`, `ProfileCard`,
`ReflectiveCard`, `ScrollStack`, `SpotlightCard`, `Stack`, `StaggeredMenu`,
`Stepper`, `TiltedCard`.

UIKitPR already uses `Stack` for its layout primitive. Import the creative
component as `CreativeStack`, or use the namespaced version through
`uikitpr.creative.Stack`.

## Backgrounds (47)

`AcidSquares`, `Aurora`, `Balatro`, `Ballpit`, `Beams`, `ColorBends`,
`DarkVeil`, `Dither`, `DotField`, `DotGrid`, `EvilEye`, `FaultyTerminal`,
`Ferrofluid`, `FloatingLines`, `Galaxy`, `GradientBlinds`, `GradientWaves`,
`Grainient`, `GridDistortion`, `GridMotion`, `GridScan`, `Hyperspeed`,
`Iridescence`, `LetterGlitch`, `LightPillar`, `LightRays`, `Lightfall`,
`Lightning`, `LineWaves`, `LiquidChrome`, `LiquidEther`, `Orb`, `Particles`,
`PixelBlast`, `PixelSnow`, `Plasma`, `PlasmaWave`, `Prism`, `PrismaticBurst`,
`Radar`, `RippleGrid`, `ShapeGrid`, `SideRays`, `Silk`, `SoftAurora`, `Threads`,
`Waves`.

## Runtime and CSP

`UIProvider` includes the shared catalog runtime by default. Externalize it for
a strict Content Security Policy:

```bash
uikitpr creative -o static/uikitpr-creative.js
```

```python
UIProvider(App(), creative_src="/static/uikitpr-creative.js")
```

Set `with_creative=False` when a page uses only CSS-based UIKitPR components.
