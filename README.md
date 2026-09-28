# Funny-button

A tiny, dependency-free front-end experiment built around one intentionally evasive button.

The page asks a simple question: **“Cineminha sexta?”** The **Sim** button behaves normally; the **Não** button escapes the pointer and touch input while remaining constrained to the viewport.

## Why this exists

This repository is a small interaction experiment for practicing:

- DOM event handling;
- pointer and touch interactions;
- viewport-aware positioning;
- responsive behavior without frameworks;
- progressive enhancement in plain HTML, CSS and JavaScript.

## Features

- no dependencies;
- no build step;
- works with mouse and touch input;
- moving button stays inside the visible viewport;
- explicit Portuguese document language;
- small enough to inspect in a single file.

## Run locally

Clone the repository or download it, then open `index.html` directly in a browser.

```bash
git clone https://github.com/VAntoniazi/Funny-button.git
cd Funny-button
```

Then open `index.html`.

## Project structure

```text
.
├── index.html
├── README.md
└── LICENSE
```

The GitHub Actions files under `.github/` are repository automation and are not required to run the page.

## License

MIT.
