/**
 * UIKitPR Motion 0.3.0
 * Runtime visual, declarativo e sem dependências.
 */
(() => {
  "use strict";

  const VERSION = "0.3.0";
  const MOTION_SELECTOR = "[data-uipr-motion]";
  const GROUP_SELECTOR = "[data-uipr-motion-group]";
  const TIMELINE_SELECTOR = "[data-uipr-timeline]";
  const states = new WeakMap();
  const timelines = new Map();
  const presets = new Map();
  const media = window.matchMedia("(prefers-reduced-motion: reduce)");

  const builtins = {
    fade: { initial: { opacity: 0 }, animate: { opacity: 1 } },
    "fade-up": {
      initial: { opacity: 0, transform: "translateY(24px)" },
      animate: { opacity: 1, transform: "translateY(0)" },
    },
    "fade-down": {
      initial: { opacity: 0, transform: "translateY(-24px)" },
      animate: { opacity: 1, transform: "translateY(0)" },
    },
    "slide-left": {
      initial: { opacity: 0, transform: "translateX(36px)" },
      animate: { opacity: 1, transform: "translateX(0)" },
    },
    "slide-right": {
      initial: { opacity: 0, transform: "translateX(-36px)" },
      animate: { opacity: 1, transform: "translateX(0)" },
    },
    scale: {
      initial: { opacity: 0, transform: "scale(.88)" },
      animate: { opacity: 1, transform: "scale(1)" },
    },
    pop: {
      initial: { opacity: 0, transform: "scale(.65) rotate(-4deg)" },
      animate: { opacity: 1, transform: "scale(1) rotate(0)" },
    },
    blur: {
      initial: { opacity: 0, filter: "blur(12px)" },
      animate: { opacity: 1, filter: "blur(0)" },
    },
    flip: {
      initial: { opacity: 0, transform: "perspective(800px) rotateX(-70deg)" },
      animate: { opacity: 1, transform: "perspective(800px) rotateX(0)" },
    },
    shake: {
      keyframes: [
        { transform: "translateX(0)" },
        { transform: "translateX(-8px)" },
        { transform: "translateX(8px)" },
        { transform: "translateX(-5px)" },
        { transform: "translateX(5px)" },
        { transform: "translateX(0)" },
      ],
    },
    pulse: {
      keyframes: [
        { transform: "scale(1)", opacity: 1 },
        { transform: "scale(1.04)", opacity: 0.82 },
        { transform: "scale(1)", opacity: 1 },
      ],
    },
    float: {
      keyframes: [
        { transform: "translateY(0)" },
        { transform: "translateY(-10px)" },
        { transform: "translateY(0)" },
      ],
    },
  };

  Object.entries(builtins).forEach(([name, value]) => presets.set(name, value));

  const parse = (value, fallback = {}) => {
    try {
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      console.warn("[UIKitPR Motion] configuração inválida", error);
      return fallback;
    }
  };

  const emit = (element, name, detail = {}) => {
    element.dispatchEvent(
      new CustomEvent(name, {
        bubbles: true,
        detail: { element, motionId: element.dataset.uiprMotionId, ...detail },
      }),
    );
  };

  const transitionOptions = (transition = {}) => ({
    duration: Math.max(0, Number(transition.duration ?? 450)),
    delay: Math.max(0, Number(transition.delay ?? 0)),
    easing: transition.spring ? "linear" : transition.easing || "cubic-bezier(.22,1,.36,1)",
    iterations:
      transition.repeat === "infinite" || transition.repeat === Infinity
        ? Infinity
        : Math.max(1, Number(transition.repeat || 0) + 1),
    direction: transition.direction || "normal",
    fill: transition.fill || "both",
  });

  const interpolateValue = (from, to, progress) => {
    if (typeof from === "number" && typeof to === "number") {
      return from + (to - from) * progress;
    }
    const fromText = String(from);
    const toText = String(to);
    const fromNumbers = [...fromText.matchAll(/-?\d*\.?\d+/g)].map((match) => Number(match[0]));
    const toNumbers = [...toText.matchAll(/-?\d*\.?\d+/g)].map((match) => Number(match[0]));
    if (!fromNumbers.length || fromNumbers.length !== toNumbers.length) {
      return progress < 0.5 ? from : to;
    }
    let index = 0;
    return fromText.replace(/-?\d*\.?\d+/g, () => {
      const value = fromNumbers[index] + (toNumbers[index] - fromNumbers[index]) * progress;
      index += 1;
      return Number(value.toFixed(4)).toString();
    });
  };

  const springProgress = (spring = {}, frames = 60) => {
    const stiffness = Number(spring.stiffness ?? 170);
    const damping = Number(spring.damping ?? 26);
    const mass = Math.max(0.001, Number(spring.mass ?? 1));
    let velocity = Number(spring.velocity ?? 0);
    let position = 0;
    const values = [0];
    const dt = 1 / 60;
    for (let index = 1; index < frames - 1; index += 1) {
      const acceleration = (-stiffness * (position - 1) - damping * velocity) / mass;
      velocity += acceleration * dt;
      position += velocity * dt;
      values.push(position);
    }
    values.push(1);
    return values;
  };

  const springFrames = (from, to, spring) =>
    springProgress(spring).map((progress, index, values) => {
      const frame = { offset: index / (values.length - 1) };
      const keys = new Set([...Object.keys(from || {}), ...Object.keys(to || {})]);
      keys.forEach((key) => {
        const start = from?.[key] ?? to?.[key];
        const end = to?.[key] ?? from?.[key];
        frame[key] = interpolateValue(start, end, progress);
      });
      return frame;
    });

  const mergeConfig = (config) => {
    const preset = config.preset ? presets.get(config.preset) || {} : {};
    return {
      ...preset,
      ...config,
      initial: { ...(preset.initial || {}), ...(config.initial || {}) },
      animate: { ...(preset.animate || {}), ...(config.animate || {}) },
      keyframes: config.keyframes || preset.keyframes,
    };
  };

  const framesFor = (config, override) => {
    if (typeof override === "string") {
      const selected = presets.get(override);
      if (selected?.keyframes) return selected.keyframes;
      if (selected) return [selected.initial || config.animate || {}, selected.animate || {}];
    }
    if (Array.isArray(override)) return override;
    if (override && typeof override === "object") {
      return [config.animate || config.initial || {}, override];
    }
    if (config.keyframes) return config.keyframes;
    const initial = config.initial || {};
    const target = config.animate || {};
    if (config.transition?.spring) {
      return springFrames(initial, target, config.transition.spring);
    }
    return [initial, target];
  };

  const commitAnimation = (animation, element, frames) => {
    animation.addEventListener("finish", () => {
      try {
        animation.commitStyles();
        if (animation.effect?.getTiming().iterations !== Infinity) animation.cancel();
      } catch {
        Object.assign(element.style, frames[frames.length - 1] || {});
      }
    }, { once: true });
  };

  const play = (element, override, transitionOverride = {}) => {
    if (!element) return null;
    const state = states.get(element) || initMotion(element);
    if (!state) return null;
    const config = state.config;
    const transition = { ...(config.transition || {}), ...transitionOverride };
    const frames = framesFor(config, override);
    if (media.matches || typeof element.animate !== "function") {
      emit(element, "uipr:motion:start", {
        config,
        reducedMotion: media.matches,
        fallback: typeof element.animate !== "function",
      });
      Object.assign(element.style, frames[frames.length - 1] || {});
      emit(element, "uipr:motion:finish", {
        config,
        reducedMotion: media.matches,
        fallback: typeof element.animate !== "function",
      });
      return null;
    }
    state.animations.forEach((animation) => animation.cancel());
    state.animations.clear();
    const animation = element.animate(frames, transitionOptions(transition));
    let completed = false;
    state.animations.add(animation);
    emit(element, "uipr:motion:start", { animation, config });
    animation.addEventListener("finish", () => {
      completed = true;
      state.animations.delete(animation);
      emit(element, "uipr:motion:finish", { animation, config });
    }, { once: true });
    animation.addEventListener("cancel", () => {
      state.animations.delete(animation);
      if (!completed) emit(element, "uipr:motion:cancel", { animation, config });
    }, { once: true });
    commitAnimation(animation, element, frames);
    return animation;
  };

  const restore = (element) => {
    const state = states.get(element);
    if (!state) return;
    const target = state.config.animate || state.config.initial || {};
    play(element, target, { duration: 180, delay: 0, spring: null });
  };

  const listen = (state, target, event, handler, options) => {
    target.addEventListener(event, handler, options);
    state.cleanup.push(() => target.removeEventListener(event, handler, options));
  };

  const setupInView = (element, state) => {
    if (typeof IntersectionObserver !== "function") {
      requestAnimationFrame(() => play(element));
      return;
    }
    const options = state.config.inView || {};
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            play(element);
            if (state.config.once !== false) observer.unobserve(element);
          } else if (state.config.replay) {
            Object.assign(element.style, state.config.initial || {});
          }
        });
      },
      {
        threshold: options.amount ?? 0.18,
        rootMargin: options.margin || "0px 0px -8% 0px",
      },
    );
    observer.observe(element);
    state.cleanup.push(() => observer.disconnect());
  };

  const setupScroll = (element, state) => {
    const config = state.config.scroll || {};
    const frames = framesFor(state.config);
    const animation = element.animate(frames, {
      duration: 1000,
      fill: "both",
      easing: "linear",
    });
    animation.pause();
    state.animations.add(animation);
    let scheduled = false;
    const update = () => {
      scheduled = false;
      const rect = element.getBoundingClientRect();
      const viewport = window.innerHeight;
      const start = Number(config.start ?? 0.95);
      const end = Number(config.end ?? 0.15);
      const raw = (viewport * start - rect.top) / (viewport * (start - end) + rect.height);
      const progress = Math.max(0, Math.min(1, raw));
      animation.currentTime = progress * 1000;
      emit(element, "uipr:motion:update", { progress });
    };
    const requestUpdate = () => {
      if (!scheduled) {
        scheduled = true;
        requestAnimationFrame(update);
      }
    };
    listen(state, window, "scroll", requestUpdate, { passive: true });
    listen(state, window, "resize", requestUpdate, { passive: true });
    requestUpdate();
  };

  const bindInteractions = (element, state) => {
    const config = state.config;
    if (config.whileHover) {
      listen(state, element, "mouseenter", () => play(element, config.whileHover, { delay: 0 }));
      listen(state, element, "mouseleave", () => restore(element));
    }
    if (config.whileTap) {
      listen(state, element, "pointerdown", () => play(element, config.whileTap, { duration: 120, delay: 0 }));
      listen(state, element, "pointerup", () => restore(element));
      listen(state, element, "pointercancel", () => restore(element));
    }
    if (config.whileFocus) {
      listen(state, element, "focus", () => play(element, config.whileFocus, { delay: 0 }));
      listen(state, element, "blur", () => restore(element));
    }
    if (config.trigger === "click") {
      listen(state, element, "click", () => play(element));
    }
  };

  function initMotion(element) {
    if (!element || states.has(element)) return states.get(element);
    const config = mergeConfig(parse(element.dataset.uiprMotion));
    const state = { config, animations: new Set(), cleanup: [] };
    states.set(element, state);
    if (config.initial) Object.assign(element.style, config.initial);
    bindInteractions(element, state);
    if (config.scroll) {
      setupScroll(element, state);
    } else if (config.trigger === "in-view") {
      setupInView(element, state);
    } else if (config.trigger === "mount") {
      requestAnimationFrame(() => play(element));
    }
    return state;
  }

  const initGroup = (group) => {
    if (group.dataset.uiprMotionGroupReady) return;
    group.dataset.uiprMotionGroupReady = "true";
    const config = parse(group.dataset.uiprMotionGroup);
    const children = [...group.querySelectorAll(config.selector || ":scope > *")];
    children.forEach((child, index) => {
      const childConfig = {
        preset: config.preset || "fade-up",
        trigger: config.trigger || "in-view",
        once: config.once !== false,
        transition: {
          duration: 450,
          delay: Number(config.delay || 0) + index * Number(config.stagger || 80),
        },
      };
      if (!child.dataset.uiprMotion) {
        child.dataset.uiprMotion = JSON.stringify(childConfig);
      }
      initMotion(child);
    });
  };

  const resolveTargets = (target) => {
    if (!target) return [];
    const value = String(target);
    const escaped = window.CSS?.escape
      ? window.CSS.escape(value)
      : value.replaceAll("\\", "\\\\").replaceAll('"', '\\"');
    const byMotionId = document.querySelectorAll(`[data-uipr-motion-id="${escaped}"]`);
    if (byMotionId.length) return [...byMotionId];
    try {
      return [...document.querySelectorAll(value)];
    } catch {
      return [];
    }
  };

  const runTimeline = async (definition) => {
    const running = [];
    let cursor = 0;
    for (const step of definition.steps || []) {
      const transition = step.transition || {};
      let at = step.at;
      if (typeof at === "string" && at.startsWith("+=")) {
        cursor += Number(at.slice(2)) * 1000;
      } else if (typeof at === "string" && at.startsWith("-=")) {
        cursor -= Number(at.slice(2)) * 1000;
      } else if (typeof at === "number") {
        cursor = at * 1000;
      }
      const animations = resolveTargets(step.target)
        .map((target) => play(target, typeof step.animate === "string" ? presets.get(step.animate)?.animate : step.animate, {
          ...transition,
          delay: Number(transition.delay || 0) + Math.max(0, cursor),
        }))
        .filter(Boolean);
      running.push(...animations);
      cursor += Number(transition.duration || 450);
    }
    await Promise.allSettled(running.map((animation) => animation.finished));
    return running;
  };

  const initTimeline = (element) => {
    if (element.dataset.uiprTimelineReady) return;
    element.dataset.uiprTimelineReady = "true";
    const definition = parse(element.dataset.uiprTimeline);
    if (definition.id) timelines.set(definition.id, definition);
    if (definition.autoplay !== false) requestAnimationFrame(() => runTimeline(definition));
  };

  const destroy = (element) => {
    const state = states.get(element);
    if (!state) return;
    state.animations.forEach((animation) => animation.cancel());
    state.cleanup.forEach((cleanup) => cleanup());
    states.delete(element);
  };

  const scan = (root = document) => {
    if (root.matches?.(MOTION_SELECTOR)) initMotion(root);
    if (root.matches?.(GROUP_SELECTOR)) initGroup(root);
    if (root.matches?.(TIMELINE_SELECTOR)) initTimeline(root);
    root.querySelectorAll?.(GROUP_SELECTOR).forEach(initGroup);
    root.querySelectorAll?.(MOTION_SELECTOR).forEach(initMotion);
    root.querySelectorAll?.(TIMELINE_SELECTOR).forEach(initTimeline);
  };

  const api = {
    version: VERSION,
    presets,
    scan,
    play(target, animate, transition) {
      const elements = typeof target === "string" ? resolveTargets(target) : [target];
      return elements.map((element) => play(element, animate, transition)).filter(Boolean);
    },
    pause(target) {
      const elements = typeof target === "string" ? resolveTargets(target) : [target];
      elements.forEach((element) => states.get(element)?.animations.forEach((animation) => animation.pause()));
    },
    resume(target) {
      const elements = typeof target === "string" ? resolveTargets(target) : [target];
      elements.forEach((element) => states.get(element)?.animations.forEach((animation) => animation.play()));
    },
    reverse(target) {
      const elements = typeof target === "string" ? resolveTargets(target) : [target];
      elements.forEach((element) => states.get(element)?.animations.forEach((animation) => animation.reverse()));
    },
    cancel(target) {
      const elements = typeof target === "string" ? resolveTargets(target) : [target];
      elements.forEach((element) => states.get(element)?.animations.forEach((animation) => animation.cancel()));
    },
    registerPreset(name, definition) {
      presets.set(name, definition);
      return api;
    },
    timeline(definitionOrId) {
      const definition =
        typeof definitionOrId === "string" ? timelines.get(definitionOrId) : definitionOrId;
      if (!definition) throw new Error(`Timeline não encontrada: ${definitionOrId}`);
      return runTimeline(definition);
    },
    spring: springProgress,
    destroy,
  };

  window.UIKitPRMotion = api;
  document.addEventListener("uipr:motion:play", (event) => {
    const target = event.detail?.target || event.detail?.id;
    api.play(target, event.detail?.animate, event.detail?.transition);
  });
  document.addEventListener("uipr:motion:timeline", (event) => {
    api.timeline(event.detail?.timeline || event.detail?.id);
  });

  const boot = () => {
    scan(document);
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) scan(node);
        });
        mutation.removedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (states.has(node)) destroy(node);
            node.querySelectorAll?.(MOTION_SELECTOR).forEach(destroy);
          }
        });
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    document.dispatchEvent(new CustomEvent("uipr:motion:ready", { detail: { api } }));
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
