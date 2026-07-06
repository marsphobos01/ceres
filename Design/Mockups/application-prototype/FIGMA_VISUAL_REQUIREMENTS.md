# Ceres Figma visual requirements

This supplements `FIGMA_SYNC.md` and covers two elements that must not be omitted from the editable Figma screens.

## Icon system

The interface uses the custom SVG sprite in `index.html`. Figma should contain a reusable `Icon` component set with the same 24 by 24 coordinate system, rounded line caps and joins, and 1.8 px default stroke.

A Figma-ready source sheet is available at:

`assets/figma/ceres-icon-sheet.svg`

Icons are required for:

- every sidebar navigation item
- global search, theme, notifications and profile controls
- quick actions and button actions where the HTML includes an icon
- empty states, file actions, filters, view toggles and overflow menus
- user, group, message, calendar, module, note, task and study-session affordances

Use the Ceres icon shapes rather than emoji, Unicode symbols or unrelated library icons. Keep the sprout-and-orbit logo as a separate brand component.

## Dashboard hero

The dashboard hero is a defining part of Ceres and should span the full available content width.

It must include:

- layered sky
- subtle stars
- three orbit rings
- the planet and moon
- the hill or horizon silhouette
- a visible foreground plant and pot
- greeting and date
- current lecture and progress
- open-lecture action
- integrated next-event row

The Moonlit editable artwork reference is:

`assets/figma/ceres-dashboard-hero-moonlit.svg`

The browser implementation remains theme-aware through the semantic values in `assets/theme-tokens.css`. Forest, Clay, Daybreak, Linen and Harvest should keep the same composition and only change palette.

The hero should not be simplified into a plain card or have the plant and celestial artwork removed to make room for more dashboard widgets.

## Figma completion checks

A synced dashboard must visibly contain both the icon system and the complete hero illustration. A text-only sidebar, empty circular controls, or a hero without the plant, planet, sky and orbit treatment is incomplete.
