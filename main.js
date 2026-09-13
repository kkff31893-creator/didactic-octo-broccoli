const progress = document.querySelector('.scroll-progress');
function updateProgress() {
  const range = document.documentElement.scrollHeight - innerHeight;
  progress.style.transform = `scaleX(${range > 0 ? scrollY / range : 0})`;
}
addEventListener('scroll', updateProgress, { passive: true });
addEventListener('resize', updateProgress);
updateProgress();

const modes = {
  focus: {
    text: 'One thing. Full attention.',
    index: 'MODE / 01',
    bars: [34, 52, 75, 42, 88, 64, 92, 55, 70, 46, 82, 61],
  },
  explore: {
    text: 'Follow the useful surprise.',
    index: 'MODE / 02',
    bars: [72, 44, 91, 62, 38, 79, 54, 86, 43, 68, 95, 57],
  },
  rest: {
    text: 'Less input. More perspective.',
    index: 'MODE / 03',
    bars: [25, 30, 22, 36, 28, 34, 20, 32, 26, 38, 24, 29],
  },
};
const modeButtons = document.querySelectorAll('[data-mode]');
const chartBars = document.querySelectorAll('#activity-chart i');
modeButtons.forEach((button) =>
  button.addEventListener('click', () => {
    const mode = modes[button.dataset.mode];
    modeButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle('selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    document.querySelector('#mode-description').textContent = mode.text;
    document.querySelector('#mode-index').textContent = mode.index;
    chartBars.forEach((bar, index) => {
      bar.style.height = `${mode.bars[index]}%`;
    });
  }),
);
modeButtons[0]?.click();

const game = document.querySelector('#game-field');
const gameIntro = document.querySelector('#game-intro');
const gameTarget = document.querySelector('#game-target');
const gameScore = document.querySelector('#game-score');
const gameTime = document.querySelector('#game-time');
const gameResult = document.querySelector('#game-result');
let score = 0;
let gameTimer;

function moveTarget() {
  const margin = 26;
  const maxX = Math.max(
    margin,
    game.clientWidth - gameTarget.offsetWidth - margin,
  );
  const maxY = Math.max(
    margin,
    game.clientHeight - gameTarget.offsetHeight - margin,
  );
  gameTarget.style.left = `${margin + Math.random() * (maxX - margin)}px`;
  gameTarget.style.top = `${margin + Math.random() * (maxY - margin)}px`;
}

function finishGame() {
  clearInterval(gameTimer);
  game.classList.remove('is-playing');
  gameTarget.hidden = true;
  gameIntro.hidden = false;
  gameResult.textContent = `RESULT / ${String(score).padStart(2, '0')} SIGNALS`;
}

document.querySelector('#game-start')?.addEventListener('click', () => {
  clearInterval(gameTimer);
  score = 0;
  let seconds = 20;
  gameScore.textContent = '00';
  gameTime.textContent = seconds;
  gameResult.textContent = '';
  gameIntro.hidden = true;
  gameTarget.hidden = false;
  game.classList.add('is-playing');
  moveTarget();
  gameTimer = setInterval(() => {
    seconds -= 1;
    gameTime.textContent = seconds;
    if (seconds <= 0) finishGame();
  }, 1000);
});
gameTarget?.addEventListener('click', () => {
  score += 1;
  gameScore.textContent = String(score).padStart(2, '0');
  moveTarget();
});

const canvas = document.querySelector('#pattern-canvas');
const density = document.querySelector('#pattern-density');
const seedLabel = document.querySelector('#pattern-seed');
let seed = 1;
function random(index) {
  const value = Math.sin(seed * 91.7 + index * 47.13) * 43758.5453;
  return value - Math.floor(value);
}
function drawPattern() {
  const rect = canvas.getBoundingClientRect();
  const ratio = Math.min(devicePixelRatio || 1, 2);
  canvas.width = Math.max(1, Math.round(rect.width * ratio));
  canvas.height = Math.max(1, Math.round(rect.height * ratio));
  const context = canvas.getContext('2d');
  context.scale(ratio, ratio);
  context.clearRect(0, 0, rect.width, rect.height);
  context.strokeStyle = '#344526';
  context.lineWidth = 1;
  const count = Number(density.value);
  for (let index = 0; index < count; index++) {
    const x = ((index + 0.5) * rect.width) / count;
    const shift = (random(index) - 0.5) * 55;
    context.beginPath();
    context.moveTo(x, 18);
    context.bezierCurveTo(
      x + shift,
      rect.height * 0.32,
      x - shift,
      rect.height * 0.68,
      x + shift * 0.3,
      rect.height - 18,
    );
    context.stroke();
    if (random(index + 100) > 0.72) {
      context.fillStyle = '#20271a';
      context.fillRect(
        x - 2,
        20 + random(index + 200) * (rect.height - 44),
        4,
        4,
      );
    }
  }
}
density?.addEventListener('input', drawPattern);
document.querySelector('#regenerate-pattern')?.addEventListener('click', () => {
  seed = 1 + Math.floor(Math.random() * 999);
  seedLabel.textContent = String(seed).padStart(3, '0');
  drawPattern();
});
new ResizeObserver(drawPattern).observe(canvas);
