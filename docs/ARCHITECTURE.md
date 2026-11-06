# Architecture

Funny Button is a dependency-free static browser experiment. The runtime lives in index.html, with semantic HTML, embedded CSS, and plain JavaScript.

## Interaction model

The affirmative choice is a normal hyperlink (to an external YouTube video). The negative choice is a native button that moves when approached with a mouse or tapped on a touch display. Positions are calculated from the visible viewport and actual button dimensions; the button is clamped after viewport resizes.

Keyboard users can focus and activate either native control. Activating the negative button produces a small live-region message rather than forcing a navigation.

## Constraints

- no framework, package manager, build tooling, backend, or local storage;
- no runtime network requests before a user opens a link;
- support narrow viewports, pointer input, touch input, and keyboard use;
- respect reduced-motion preferences;
- keep the code readable and reviewable.

## Validation

Tests in tests/interaction.test.mjs use the built-in Node.js test runner and a minimal DOM stub. CI validates the markup contract and key interaction behavior on pushes to main and pull requests. Manual visual checks remain valuable for different browsers and touch devices.
