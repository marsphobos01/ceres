# Ceres Figma Sync Contract

The connected HTML prototype in this directory is the visual and content source of truth for the Figma file:

**Ceres — Connected Product Prototype**  
https://www.figma.com/design/21zRR3uttJnfG48os8JgKk/Ceres-%E2%80%94-Connected-Product-Prototype?node-id=4-2

This contract exists to prevent the editable Figma mockups and the browser prototype from drifting apart.

## Canonical source files

1. `index.html` — application shell and SVG icon sprite
2. `assets/prototype.css` — layout, typography and component geometry
3. `assets/theme-tokens.css` — all colour and theme values
4. `assets/prototype.js` — screen content, route inventory and prototype interactions

When Figma and these files disagree, update Figma to match these files unless a deliberate design change is first made in the HTML prototype.

## Shared shell

| Property | Canonical value |
| --- | ---: |
| Desktop sidebar | `218px` |
| Desktop top bar | `66px` |
| Standard screen padding | `28px` |
| Default card radius | `17px` |
| Default control radius | `10px` |
| UI typeface | Inter |
| Display typeface | Newsreader |

The sidebar navigation order, badges, profile footer, global search, theme button, notifications and avatar must remain identical across top-level screens.

## Theme collection

### Dark

- Moonlit — default
- Forest
- Clay

### Light

- Daybreak
- Linen
- Harvest

Figma colours must be derived from `assets/theme-tokens.css`. Do not create visually similar one-off colour styles. Every screen must work with the same semantic roles: app background, main background, sidebar, surface levels, text, muted text, line, accent, gold, danger, success, warning, attention and button.

## Supplied reference renders

These are the approved core-screen references and their native frame sizes:

| Screen | Theme | Frame size |
| --- | --- | ---: |
| Dashboard | Moonlit | `1600 × 1153` |
| Calendar | Moonlit | `1440 × 1106` |
| Messages | Linen | `1440 × 1014` |
| Modules | Moonlit | `1440 × 900` |
| Notes | Moonlit | `1440 × 900` |
| Onboarding | Linen | `1440 × 900` |
| Settings | Linen | `1440 × 1084` |

The Figma page `01 · Core Screens` contains a section named **HTML Wireframes · Source of Truth** reserved for these exact references. Older hand-built frames should be treated as legacy comparison material until rebuilt against the references.

## Screen inventory

The complete connected prototype includes:

- Dashboard
- Calendar
- Timetable
- Modules and Module Detail
- Lecture Hub
- Assignments and Assignment Detail
- Notes and Note Editor
- Revision and Flashcards
- Tasks and Study Sessions
- Files and File Detail
- Whiteboard
- Friends
- Groups and Project Workspace
- Messages
- Search
- Notifications
- Onboarding
- Settings
- Profile
- Login and Registration

## Content parity rules

Figma must match the prototype for:

- labels, headings, descriptions and button copy
- dates, times, counts, badges and percentages
- module codes and academic terminology
- selected navigation state
- card order and information hierarchy
- theme shown on each approved reference
- icon meaning, size and stroke treatment

Do not substitute placeholder copy, generic icons or approximate counts while marking a frame as synced.

## Layout parity rules

- Preserve the same page width, rail proportions and card grid structure.
- Use the shared shell rather than recreating navigation per screen.
- Use reusable Figma components for buttons, icon buttons, navigation rows, cards, pills, inputs, switches and segmented controls.
- Use variables or semantic styles mapped directly to the CSS token names.
- Keep headings in Newsreader and functional interface copy in Inter.
- Avoid shadows, gradients or glass effects unless they exist in `prototype.css` for that component.
- Reference renders may be placed as locked comparison layers, but final synced frames should remain editable.

## Sync completion checklist

A Figma frame is considered synced only when:

- [ ] its dimensions match the HTML render
- [ ] its theme maps to the CSS tokens
- [ ] shell dimensions and navigation match
- [ ] typography and hierarchy match
- [ ] all visible copy and data match
- [ ] spacing, radii, borders and control sizes match
- [ ] reusable components are used where applicable
- [ ] a side-by-side visual comparison shows no material drift

Last reviewed against the connected prototype: **6 July 2026**.
