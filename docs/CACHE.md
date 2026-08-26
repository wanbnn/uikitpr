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
- safe runtime caching boundaries that do not cache arbitrary same-origin API requests;
- `Cache-Control: no-store` and `private` enforcement before runtime responses are persisted;
- cache isolation so one UIKitPR cache cannot accidentally satisfy another cache's request;
- explicit opt-in for public dynamic routes;
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

## Safe runtime caching

The generated Service Worker does not treat every same-origin GET as cacheable.
By default it handles only:

- navigations, preserving the existing offline/navigation behavior;
- static browser destinations such as scripts, styles, images, fonts, workers,
  manifests, audio, and video;
- URLs explicitly included in the precache list.

Fetch/XHR requests with an empty browser destination, such as `/api/me`,
`/api/session`, or `/graphql`, bypass UIKitPR's runtime cache by default. Requests
that carry an `Authorization` header are also bypassed.

Before a runtime response is written, UIKitPR rejects responses whose
`Cache-Control` contains `no-store` or `private`, as well as `Vary: *`. This lets
applications and backend APIs explicitly prevent persistence even for routes
that would otherwise be eligible.

For a public dynamic endpoint that is intentionally safe to cache, opt in with
same-origin path prefixes:

```python
policy = CachePolicy(
    runtime_cache_paths=("/api/public/", "/content/"),
)
```

Only absolute same-origin path prefixes beginning with `/` are accepted; full
URLs are rejected. This makes dynamic caching an explicit application decision
rather than an accidental side effect.

Applications with personalized HTML can also disable navigation caching while
retaining static-asset caching:

```python
policy = CachePolicy(cache_navigations=False)
```

Each Service Worker strategy reads only from its own versioned cache instead of
using a global `caches.match()`. This prevents an unrelated cache on the same
origin from supplying a stale or incorrect response.

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
