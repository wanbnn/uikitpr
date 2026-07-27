(() => {
  const root = document.querySelector(".site-root");
  const toggles = document.querySelectorAll("[data-theme-toggle]");
  const toast = document.querySelector(".toast");

  const setTheme = (theme) => {
    root.dataset.uiprTheme = theme;
    root.dataset.uiprColorMode = theme;
    document.documentElement.style.colorScheme = theme;
    localStorage.setItem("uipr-site-theme", theme);
    document.querySelectorAll("[data-theme-label]").forEach((label) => {
      label.textContent = theme === "dark" ? "Testar modo claro" : "Testar modo escuro";
    });
  };

  const preferred = localStorage.getItem("uipr-site-theme")
    || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  setTheme(preferred);

  toggles.forEach((button) => {
    button.addEventListener("click", () => {
      setTheme(root.dataset.uiprColorMode === "dark" ? "light" : "dark");
    });
  });

  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      await navigator.clipboard.writeText(button.dataset.copy);
      toast.textContent = "Comando copiado";
      toast.classList.add("toast-visible");
      window.setTimeout(() => toast.classList.remove("toast-visible"), 1800);
    });
  });

  const motionEvent = document.querySelector("[data-motion-event]");
  const setMotionStatus = (value) => {
    if (motionEvent) motionEvent.textContent = value;
  };
  if (window.UIKitPRMotion) {
    setMotionStatus(`motion: v${window.UIKitPRMotion.version}`);
  } else {
    document.addEventListener(
      "uipr:motion:ready",
      (event) => setMotionStatus(`motion: v${event.detail.api.version}`),
      { once: true },
    );
  }
  ["uipr:motion:start", "uipr:motion:finish", "uipr:motion:cancel"].forEach((name) => {
    document.addEventListener(name, (event) => {
      if (!motionEvent || !event.target.closest?.(".section-motion")) return;
      motionEvent.textContent = name;
      motionEvent.parentElement.classList.add("event-active");
      window.setTimeout(() => motionEvent.parentElement.classList.remove("event-active"), 420);
    });
  });

  const cacheStatus = document.querySelector("[data-cache-status]");
  const cacheMonitor = cacheStatus?.closest(".cache-event-monitor");
  const setCacheStatus = (value) => {
    if (cacheStatus) cacheStatus.textContent = value;
    cacheMonitor?.classList.add("event-active");
    window.setTimeout(() => cacheMonitor?.classList.remove("event-active"), 420);
  };
  if (window.UIKitPRCache) {
    const current = window.UIKitPRCache.status();
    setCacheStatus(
      current.supported
        ? `cache: ${current.cacheVersion}`
        : "cache: não suportado",
    );
  }
  document.addEventListener("uipr:cache:ready", (event) => {
    setCacheStatus(`cache: ${event.detail.cacheVersion}`);
  });
  document.addEventListener("uipr:cache:update", () => {
    setCacheStatus("cache: atualizando");
  });
  document.addEventListener("uipr:cache:error", () => {
    setCacheStatus("cache: modo online");
  });
  document.querySelector("[data-cache-refresh]")?.addEventListener("click", async () => {
    if (!window.UIKitPRCache) {
      window.location.reload();
      return;
    }
    setCacheStatus("cache: limpando");
    await window.UIKitPRCache.clear();
    window.location.reload();
  });

  const header = document.querySelector(".site-header");
  const updateHeader = () => header.classList.toggle("header-scrolled", window.scrollY > 16);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
})();
