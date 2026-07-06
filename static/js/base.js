"use strict";

const sidebar = document.querySelector("#sidebar");
const menuButton = document.querySelector("#menu-button");
const scrim = document.querySelector("#sidebar-scrim");
const mobileNavigation = window.matchMedia("(max-width: 900px)");

function setSidebarOpen(isOpen, restoreFocus = false) {
  if (!sidebar || !menuButton || !scrim) return;

  const shouldOpen = mobileNavigation.matches && isOpen;
  sidebar.classList.toggle("open", shouldOpen);
  scrim.classList.toggle("visible", shouldOpen);
  scrim.setAttribute("aria-hidden", String(!shouldOpen));
  menuButton.setAttribute("aria-expanded", String(shouldOpen));
  document.body.classList.toggle("navigation-open", shouldOpen);

  if (mobileNavigation.matches) {
    sidebar.toggleAttribute("inert", !shouldOpen);
    sidebar.setAttribute("aria-hidden", String(!shouldOpen));
  } else {
    sidebar.removeAttribute("inert");
    sidebar.removeAttribute("aria-hidden");
  }

  if (!shouldOpen && restoreFocus) menuButton.focus();
}

menuButton?.addEventListener("click", () => setSidebarOpen(true));
scrim?.addEventListener("click", () => setSidebarOpen(false, true));
sidebar?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setSidebarOpen(false)));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setSidebarOpen(false, true);
});

mobileNavigation.addEventListener("change", () => setSidebarOpen(false));
setSidebarOpen(false);

/* Theme panel, toasts and page-specific controls remain disabled until their owning issues. */
