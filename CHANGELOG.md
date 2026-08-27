# Changelog

All notable UIKitPR changes will be documented in this file.

## Unreleased

- Raised the supported Python baseline to 3.10 so UIKitPR's package metadata,
  CI matrix, and documentation match the required PyReact runtime dependency.
- Added animated text primitives: `AnimatedText`, `BlurText`, `SplitText`,
  `ShinyText`, and `GradientText`.
- Added Aurora, dots, grid, and beam background components.
- Added `SpotlightCard`, `StarBorder`, and `Marquee` creative surfaces.
- Added a searchable live catalog with copy-ready examples to GitHub Pages.
- Added reduced-motion fallbacks and accessible text segmentation.
- Added the frozen 135-item compatibility baseline: 22 text animations,
  28 animations, 38 UI components, and 47 backgrounds.
- Added a shared pointer/canvas runtime, `UIProvider` integration, and the
  `uikitpr creative` asset export command.
- Generated all catalog exports and GitHub Pages entries from one registry.

## 0.3.2 - 2026-07-27

- Added continuous ambient movement to the Motion demonstration.
- Limited the state monitor to the main target, excluding entry-animation noise.
- Added readable per-preset states: running, completed, interrupted, and ambient loop.
- Lifecycle events now include `preset` and `animate` in `event.detail`.

## 0.3.1 - 2026-07-27

- Added declarative Motion controls through `motion_control()`.
- Integrated click delegation directly into the Motion runtime.
- Resolved `motion_id` without CSS selector interpolation.
- Made Pop, Shake, Flip, and Blur demos independent from helper JavaScript.

## 0.3.0 - 2026-07-27

- Added cache management with SHA-256 fingerprints and asset manifests.
- Added a versioned Service Worker with configurable strategies and cleanup.
- Added a browser API for diagnostics, updates, registration, and invalidation.
- Added immutable website URLs to prevent mixed releases on GitHub Pages.
- Added live Motion and Cache indicators to the demo.
- Added fallbacks when Web Animations or IntersectionObserver are unavailable.

## 0.2.0 - 2026-07-27

- Added UIKitPR's dependency-free declarative Motion engine.
- Added presets, spring physics, timelines, stagger, scroll, and in-view.
- Added mount, click, hover, tap, and focus triggers.
- Added lifecycle events and an imperative browser API.
- Added dots, bars, ring, pulse, orbit, and wave loaders.
- Added skeletons, loading cards, and a page loader.
- Bundled an exportable runtime in the wheel and CLI.

## 0.1.0 - 2026-07-27

- First public release.
- Utility-first CSS framework with light and dark themes.
- PyReact components for layout, forms, feedback, data, and navigation.
- Token-based custom themes.
- CLI stylesheet export.
- SSR and Python 3.9–3.14 support.
