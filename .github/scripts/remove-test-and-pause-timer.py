from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one {label} block, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    '''    .primary-button,
    .secondary-button {
      width: 100%;
      border-radius: 14px;
      font-size: 18px;
      font-weight: bold;
    }''',
    '''    .primary-button {
      width: 100%;
      border-radius: 14px;
      font-size: 18px;
      font-weight: bold;
    }''',
    "shared button styles",
)

replace_once(
    '''
    .secondary-button {
      margin-top: 12px;
      padding: 14px;
      border: 2px solid #2563eb;
      background: white;
      color: #2563eb;
    }
''',
    "\n",
    "secondary button styles",
)

replace_once(
    '''
    .test-controls {
      display: none;
      margin-top: 12px;
      gap: 10px;
    }

    .test-controls button {
      flex: 1;
      padding: 12px;
      border: none;
      border-radius: 12px;
      font-weight: bold;
    }

    .test-skip {
      background: #f59e0b;
      color: white;
    }

    .test-correct {
      background: #16a34a;
      color: white;
    }
''',
    "\n",
    "test control styles",
)

replace_once(
    '''
      <button
        id="testButton"
        class="secondary-button"
        type="button"
        onclick="startTestGame()"
      >
        Test on Computer
      </button>
''',
    "\n",
    "computer test button",
)

replace_once(
    '''
      <div id="testControls" class="test-controls">
        <button class="test-skip" type="button" onclick="answerWord(false)">
          Test Skip
        </button>

        <button class="test-correct" type="button" onclick="answerWord(true)">
          Test Correct
        </button>
      </div>
''',
    "\n",
    "test answer controls",
)

replace_once(
    '    const testControls = document.getElementById("testControls");\n',
    "",
    "test controls element",
)

replace_once(
    '''    let timerAnimationFrame = null;
    let timerEndTimeout = null;
    let timerStarted = false;''',
    '''    let timerAnimationFrame = null;
    let timerStarted = false;
    let timerRemainingMs = 0;
    let timerLastTickAt = null;
    let timerPausedForOrientation = false;''',
    "timer state variables",
)

replace_once(
    '''    let motionEnabled = false;
    let testMode = false;''',
    '''    let motionEnabled = false;''',
    "test mode state",
)

replace_once(
    '''        motionEnabled = true;
        testMode = false;
        motionMessage.textContent = "Motion controls enabled.";''',
    '''        motionEnabled = true;
        motionMessage.textContent = "Motion controls enabled.";''',
    "motion start state",
)

replace_once(
    '''
    function startTestGame() {
      initializeAudio();
      motionEnabled = false;
      testMode = true;
      motionMessage.textContent = "";
      startGame();
    }
''',
    "\n",
    "test game function",
)

replace_once(
    '      testControls.style.display = testMode ? "flex" : "none";\n',
    "",
    "test controls display",
)

replace_once(
    '''      if (testMode) {
        beginRound();
      } else {
        beginCountdown();
      }''',
    '''      beginCountdown();''',
    "test start branch",
)

old_timer = '''    function stopRoundTimer() {
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
          finishGame({ reason: "timer" });
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
        finishGame({ reason: "timer" });
      }, durationMs + 100);
    }'''

new_timer = '''    function stopRoundTimer() {
      if (timerAnimationFrame !== null) {
        cancelAnimationFrame(timerAnimationFrame);
        timerAnimationFrame = null;
      }

      timerLastTickAt = null;
      timerPausedForOrientation = false;
    }

    function roundTimerCanRun() {
      return (
        (!motionEnabled || isPhoneLandscape()) &&
        gamePhase !== "centering"
      );
    }

    function drawRoundTimer(timestamp) {
      timerAnimationFrame = null;

      if (!gameActive || !timerStarted) {
        return;
      }

      if (!roundTimerCanRun()) {
        timerPausedForOrientation = true;
        timerLastTickAt = null;
        timerAnimationFrame = requestAnimationFrame(drawRoundTimer);
        return;
      }

      if (timerPausedForOrientation || timerLastTickAt === null) {
        timerPausedForOrientation = false;
        timerLastTickAt = timestamp;
      } else {
        timerRemainingMs -= timestamp - timerLastTickAt;
        timerLastTickAt = timestamp;
      }

      const displayedSeconds = Math.max(
        0,
        Math.ceil(timerRemainingMs / 1000)
      );

      if (displayedSeconds !== timeRemaining) {
        timeRemaining = displayedSeconds;
        timeDisplay.textContent = String(displayedSeconds);
      }

      if (timerRemainingMs <= 0) {
        timerRemainingMs = 0;
        timeRemaining = 0;
        timeDisplay.textContent = "0";
        finishGame({ reason: "timer" });
        return;
      }

      timerAnimationFrame = requestAnimationFrame(drawRoundTimer);
    }

    function startRoundTimer() {
      if (timerStarted || !gameActive) {
        return;
      }

      timerStarted = true;
      stopRoundTimer();
      timerRemainingMs = timeRemaining * 1000;
      timerLastTickAt = null;
      timerPausedForOrientation = !roundTimerCanRun();
      timeDisplay.textContent = String(timeRemaining);
      timerAnimationFrame = requestAnimationFrame(drawRoundTimer);
    }'''

replace_once(old_timer, new_timer, "round timer implementation")

replace_once(
    '''      if (testMode) {
        gamePhase = "playing";
        answerArmed = true;
        gameInstructions.textContent = "Use the test buttons below";
        showNextWord();
      } else {
        beginAutomaticCentering(false);
      }''',
    '''      beginAutomaticCentering(false);''',
    "test begin-round branch",
)

replace_once(
    '      if (motionEnabled && !testMode) {',
    '      if (motionEnabled) {',
    "test answer branch",
)

replace_once(
    '''      document.body.classList.toggle(
        "portrait-mode",
        portraitBlocked
      );
    }''',
    '''      document.body.classList.toggle(
        "portrait-mode",
        portraitBlocked
      );

      if (portraitBlocked && timerStarted) {
        timerPausedForOrientation = true;
        timerLastTickAt = null;
      }
    }''',
    "orientation timer pause",
)

if text == original:
    raise SystemExit("No changes were made")

path.write_text(text, encoding="utf-8")
print("Removed computer test mode and added true landscape timer pausing")
