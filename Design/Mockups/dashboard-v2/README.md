# Ceres Dashboard V2 Mockup Pack

This directory contains a standalone design concept for the next Ceres dashboard and identity direction.

## Open the mockups

Open `index.html` in a modern browser and choose the desktop dashboard, mobile dashboard, identity system, or theme studio. The pages do not require Django or a build process.

## Product direction

- Prioritise what is happening now, what comes next, and what needs attention.
- Keep the hero distinctive without pushing useful information too far below the fold.
- Use one calm workspace rather than several competing coloured panels.
- Give deadlines progress, a concrete next action, and a continuation control.
- Use a vertical agenda spine and persistent navigation on mobile.

## V2.2 dashboard changes

- Reduced the hero planet while preserving the shared orbital centre.
- Kept the moon positioned on its orbit.
- Attached the next event directly beneath the current lecture.
- Anchored the desktop agenda line and nodes to one shared CSS coordinate.
- Restored a solid terracotta-brown attention card with no blur or transparent glass effect.
- Applied the same attention card on mobile and removed the side highlight.

## V2.3 logo refinement

- Retained the rounded gold orbit.
- Extended the plant well above the orbit crossing point.
- Continued the central stem naturally into the upper-right leaf.
- Moved the lower-left leaf onto one clear secondary branch.
- Lowered the orbit crossing so the stem no longer appears to end at the ring.
- Preserved the centred gold seed and rear/front orbit layering.

## V2.3.1 surface polish

- Removed the large outer shadow from the desktop workspace.
- Replaced the surrounding gradient with a flat forest surface.
- The workspace now uses its border and surface contrast for consistent separation on every side.

## V2.4 theme studio

Open `theme-options.html` to compare four complete dashboard palettes using the same layout and content:

- **Forest** — the original deep botanical Ceres palette.
- **Moonlit** — navy, periwinkle and gold. This is the recommended balanced default.
- **Clay** — charcoal, terracotta and warm gold.
- **Linen** — a warm light, paper-inspired academic theme.

The theme studio remembers the selected option in local storage and accepts direct query links such as `theme-options.html?theme=clay`. Reusable design tokens are defined in `assets/theme-tokens.css` so the palettes can later be connected to Django user preferences without duplicating component CSS.

Reusable logo assets are available in `assets/ceres-icon.svg` and `assets/ceres-logo.svg`.

## Implementation boundary

This pack is standalone. It does not modify production Django templates, models, URLs, or static assets.
