# Accessibility

Funny Button is an intentionally playful experiment, not a recommended UI pattern for important decisions.

## Implemented

- The document declares Brazilian Portuguese (pt-BR).
- Native hyperlink and button controls remain focusable via keyboard.
- Visible keyboard-focus styling is provided.
- The "Não" button is evasive for pointer and touch interaction but responds to keyboard activation with a status message.
- The status message uses a live region.
- Viewport-constrained placement avoids losing the moved button offscreen after resize.
- Reduced-motion preferences disable nonessential transitions.
- Input targets are sized for touch use.

## Intentional limitation

Making a choice hard to select is not appropriate for consent, forms, purchases, account settings, or accessibility-critical interactions. Avoid reusing the evasive behavior in those contexts.

## Manual testing checklist

- Desktop mouse or trackpad: the button moves and remains onscreen.
- Touch: the button moves without activating unexpectedly.
- Keyboard: Tab reaches each control, and Enter/Space can activate the native button.
- Zoom and narrow screens: content and controls remain readable.
- Screen reader: the prompt, controls, and status make sense.
- Reduced motion: no unnecessary visual transition is required.
