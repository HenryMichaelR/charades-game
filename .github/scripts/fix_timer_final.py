from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = '''    let timeRemaining = 60;
    let timer = null;
    let roundEndsAt = null;
    let countdownTimeout = null;
'''
new = '''    let timeRemaining = 60;
    let timerAnimationFrame = null;
    let timerEndTimeout = null;
    let timerStarted = false;
    let countdownTimeout = null;
'''
if old not in s:
    raise SystemExit('timer variable block not found')
s = s.replace(old, new, 1)

s = s.replace('      clearInterval(timer);', '      stopRoundTimer();')

old_begin = '''    function beginRound() {
      if (!gameActive) {
        return;
      }

      stopRoundTimer();
      resetMotionState();
      lastScreenAngle = getScreenAngle();

      if (testMode) {
        gamePhase = "playing";
        answerArmed = true;
        gameInstructions.textContent = "Use the test buttons below";
        showNextWord();
      } else {
        beginAutomaticCentering(false);
      }

      timer = setInterval(() => {
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
    }
'''
new_begin = '''    function stopRoundTimer() {
      if (timerAnimationFrame !== null) {
        cancelAnimationFrame(timerAnimationFrame);
        timerAnimationFrame = null;
      }

      if (timerEndTimeout !== null) {
        clearTimeout(timerEndTimeout);
        timerEndTimeout = null;
      }
    }

    function startRoundTimer() {
      if (timerStarted || !gameActive) {
        return;
      }

      timerStarted = true;
      stopRoundTimer();

      const durationMs = timeRemaining * 1000;
      const endsAt = Date.now() + durationMs;

      function drawTimer() {
        if (!gameActive || !timerStarted) {
          return;
        }

        const millisecondsRemaining = endsAt - Date.now();
        const displayedSeconds = Math.max(
          0,
          Math.ceil(millisecondsRemaining / 1000)
        );

        if (displayedSeconds !== timeRemaining) {
          timeRemaining = displayedSeconds;
          timeDisplay.textContent = String(displayedSeconds);
        }

        if (millisecondsRemaining <= 0) {
          timeRemaining = 0;
          timeDisplay.textContent = "0";
          finishGame();
          return;
        }

        timerAnimationFrame = requestAnimationFrame(drawTimer);
      }

      timeDisplay.textContent = String(timeRemaining);
      timerAnimationFrame = requestAnimationFrame(drawTimer);

      timerEndTimeout = setTimeout(() => {
        if (!gameActive || !timerStarted) {
          return;
        }

        timeRemaining = 0;
        timeDisplay.textContent = "0";
        finishGame();
      }, durationMs + 100);
    }

    function beginRound() {
      if (!gameActive) {
        return;
      }

      stopRoundTimer();
      timerStarted = false;
      resetMotionState();
      lastScreenAngle = getScreenAngle();

      if (testMode) {
        gamePhase = "playing";
        answerArmed = true;
        gameInstructions.textContent = "Use the test buttons below";
        showNextWord();
      } else {
        beginAutomaticCentering(false);
      }
    }
'''
if old_begin not in s:
    raise SystemExit('beginRound timer block not found')
s = s.replace(old_begin, new_begin, 1)

old_show = '''      currentWord = availableWords.shift();
      wordCard.textContent = currentWord;

      if (roundEndsAt === null) {
        roundEndsAt = Date.now() + timeRemaining * 1000;
      }
'''
new_show = '''      currentWord = availableWords.shift();
      wordCard.textContent = currentWord;
      startRoundTimer();
'''
if old_show not in s:
    raise SystemExit('showNextWord timer block not found')
s = s.replace(old_show, new_show, 1)

s = s.replace('      roundEndsAt = null;\n      stopRoundTimer();', '      timerStarted = false;\n      stopRoundTimer();')

old_start_state = '''      score = 0;
      timeRemaining = Number(timeSelect.value);
      roundEndsAt = null;
      currentWord = "";
      gameActive = true;
'''
new_start_state = '''      score = 0;
      timeRemaining = Number(timeSelect.value);
      timerStarted = false;
      stopRoundTimer();
      currentWord = "";
      gameActive = true;
'''
if old_start_state not in s:
    raise SystemExit('new-game timer state block not found')
s = s.replace(old_start_state, new_start_state, 1)

if 'roundEndsAt' in s:
    raise SystemExit('roundEndsAt remains after patch')
if 'timer = setInterval' in s:
    raise SystemExit('old interval timer remains')

path.write_text(s, encoding='utf-8')
