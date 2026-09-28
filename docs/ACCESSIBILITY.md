# Accessibility

Funny-button is a playful interaction experiment, but the page should still remain understandable and operable across common input methods.

## Current considerations

- the document declares `pt-BR` as its language;
- the affirmative action is a native hyperlink;
- the negative action remains a native button element;
- touch input is handled explicitly;
- the moving button is constrained to the visible viewport;
- the page does not depend on animation libraries or scripted page transitions.

## Known limitation

The intentionally evasive negative button is hostile by design to direct activation. That behavior is the point of the experiment, so this repository should not be used as a pattern for consequential forms, consent interfaces, accessibility-critical workflows or production decision controls.

## Testing

When changing the interaction, verify the page at narrow and wide viewport sizes and test pointer, touch and keyboard behavior separately.
