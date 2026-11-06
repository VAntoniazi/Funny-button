# Funny Button

[![Validate static project](https://github.com/VAntoniazi/Funny-button/actions/workflows/validate.yml/badge.svg)](https://github.com/VAntoniazi/Funny-button/actions/workflows/validate.yml)
![No dependencies](https://img.shields.io/badge/dependencies-none-6c34a4)
![MIT License](https://img.shields.io/badge/license-MIT-blue)

A playful, responsive **cinema invitation** built with vanilla HTML, CSS, and JavaScript. One button says yes. The other is a little harder to catch.

## Features

- **Zero runtime dependencies:** open a single HTML file to run the project.
- **Responsive design:** a centered invitation card for desktop and mobile screens.
- **Pointer and touch interactions:** the evasive button moves to a random position inside the visible viewport.
- **Viewport-aware movement:** on resize, the button is kept on screen.
- **Keyboard considerations:** native controls remain focusable; activating “Não” with a keyboard provides feedback.
- **Reduced-motion support:** unnecessary transitions are disabled when the user prefers reduced motion.
- **Automated checks:** dependency-free interaction tests using Node.js built-ins.

## Run locally

Clone this repository, then open index.html in your browser:

~~~bash
git clone https://github.com/VAntoniazi/Funny-button.git
cd Funny-button
~~~

No installation or build process is required. You can also serve it locally using Python:

~~~bash
python3 -m http.server 8000
~~~

Then visit http://localhost:8000.

## Test

Node.js 22 or newer is recommended for reproducible CI parity:

~~~bash
node --test tests/*.test.mjs
~~~

## Structure

~~~text
index.html              # The complete static web experience
tests/interaction.test.mjs
.github/workflows/validate.yml
docs/                   # Architecture and accessibility notes
~~~

## Accessibility

The moving “Não” button is deliberately evasive for pointer and touch users. This is a **playful interaction demo**, not a UI pattern for forms, consent, purchases, or other consequential decisions. See [accessibility notes](docs/ACCESSIBILITY.md).

## Contributing and license

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. Licensed under [MIT](LICENSE).
