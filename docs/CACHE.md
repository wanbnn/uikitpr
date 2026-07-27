# UIKitPR Cache

UIKitPR Cache is the framework's asset delivery and invalidation layer. It
prevents HTML, CSS, and JavaScript runtimes deployed through a CDN or GitHub
Pages from being served from different releases.

## Features

- SHA-256 fingerprints in asset filenames;
- a JSON manifest with path, hash, SRI, size, and MIME type;
- a versioned Service Worker and automatic stale-cache cleanup;
- `network-first` navigation;
- `cache-first`, `network-first`, or `stale-while-revalidate` assets;
- a browser client for updates, diagnostics, and manual cleanup;
- `uipr:cache:*` events.

## Build

```python
from uikitpr import CacheManager, CachePolicy

manager = CacheManager(
    "public",
    policy=CachePolicy(
        name="my-pyreact-app",
        version="1.4.0",
        strategy="cache-first",
        navigation_strategy="network-first",
    ),
)

app = manager.add_file("app.js", "static/app.js")
styles = manager.add_file("app.css", "static/app.css")
manager.finalize(precache=["./"])
```

Use `app.path` and `styles.path` in the HTML. The build writes
`asset-manifest.json` and `sw.js` at the output root. Asset names must be
relative; absolute paths and `..` traversal are rejected.

## PyReact integration

```python
from uikitpr import CacheRuntime, UIProvider

UIProvider(
    App(),
    with_cache=True,
    cache_src="/assets/uikitpr-cache.js",
    service_worker="/sw.js",
    cache_manifest="/asset-manifest.json",
    cache_version="1.4.0",
    cache_name="my-pyreact-app",
)
```

You may also include `CacheRuntime(...)` directly. Caching is opt-in because
each application must publish its own Service Worker and manifest.

## Browser API

```javascript
await UIKitPRCache.register();
await UIKitPRCache.refresh();
const manifest = await UIKitPRCache.manifest();
const state = UIKitPRCache.status();
await UIKitPRCache.clear();
await UIKitPRCache.clear({ unregister: true });
```

Registration uses `updateViaCache: "none"` and includes the version in the
Service Worker URL so that the updater itself cannot become stuck in cache.

## Events

Events include `registering`, `ready`, `updatefound`, `update`, `installed`,
`controllerchange`, `refreshed`, `cleared`, `error`, and `unsupported`, all
under the `uipr:cache:` prefix. Every event includes `version` and
`cacheVersion` in `event.detail`.

## GitHub Pages

Serve `sw.js`, `asset-manifest.json`, `index.html`, and `assets/` in the same
artifact. Relative Service Worker URLs support both root domains and project
paths such as `/uikitpr/`. Use `network-first` for navigation; hashed assets can
safely use `cache-first`.
