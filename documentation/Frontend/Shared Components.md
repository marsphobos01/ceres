# Shared frontend components

## Source of truth

The production frontend foundation uses the exact shared styles and class names from:

```text
Design/Mockups/application-prototype/
```

The active production copy is:

```text
static/css/prototype-foundation.css
```

It contains the prototype's application shell, navigation, top bar, typography, controls, cards, grids, lists, tables, empty states and responsive rules.

Feature-specific prototype stylesheet imports are retained as comments at the top of `prototype-foundation.css`. They must stay disabled until their owning feature issues are implemented.

## Permanent visual rule: no side highlights

Do not use a coloured strip, thickened border or inset shadow on only the left or right edge of a UI component.

This includes:

- active navigation items
- alerts and message banners
- calendar and timetable items
- cards, list rows and empty states
- form validation states
- selected, warning, success and error states

Do not introduce patterns such as:

```css
border-left: 0.25rem solid var(--accent);
border-left-width: 0.25rem;
box-shadow: inset 0.25rem 0 var(--accent);
```

Use one or more of these instead:

- a full border around the component
- a subtle tinted background
- an icon or badge
- a text colour change
- a normal focus outline around the whole component

Structural dividers between major layout regions are allowed, provided they are neutral separators rather than coloured state indicators.

## Buttons

Use `.button` as the base class and the same modifier names as the prototype.

```html
<button class="button primary" type="submit">Save changes</button>
<a class="button" href="/planning/">Open planning</a>
<button class="button danger" type="button">Delete</button>
<button class="button ghost" type="button">Cancel</button>
<button class="button small" type="button">Compact action</button>
```

Available prototype modifiers are:

- `.primary`
- `.danger`
- `.ghost`
- `.round`
- `.small`

Use links for navigation and buttons for actions.

## Forms

Wrap controls in `.field` and keep a visible label.

```html
<div class="field">
    <label for="module-name">Module name</label>
    <input class="input" id="module-name" name="module_name" aria-describedby="module-name-help">
    <small class="field-help" id="module-name-help">Use the official module title.</small>
</div>
```

Use `.input`, `.select` and `.textarea` for the matching controls. Use `.search-input` when the input has the prototype search icon treatment.

## Message banners

Django messages use a small production-only adapter around the prototype visual language.

```html
<div class="message-banner message-banner--success" role="status">
    <p>Your changes were saved.</p>
</div>
```

Available variants:

- `.message-banner--success`
- `.message-banner--warning`
- `.message-banner--error`

Message variants use a full border and subtle tinted background. They must never use a one-sided accent strip.

## Empty states

Use the exact prototype structure:

```html
<div class="empty-state">
    <div class="empty-icon" aria-hidden="true">
        <svg class="icon"><use href="#i-check"></use></svg>
    </div>
    <h3>No tasks yet</h3>
    <p>Create a task to begin planning your week.</p>
    <a class="button primary" href="/planning/">Open planning</a>
</div>
```

## Cards and layouts

Use the prototype classes directly:

- `.card`, `.card-header`, `.card-body`, `.card-footer`
- `.grid-2`, `.grid-3`, `.grid-4`
- `.layout-main-rail`, `.layout-rail-main`
- `.list`, `.list-item`, `.data-table`
- `.page-header`, `.page-header-copy`, `.page-actions`
- `.eyebrow`, `.muted`, `.subtle`

## Reference implementation

`core/templates/core/dashboard.html` demonstrates all issue #239 component categories without implementing the later dashboard feature:

- standard and primary buttons
- labelled search input and help text
- Django message banner styling
- prototype card and grid layout
- prototype empty state

## Accessibility checklist

- Navigate the component using only the keyboard.
- Keep a visible focus indicator.
- Give icon-only controls an accessible name.
- Keep form labels visible.
- Associate help and error text with the control.
- Hide decorative icons with `aria-hidden="true"`.
- Test at 320px width and 200% browser zoom.
- Run axe or an equivalent automated accessibility scan.
