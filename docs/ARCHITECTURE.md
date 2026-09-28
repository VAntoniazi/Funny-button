# Architecture

Funny-button is deliberately small: the runtime is a single static document with HTML, CSS and JavaScript.

## Interaction model

The page exposes two choices. The affirmative choice is a normal hyperlink. The negative button listens for pointer entry and touch input, calculates its own rendered dimensions, then chooses a new position constrained by the current viewport.

## Design constraints

- no framework or package runtime;
- no backend or persistent state;
- no network dependency for the interaction itself;
- touch and pointer input supported;
- viewport bounds calculated at interaction time;
- source remains readable without a build process.

## Automation

GitHub Actions is used only for repository maintenance and validation. Automation is not required to run the page.
