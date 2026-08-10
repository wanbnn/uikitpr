(() => {
  if (window.UIKitPRCreative) return;
  const cleanups = new WeakMap();
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const animateNumber = (node) => {
    const from = Number(node.dataset.uiprCreativeFrom);
    const to = Number(node.dataset.uiprCreativeTo);
    if (!Number.isFinite(from) || !Number.isFinite(to)) return;
    if (reduceMotion) { node.textContent = String(to); return; }
    const start = performance.now();
    const tick = (now) => {
      const progress = Math.min(1, (now - start) / 1200);
      const eased = 1 - Math.pow(1 - progress, 3);
      node.textContent = String(Math.round(from + (to - from) * eased));
      if (progress < 1 && node.isConnected) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  const pointer = (node) => {
    const move = (event) => {
      const rect = node.getBoundingClientRect();
      node.style.setProperty("--uipr-creative-x", `${event.clientX - rect.left}px`);
      node.style.setProperty("--uipr-creative-y", `${event.clientY - rect.top}px`);
      node.style.setProperty("--uipr-creative-nx", String((event.clientX - rect.left) / rect.width - .5));
      node.style.setProperty("--uipr-creative-ny", String((event.clientY - rect.top) / rect.height - .5));
    };
    node.addEventListener("pointermove", move, { passive: true });
    return () => node.removeEventListener("pointermove", move);
  };

  const canvas = (node) => {
    const target = node.querySelector(".uipr-creative-canvas");
    if (!target || reduceMotion) return () => {};
    const context = target.getContext("2d");
    if (!context) return () => {};
    const seed = [...(node.dataset.uiprCreative || "creative")].reduce((total, char) => total + char.charCodeAt(0), 0);
    const particles = Array.from({ length: 34 }, (_, index) => ({
      x: ((seed * (index + 3)) % 997) / 997,
      y: ((seed * (index + 7)) % 991) / 991,
      r: 1 + ((seed + index * 13) % 4),
      v: .00008 + ((index * 7) % 9) * .000012,
    }));
    let frame = 0;
    let running = false;
    let destroyed = false;
    const resize = () => {
      const rect = node.getBoundingClientRect();
      const ratio = Math.min(devicePixelRatio || 1, 2);
      target.width = Math.max(1, rect.width * ratio);
      target.height = Math.max(1, rect.height * ratio);
      target.style.width = `${rect.width}px`;
      target.style.height = `${rect.height}px`;
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
    };
    const draw = (time) => {
      if (!running || destroyed || !node.isConnected) return;
      const width = target.clientWidth;
      const height = target.clientHeight;
      context.clearRect(0, 0, width, height);
      const color = getComputedStyle(node).getPropertyValue("--uipr-creative-color").trim() || "#8b5cf6";
      context.fillStyle = color;
      context.strokeStyle = color;
      particles.forEach((particle, index) => {
        const x = particle.x * width;
        const y = ((particle.y + time * particle.v) % 1) * height;
        context.globalAlpha = .18 + (index % 5) * .08;
        context.beginPath();
        context.arc(x, y, particle.r, 0, Math.PI * 2);
        context.fill();
        if (index && index % 3 === 0) {
          const previous = particles[index - 1];
          context.beginPath();
          context.moveTo(x, y);
          context.lineTo(previous.x * width, ((previous.y + time * previous.v) % 1) * height);
          context.stroke();
        }
      });
      context.globalAlpha = 1;
      frame = requestAnimationFrame(draw);
    };
    resize();
    const observer = new ResizeObserver(resize);
    observer.observe(node);
    const visibility = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !running) {
        running = true;
        frame = requestAnimationFrame(draw);
      } else if (!entry.isIntersecting && running) {
        running = false;
        cancelAnimationFrame(frame);
      }
    }, { rootMargin: "160px" });
    visibility.observe(node);
    return () => {
      destroyed = true;
      running = false;
      cancelAnimationFrame(frame);
      observer.disconnect();
      visibility.disconnect();
    };
  };

  const mount = (node) => {
    if (!(node instanceof HTMLElement) || cleanups.has(node)) return;
    const teardown = [pointer(node)];
    if (node.dataset.uiprCreativeFrom !== undefined) animateNumber(node);
    if (node.querySelector(".uipr-creative-canvas")) teardown.push(canvas(node));
    cleanups.set(node, () => teardown.forEach((cleanup) => cleanup?.()));
  };

  const scan = (root = document) => root.querySelectorAll?.("[data-uipr-creative]").forEach(mount);
  const observer = new MutationObserver((records) => records.forEach((record) => {
    record.addedNodes.forEach((node) => { if (node.nodeType === 1) { if (node.matches?.("[data-uipr-creative]")) mount(node); scan(node); } });
    record.removedNodes.forEach((node) => { if (node.nodeType === 1) { cleanups.get(node)?.(); node.querySelectorAll?.("[data-uipr-creative]").forEach((child) => cleanups.get(child)?.()); } });
  }));
  scan();
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.UIKitPRCreative = { version: "1.0.0", scan, destroy: () => observer.disconnect() };
  document.dispatchEvent(new CustomEvent("uipr:creative:ready", { detail: { api: window.UIKitPRCreative } }));
})();
