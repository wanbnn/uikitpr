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

  document.querySelectorAll("[data-motion-preset]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!window.UIKitPRMotion) return;
      window.UIKitPRMotion.play("motion-lab-card", button.dataset.motionPreset, {
        duration: button.dataset.motionPreset === "shake" ? 620 : 720,
        easing: "cubic-bezier(.22,1,.36,1)",
      });
    });
  });

  const motionEvent = document.querySelector("[data-motion-event]");
  ["uipr:motion:start", "uipr:motion:finish", "uipr:motion:cancel"].forEach((name) => {
    document.addEventListener(name, (event) => {
      if (!motionEvent || !event.target.closest?.(".section-motion")) return;
      motionEvent.textContent = name;
      motionEvent.parentElement.classList.add("event-active");
      window.setTimeout(() => motionEvent.parentElement.classList.remove("event-active"), 420);
    });
  });

  const header = document.querySelector(".site-header");
  const updateHeader = () => header.classList.toggle("header-scrolled", window.scrollY > 16);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
})();
