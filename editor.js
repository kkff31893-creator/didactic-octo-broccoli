const initialFiles = {
  html: `<main class="demo-card">
  <span>INTERACTION / 01</span>
  <h1>Make it tangible.</h1>
  <p>Change this code and watch the result.</p>
  <button id="demo-button">Activate</button>
  <strong id="demo-state">Waiting.</strong>
</main>`,
  css: `body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: #dce0d3;
  color: #20261c;
  font-family: Arial, sans-serif;
}
.demo-card { width: min(76%, 430px); }
.demo-card span { font: 10px Consolas, monospace; }
.demo-card h1 { font-size: clamp(38px, 7vw, 72px); line-height: .9; letter-spacing: -.06em; }
.demo-card p { color: #5e6856; line-height: 1.6; }
.demo-card button { padding: 12px 18px; border: 0; background: #20261c; color: #dce0d3; cursor: pointer; }
.demo-card strong { margin-left: 14px; font: 11px Consolas, monospace; }`,
  js: `const button = document.querySelector('#demo-button');
const state = document.querySelector('#demo-state');
let active = false;
button.addEventListener('click', () => {
  active = !active;
  state.textContent = active ? 'Active.' : 'Waiting.';
  button.textContent = active ? 'Reset' : 'Activate';
});`,
};
let files = { ...initialFiles };
let activeFile = 'css';
let previewTimer;
const input = document.querySelector('#code-input');
const highlight = document.querySelector('#highlight');
const lineNumbers = document.querySelector('#line-numbers');
const preview = document.querySelector('#live-preview');
const stateLabel = document.querySelector('#editor-state');

function renderPreview() {
  const safeScript = files.js.replace(/<\/script/gi, '<\\/script');
  preview.srcdoc = `<!doctype html><html><head><meta charset="utf-8"><style>${files.css}</style></head><body>${files.html}<script>${safeScript}<\/script></body></html>`;
  stateLabel.textContent = 'Preview updated';
}

function renderEditor() {
  input.value = files[activeFile];
  highlight.textContent = files[activeFile];
  lineNumbers.textContent = files[activeFile]
    .split('\n')
    .map((_, index) => index + 1)
    .join('\n');
  document.querySelector('#file-language').textContent =
    activeFile.toUpperCase();
  document
    .querySelector('#code-panel')
    .setAttribute('aria-labelledby', `tab-${activeFile}`);
  input.setAttribute(
    'aria-label',
    `Редактировать ${document.querySelector(`[data-file="${activeFile}"]`).textContent}`,
  );
  input.scrollTop = 0;
  input.scrollLeft = 0;
  highlight.scrollTop = 0;
  highlight.scrollLeft = 0;
}

document.querySelectorAll('[data-file]').forEach((tab) =>
  tab.addEventListener('click', () => {
    activeFile = tab.dataset.file;
    document.querySelectorAll('[data-file]').forEach((item) => {
      const selected = item === tab;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    renderEditor();
  }),
);

input?.addEventListener('input', () => {
  files[activeFile] = input.value;
  highlight.textContent = input.value;
  lineNumbers.textContent = input.value
    .split('\n')
    .map((_, index) => index + 1)
    .join('\n');
  stateLabel.textContent = 'Editing…';
  clearTimeout(previewTimer);
  previewTimer = setTimeout(renderPreview, 280);
});
input?.addEventListener('scroll', () => {
  highlight.scrollTop = input.scrollTop;
  highlight.scrollLeft = input.scrollLeft;
  lineNumbers.scrollTop = input.scrollTop;
});
document.querySelector('#replay-code')?.addEventListener('click', () => {
  files = { ...initialFiles };
  renderEditor();
  renderPreview();
});

renderEditor();
renderPreview();
