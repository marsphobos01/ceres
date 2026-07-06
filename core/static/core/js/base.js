"use strict";

const navigation = document.querySelector("[data-navigation]");
const mobileNavigation = window.matchMedia("(max-width: 768px)");

function updateNavigationState(event) {
  if (!navigation) {
    return;
  }

  navigation.open = !event.matches;
}

updateNavigationState(mobileNavigation);
mobileNavigation.addEventListener("change", updateNavigationState);
