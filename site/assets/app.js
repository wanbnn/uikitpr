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

  const header = document.querySelector(".site-header");
  const updateHeader = () => header.classList.toggle("header-scrolled", window.scrollY > 16);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
})();

