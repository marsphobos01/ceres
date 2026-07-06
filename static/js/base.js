"use strict";

const sidebar = document.querySelector("[data-sidebar]");
const openButton = document.querySelector("[data-sidebar-open]");
const closeButton = document.querySelector("[data-sidebar-close]");
const scrim = document.querySelector("[data-sidebar-scrim]");
const mobileNavigation = window.matchMedia("(max-width: 900px)");

function setNavigationState(isOpen) {
  if (!sidebar || !openButton || !scrim) {
    return;
  }

  const shouldOpen = mobileNavigation.matches && isOpen;

  sidebar.classList.toggle("is-open", shouldOpen);
  sidebar.toggleAttribute("inert", mobileNavigation.matches && !shouldOpen);
  sidebar.setAttribute("aria-hidden", String(mobileNavigation.matches && !shouldOpen));
  openButton.setAttribute("aria-expanded", String(shouldOpen));
  scrim.hidden = !shouldOpen;
  document.body.classList.toggle("navigation-open", shouldOpen);
}

function closeNavigation({ restoreFocus = false } = {}) {
  const wasOpen = sidebar?.classList.contains("is-open");
  setNavigationState(false);

  if (restoreFocus && wasOpen) {
    openButton?.focus();
  }
}

openButton?.addEventListener("click", () => setNavigationState(true));
closeButton?.addEventListener("click", () => closeNavigation({ restoreFocus: true }));
scrim?.addEventListener("click", () => closeNavigation({ restoreFocus: true }));

sidebar?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => closeNavigation());
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeNavigation({ restoreFocus: true });
  }
});

mobileNavigation.addEventListener("change", () => setNavigationState(false));
setNavigationState(false);
