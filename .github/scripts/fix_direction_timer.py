from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = '    const standardCorrectDirection = 1;\n'
new = '    const standardCorrectDirection = -1;\n'
if old not in s:
    raise SystemExit('correct-direction constant not found')
s = s.replace(old, new, 1)

old = '''      timer = setInterval(() => {
        if (
          !gameActive ||
          gamePhase !== "playing" ||
          (motionEnabled && !isPhoneLandscape())
        ) {
          return;
        }

        timeRemaining -= 1;
        timeDisplay.textContent = timeRemaining;

        if (timeRemaining <= 0) {
          finishGame();
        }
      }, 1000);
'''
new = '''      timer = setInterval(() => {
        if (
          !gameActive ||
          !currentWord ||
          (motionEnabled && !isPhoneLandscape())
        ) {
          return;
        }

        timeRemaining -= 1;
        timeDisplay.textContent = timeRemaining;

        if (timeRemaining <= 0) {
          finishGame();
        }
      }, 1000);
'''
if old not in s:
    raise SystemExit('timer block not found')
s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')
