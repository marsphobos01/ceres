# Shared frontend components

## Design source

The shared frontend foundation is adapted from:

```text
Design/Mockups/application-prototype/
```

Use the prototype's semantic theme tokens, custom SVG icon shapes, rounded controls, restrained spacing and responsive shell. Do not replace the Ceres icons with emoji, Unicode symbols or unrelated icon libraries.

## Loading the component styles

`core/templates/base.html` loads all shared stylesheets, so pages extending `base.html` can use the classes directly.

```text
static/css/components/buttons.css
static/css/components/forms.css
static/css/components/messages.css
static/css/components/empty.css
```

## Buttons

Use `.button` as the base class.

```html
<button class="button button--primary" type="submit">Save changes</button>
<a class="button button--secondary" href="/calendar/">Open calendar</a>
<button class="button button--danger" type="button">Delete</button>
<button class="button button--ghost" type="button">Cancel</button>
<button class="button button--secondary" type="button" disabled>Unavailable</button>
```

Available modifiers:

- `.button--primary`
- `.button--secondary`
- `.button--danger`
- `.button--ghost`
- `.button--small`
- `.button--round`

Use a link when the control navigates and a button when it performs an action. Icon-only buttons must have an `aria-label`.

## Forms

Wrap each control in `.field`. Labels must remain visible.

```html
<div class="field">
    <label for="module-name">Module name</label>
    <input class="input" id="module-name" name="module_name" aria-describedby="module-name-help">
    <p class="field__help" id="module-name-help">Use the official module title.</p>
</div>
```

Use `.select` for select elements and `.textarea` for text areas.

For validation errors, add `.field--error`, set `aria-invalid="true"`, and associate the error with `aria-describedby`.

```html
<div class="field field--error">
    <label for="deadline">Deadline</label>
    <input class="input" id="deadline" name="deadline" aria-invalid="true" aria-describedby="deadline-error">
    <p class="field__error" id="deadline-error">Enter a valid date.</p>
</div>
```

## Message banners

Message banners communicate page-level feedback. Django messages are rendered automatically by `base.html`.

```html
<div class="message-banner message-banner--success" role="status">
    <p>Your changes were saved.</p>
</div>
```

Available variants:

- `.message-banner--success`
- `.message-banner--warning`
- `.message-banner--error`
- `.message-banner--info`

Use `role="status"` for routine feedback. Use `role="alert"` only when the message requires immediate attention.

## Empty states

Empty states explain why a section has no content and provide one useful next action.

```html
<div class="empty-state">
    <div class="empty-state__icon" aria-hidden="true">
        <svg class="icon"><use href="#i-check"></use></svg>
    </div>
    <h2>No tasks yet</h2>
    <p>Create a task to begin planning your week.</p>
    <a class="button button--primary" href="/tasks/new/">Create task</a>
</div>
```

Decorative empty-state icons must be hidden from assistive technology. Do not use colour alone to explain the state.

## Layout helpers

The base stylesheet includes:

- `.stack`, `.stack--sm`, `.stack--lg`, `.stack--xl`
- `.cluster`, `.cluster--between`
- `.grid`, `.grid--2`, `.grid--3`, `.grid--4`
- `.card`, `.card__header`, `.card__body`, `.card__footer`
- `.surface`, `.container`, `.muted`, `.subtle`, `.eyebrow`

Grid helpers collapse to one column on small screens.

## Reference implementation

`core/templates/core/dashboard.html` deliberately uses every shared component category without implementing the separate dashboard feature scope:

- buttons in the page actions and search form
- a labelled search form with help text
- an information message banner
- an empty state with a clear next action

## Accessibility checklist

Before merging a new component or variant:

- navigate it using only the keyboard
- verify a visible focus indicator
- verify text and control contrast in dark and light themes
- confirm labels and accessible names in the accessibility tree
- confirm validation messages are programmatically associated
- test at 320px width and at 200% browser zoom
- run axe or an equivalent automated accessibility scan
