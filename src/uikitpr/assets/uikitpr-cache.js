/**
 * UIKitPR Cache 0.3.1
 * Registro, atualização, diagnóstico e invalidação do cache web.
 */
(() => {
  "use strict";

  const VERSION = "0.3.1";
  const script = document.currentScript
    || document.querySelector("[data-uipr-cache-runtime]");
  const options = {
    serviceWorker: script?.dataset.serviceWorker || "sw.js",
    manifest: script?.dataset.manifest || "asset-manifest.json",
    version: script?.dataset.version || VERSION,
    name: script?.dataset.cacheName || "uikitpr",
    scope: script?.dataset.scope || undefined,
    auto: script?.dataset.auto !== "false",
  };
  let registration = null;
  let refreshing = false;

  const emit = (name, detail = {}) => {
    document.dispatchEvent(
      new CustomEvent(name, {
        detail: { version: VERSION, cacheVersion: options.version, ...detail },
      }),
    );
  };

  const status = () => ({
    supported: "serviceWorker" in navigator && "caches" in window,
    controlled: Boolean(navigator.serviceWorker?.controller),
    version: VERSION,
    cacheVersion: options.version,
    registration,
  });

  const register = async (overrides = {}) => {
    Object.assign(options, overrides);
    if (!("serviceWorker" in navigator)) {
      emit("uipr:cache:unsupported");
      return null;
    }
    emit("uipr:cache:registering");
    const separator = options.serviceWorker.includes("?") ? "&" : "?";
    const url = `${options.serviceWorker}${separator}v=${encodeURIComponent(options.version)}`;
    try {
      registration = await navigator.serviceWorker.register(url, {
        scope: options.scope,
        updateViaCache: "none",
      });
      registration.addEventListener("updatefound", () => {
        const worker = registration.installing;
        emit("uipr:cache:updatefound", { registration, worker });
        worker?.addEventListener("statechange", () => {
          if (worker.state === "installed") {
            emit(
              navigator.serviceWorker.controller
                ? "uipr:cache:update"
                : "uipr:cache:installed",
              { registration, worker },
            );
            if (navigator.serviceWorker.controller) {
              worker.postMessage({ type: "UIKITPR_SKIP_WAITING" });
            }
          }
        });
      });
      await registration.update();
      emit("uipr:cache:ready", { registration });
      return registration;
    } catch (error) {
      emit("uipr:cache:error", { error });
      console.warn("[UIKitPR Cache] falha ao registrar o Service Worker", error);
      return null;
    }
  };

  const clear = async ({ unregister = false } = {}) => {
    if (!("caches" in window)) return [];
    const names = await caches.keys();
    const removed = await Promise.all(
      names
        .filter((name) => name.startsWith(`${options.name}-`))
        .map(async (name) => ((await caches.delete(name)) ? name : null)),
    );
    if (unregister && "serviceWorker" in navigator) {
      const registrations = await navigator.serviceWorker.getRegistrations();
      await Promise.all(registrations.map((item) => item.unregister()));
      registration = null;
    }
    const result = removed.filter(Boolean);
    emit("uipr:cache:cleared", { caches: result, unregistered: unregister });
    return result;
  };

  const manifest = async () => {
    const separator = options.manifest.includes("?") ? "&" : "?";
    const response = await fetch(
      `${options.manifest}${separator}v=${encodeURIComponent(options.version)}`,
      { cache: "no-store" },
    );
    if (!response.ok) throw new Error(`Manifesto indisponível (${response.status})`);
    return response.json();
  };

  const refresh = async () => {
    const current = registration || await register();
    await current?.update();
    emit("uipr:cache:refreshed", { registration: current });
    return current;
  };

  navigator.serviceWorker?.addEventListener("controllerchange", () => {
    emit("uipr:cache:controllerchange");
    if (!refreshing) {
      refreshing = true;
      window.location.reload();
    }
  });

  const api = { version: VERSION, options, status, register, clear, manifest, refresh };
  window.UIKitPRCache = api;
  if (options.auto) register();
})();
