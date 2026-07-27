# UIKitPR Cache

UIKitPR Cache é a camada de entrega e invalidação de assets do framework. Ela
resolve o caso comum em que HTML, CSS e runtimes JavaScript publicados por uma
CDN ou pelo GitHub Pages ficam em versões diferentes.

## O que ele entrega

- fingerprint SHA-256 no nome de cada asset;
- manifesto JSON com caminho, hash, SRI, tamanho e MIME type;
- Service Worker com cache versionado;
- limpeza automática de caches antigos;
- navegação `network-first`;
- assets em `cache-first`, `network-first` ou `stale-while-revalidate`;
- cliente web com atualização, diagnóstico e limpeza manual;
- eventos `uipr:cache:*`.

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

`app.path` e `styles.path` são os caminhos que devem entrar no HTML. O build
gera `asset-manifest.json` e `sw.js` na raiz de saída.

Nomes passados ao gerenciador são sempre relativos. Caminhos absolutos e
travessias com `..` são rejeitados.

## Integração PyReact

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

Ou inclua `CacheRuntime(...)` diretamente. `with_cache` é opt-in porque cada
aplicação precisa publicar seu próprio `sw.js` e manifesto.

## API do navegador

```javascript
await UIKitPRCache.register();
await UIKitPRCache.refresh();
const manifest = await UIKitPRCache.manifest();
const state = UIKitPRCache.status();
await UIKitPRCache.clear();
await UIKitPRCache.clear({ unregister: true });
```

O registro usa `updateViaCache: "none"` e inclui a versão na URL do Service
Worker, evitando que o próprio script de atualização fique preso em cache.

## Eventos

- `uipr:cache:registering`
- `uipr:cache:ready`
- `uipr:cache:updatefound`
- `uipr:cache:update`
- `uipr:cache:installed`
- `uipr:cache:controllerchange`
- `uipr:cache:refreshed`
- `uipr:cache:cleared`
- `uipr:cache:error`
- `uipr:cache:unsupported`

Todos os eventos incluem `version` e `cacheVersion` em `event.detail`.

## GitHub Pages

Sirva `sw.js`, `asset-manifest.json`, `index.html` e a pasta `assets` no mesmo
artefato. O Service Worker usa URLs relativas ao próprio escopo, portanto
funciona tanto em domínio raiz quanto em Pages de projeto, como `/uikitpr/`.

Use `network-first` para navegação. O HTML novo aponta para nomes com hash; os
assets podem então usar `cache-first` sem risco de servir conteúdo de outra
release.
