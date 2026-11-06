import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import vm from 'node:vm';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];

function createPage({ width = 390, height = 844, random = 0.65 } = {}) {
  const handlers = new Map();
  const windowHandlers = new Map();
  const state = new Set();
  const button = {
    style: {},
    classList: { add: (name) => state.add(name), contains: (name) => state.has(name) },
    getBoundingClientRect: () => ({ width: 110, height: 52 }),
    addEventListener: (name, handler) => handlers.set(name, handler)
  };
  const feedback = { textContent: '' };
  const document = {
    documentElement: { clientWidth: width },
    getElementById: (id) => ({ 'no-button': button, feedback })[id]
  };
  const window = {
    innerHeight: height,
    visualViewport: null,
    addEventListener: (name, handler) => windowHandlers.set(name, handler)
  };
  const math = Object.create(Math);
  math.random = () => random;
  vm.runInNewContext(script, { document, window, Math: math });
  return { button, feedback, document, window, handlers, windowHandlers };
}

test('static document has semantic controls and the original affirmative destination', () => {
  assert.match(html, /<html lang="pt-BR">/);
  assert.match(html, /name="viewport"/);
  assert.match(html, /href="https:\/\/www\.youtube\.com\/watch\?v=thJ0sUR_sWg"/);
  assert.match(html, /id="no-button" type="button"/);
  assert.ok(script);
});

test('mouse movement keeps the playful button inside viewport bounds', () => {
  const page = createPage();
  page.handlers.get('pointerenter')({ pointerType: 'mouse', clientX: 135, clientY: 250 });
  assert.ok(page.button.classList.contains('is-escaping'));
  const x = parseFloat(page.button.style.left);
  const y = parseFloat(page.button.style.top);
  assert.ok(x >= 0 && x <= 390 - 110, 'x within viewport');
  assert.ok(y >= 0 && y <= 844 - 52, 'y within viewport');
});

test('touch uses a single escape path and prevents accidental activation', () => {
  const page = createPage();
  page.handlers.get('pointerenter')({ pointerType: 'touch', clientX: 100, clientY: 100 });
  assert.equal(page.button.style.left, undefined);
  let prevented = false;
  page.handlers.get('touchstart')({
    cancelable: true,
    preventDefault() { prevented = true; },
    touches: [{ clientX: 100, clientY: 100 }]
  });
  assert.ok(prevented);
  assert.ok(page.button.classList.contains('is-escaping'));
});

test('viewport resize reclamps the button to the visible area', () => {
  const page = createPage();
  page.handlers.get('pointerenter')({ pointerType: 'mouse', clientX: 60, clientY: 60 });
  page.document.documentElement.clientWidth = 200;
  page.window.innerHeight = 140;
  page.windowHandlers.get('resize')();
  assert.ok(parseFloat(page.button.style.left) <= 90);
  assert.ok(parseFloat(page.button.style.top) <= 88);
});

test('keyboard activation can still select no and receive feedback', () => {
  const page = createPage();
  page.handlers.get('click')();
  assert.match(page.feedback.textContent, /convite continua aberto/);
});
