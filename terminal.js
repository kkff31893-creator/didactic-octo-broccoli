const terminalOutput = document.querySelector('#terminal-output');
const terminalForm = document.querySelector('#terminal-form');
const terminalInput = document.querySelector('#terminal-input');
const commands = {
  help: 'COMMANDS\nabout — who I am\nskills — what I do\nprojects — selected work\nclear — clear terminal',
  about:
    'Dmitry Kamenskikh\nDesigner and frontend developer.\nI turn systems into expressive interfaces.',
  skills:
    'DEVELOPMENT  / interactive web, browser games\nDESIGN       / UI systems, motion\nEXPERIMENTS  / creative coding, AI',
  projects: '01 Quiet control\n02 Catch the signal\n03 Generative system',
};

function print(text, className = '') {
  const line = document.createElement('div');
  line.className = `terminal-line ${className}`;
  line.textContent = text;
  terminalOutput.append(line);
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

function run(command) {
  const value = command.trim().toLowerCase();
  if (!value) return;
  print(`visitor@dk › ${value}`, 'command');
  if (value === 'clear') terminalOutput.replaceChildren();
  else print(commands[value] || `Unknown command: ${value}\nType “help”.`);
}

terminalForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  run(terminalInput.value);
  terminalInput.value = '';
});
document
  .querySelectorAll('[data-command]')
  .forEach((button) =>
    button.addEventListener('click', () => run(button.dataset.command)),
  );
print('DK INTERACTIVE SHELL / READY\nType “help” to begin.', 'welcome');
