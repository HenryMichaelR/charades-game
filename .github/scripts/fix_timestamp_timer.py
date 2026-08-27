from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = '''    let timeRemaining = 60;
    let timer = null;
    let countdownTimeout = null;
'''
new = '''    let timeRemaining = 60;
    let timer = null;
    let roundEndsAt = null;
    let countdownTimeout = null;
'''
if old not in s:
    raise SystemExit('timer variable block not found')
s = s.replace(old, new, 1)

old = '''      timeRemaining = Number(timeSelect.value);
      currentWord = "";
      gameActive = true;
'''
new = '''      timeRemaining = Number(timeSelect.value);
      roundEndsAt = null;
      currentWord = "";
      gameActive = true;
'''
if old not in s:
    raise SystemExit('game reset block not found')
s = s.replace(old, new, 1)

old = '''      timer = setInterval(() => {
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
new = '''      timer = setInterval(() => {
        if (!gameActive || roundEndsAt === null) {
          return;
        }

        const millisecondsRemaining = roundEndsAt - Date.now();
        const nextTimeRemaining = Math.max(
          0,
          Math.ceil(millisecondsRemaining / 1000)
        );

        if (nextTimeRemaining !== timeRemaining) {
          timeRemaining = nextTimeRemaining;
          timeDisplay.textContent = timeRemaining;
        }

        if (millisecondsRemaining <= 0) {
          finishGame();
        }
      }, 200);
'''
if old not in s:
    raise SystemExit('old timer interval not found')
s = s.replace(old, new, 1)

old = '''      currentWord = availableWords.shift();
      wordCard.textContent = currentWord;
'''
new = '''      currentWord = availableWords.shift();
      wordCard.textContent = currentWord;

      if (roundEndsAt === null) {
        roundEndsAt = Date.now() + timeRemaining * 1000;
      }
'''
if old not in s:
    raise SystemExit('showNextWord assignment not found')
s = s.replace(old, new, 1)

old = '''      gameActive = false;
      gamePhase = "finished";
      clearInterval(timer);
'''
new = '''      gameActive = false;
      gamePhase = "finished";
      roundEndsAt = null;
      clearInterval(timer);
'''
if old not in s:
    raise SystemExit('finishGame block not found')
s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')
