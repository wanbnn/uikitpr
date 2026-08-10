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

  const docsSearch = document.querySelector("[data-doc-search-input]");
  const docsItems = [...document.querySelectorAll("[data-doc-item]")];
  const docsFilters = [...document.querySelectorAll("[data-doc-filter]")];
  const docsEmpty = document.querySelector("[data-doc-empty]");
  let docsCategory = "all";
  const updateDocs = () => {
    const query = docsSearch?.value.trim().toLowerCase() || "";
    let visible = 0;
    docsItems.forEach((item) => {
      const categoryMatches = docsCategory === "all" || item.dataset.docCategory === docsCategory;
      const searchMatches = !query || item.dataset.docSearch.includes(query);
      item.hidden = !(categoryMatches && searchMatches);
      if (!item.hidden) visible += 1;
    });
    if (docsEmpty) docsEmpty.hidden = visible !== 0;
  };
  docsSearch?.addEventListener("input", updateDocs);
  docsFilters.forEach((button) => {
    button.addEventListener("click", () => {
      docsCategory = button.dataset.docFilter;
      docsFilters.forEach((item) => {
        item.classList.toggle("uipr-button-primary", item === button);
        item.classList.toggle("uipr-button-ghost", item !== button);
      });
      updateDocs();
    });
  });
  if (document.querySelector(".docs-root") && window.location.hash) {
    window.setTimeout(() => {
      document.getElementById(window.location.hash.slice(1))?.scrollIntoView({ block: "start" });
    }, 120);
  }

  const motionEvent = document.querySelector("[data-motion-event]");
  const motionMonitor = motionEvent?.closest(".motion-event-monitor");
  const motionTarget = "motion-lab-card";
  let motionRevision = 0;
  const setMotionStatus = (value) => {
    if (motionEvent) motionEvent.textContent = value;
    motionMonitor?.classList.add("event-active");
    window.setTimeout(() => motionMonitor?.classList.remove("event-active"), 420);
  };
  if (window.UIKitPRMotion) {
    setMotionStatus(`loop ambiente · v${window.UIKitPRMotion.version}`);
  } else {
    document.addEventListener(
      "uipr:motion:ready",
      (event) => setMotionStatus(`loop ambiente · v${event.detail.api.version}`),
      { once: true },
    );
  }
  document.addEventListener("uipr:motion:start", (event) => {
    if (event.target.dataset?.uiprMotionId !== motionTarget) return;
    motionRevision += 1;
    setMotionStatus(`${event.detail.preset || "motion"} · executando`);
  });
  document.addEventListener("uipr:motion:finish", (event) => {
    if (event.target.dataset?.uiprMotionId !== motionTarget) return;
    const revision = motionRevision;
    setMotionStatus(`${event.detail.preset || "motion"} · concluído`);
    window.setTimeout(() => {
      if (revision === motionRevision) {
        setMotionStatus(`loop ambiente · v${window.UIKitPRMotion?.version || "ativo"}`);
      }
    }, 900);
  });
  document.addEventListener("uipr:motion:cancel", (event) => {
    if (event.target.dataset?.uiprMotionId !== motionTarget) return;
    setMotionStatus(`${event.detail.preset || "motion"} · interrompido`);
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
