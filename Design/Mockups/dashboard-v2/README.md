# Ceres Dashboard V2 Mockup Pack

This directory contains a standalone, implementation-neutral concept for the next Ceres dashboard and identity direction.

## Open the mockups

Open `index.html` in a modern browser and choose the desktop dashboard, mobile dashboard, or identity system. The pages do not require Django or a build process.

## Product decisions represented

- The dashboard first answers what is happening now, what comes next, and what needs attention.
- The hero remains distinctive but no longer pushes useful information too far below the fold.
- The body is one calm workspace rather than several competing coloured cards.
- Deadlines include progress, a concrete next action, and a direct continuation control.
- Desktop navigation exposes six primary destinations and moves secondary tools behind More tools.
- Mobile uses a vertical agenda spine and five persistent navigation destinations.
- Sage communicates growth/current state, gold communicates progress and planetary identity, and terracotta is reserved for genuine attention.

## V2.1 refinement pass

The refinement pass addresses the first visual review:

- Redraws the sprout so curved branches visibly connect to both leaves.
- Splits the gold ellipse into rear and front arcs so it reads as an orbit around the plant.
- Integrates the next event into the hero timeline and removes the duplicate desktop Up next strip.
- Rebuilds the hero orbits, planet, and moon around shared geometric centres.
- Aligns every agenda marker precisely over its timeline.
- Uses one two-column CSS grid for all four dashboard quadrants, keeping the central intersection aligned.
- Replaces the assignment alert's translucent nested panel with a flat editorial treatment.
- Compacts the sidebar profile footer.
- Applies the same flat attention treatment on mobile.

Reusable logo assets are available in `assets/ceres-icon.svg` and `assets/ceres-logo.svg`.

## Implementation boundary

This pack is deliberately standalone. It does not modify production Django templates, models, URLs, or static assets. It is intended for design review before implementation work begins.
