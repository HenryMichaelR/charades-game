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
    '        <option value="120">2 minutes</option>\n',
    '        <option value="120">2 minutes</option>\n'
    '        <option value="180">3 minutes</option>\n'
    '        <option value="300">5 minutes</option>\n',
    "time options",
)

replace_once(
    '''    function playSkipSound() {
      if (!audioContext) {
        return;
      }

      const now = audioContext.currentTime;
      playTone(330, now, 0.18);
      playTone(220, now + 0.14, 0.25);
    }

    function showAnswerFeedback(wasCorrect) {''',
    '''    function playSkipSound() {
      if (!audioContext) {
        return;
      }

      const now = audioContext.currentTime;
      playTone(330, now, 0.18);
      playTone(220, now + 0.14, 0.25);
    }

    function vibratePhone(pattern) {
      if (!("vibrate" in navigator)) {
        return;
      }

      try {
        navigator.vibrate(pattern);
      } catch (error) {
        console.info("Phone vibration was not available:", error);
      }
    }

    function playTimeUpSound() {
      initializeAudio();

      if (!audioContext) {
        return;
      }

      const now = audioContext.currentTime;
      playTone(784, now, 0.28, 0.42);
      playTone(784, now + 0.38, 0.28, 0.42);
      playTone(784, now + 0.76, 0.28, 0.42);
      playTone(523, now + 1.14, 0.65, 0.5);
    }

    function signalTimeUp() {
      vibratePhone([250, 100, 250, 100, 500]);
      playTimeUpSound();
    }

    function showAnswerFeedback(wasCorrect) {''',
    "feedback helper",
)

replace_once(
    '''          timeRemaining = 0;
          timeDisplay.textContent = "0";
          finishGame();
          return;''',
    '''          timeRemaining = 0;
          timeDisplay.textContent = "0";
          finishGame({ reason: "timer" });
          return;''',
    "animation-frame timer completion",
)

replace_once(
    '''        timeRemaining = 0;
        timeDisplay.textContent = "0";
        finishGame();
      }, durationMs + 100);''',
    '''        timeRemaining = 0;
        timeDisplay.textContent = "0";
        finishGame({ reason: "timer" });
      }, durationMs + 100);''',
    "timeout timer completion",
)

replace_once(
    '''      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }''',
    '''      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);
    }''',
    "tilt-only vibration",
)

replace_once(
    '''      results.push({
        word: currentWord,
        correct: wasCorrect
      });

      if (wasCorrect) {''',
    '''      results.push({
        word: currentWord,
        correct: wasCorrect
      });

      vibratePhone(wasCorrect ? 120 : [70, 60, 70]);

      if (wasCorrect) {''',
    "shared answer vibration",
)

replace_once(
    '''      if (availableWords.length === 0) {
        finishGame();
        return;
      }''',
    '''      if (availableWords.length === 0) {
        finishGame({ reason: "words-exhausted" });
        return;
      }''',
    "word exhaustion finish",
)

replace_once(
    '''      finishGame();
    }

    function finishGame() {
      if (!gameActive) {
        return;
      }

      gameActive = false;
      gamePhase = "finished";
      timerStarted = false;
      stopRoundTimer();
      clearTimeout(countdownTimeout);
      clearInterval(orientationPollTimer);

      document.body.classList.remove("motion-game", "portrait-mode");
      gameScreen.classList.add("hidden");
      resultsScreen.classList.remove("hidden");
      finalScoreDisplay.textContent = score;
      resultsList.innerHTML = "";

      if (results.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "No words were answered.";
        resultsList.appendChild(emptyItem);
        return;
      }

      results.forEach((result) => {
        const listItem = document.createElement("li");
        listItem.textContent =
          `${result.correct ? "Correct" : "Skipped"}: ${result.word}`;
        listItem.className =
          result.correct ? "correct-result" : "skip-result";
        resultsList.appendChild(listItem);
      });
    }''',
    '''      finishGame({ reason: "exit" });
    }

    function finishGame({ reason = "exit" } = {}) {
      if (!gameActive) {
        return;
      }

      const shouldRecordCurrentWord =
        (reason === "timer" || reason === "exit") && Boolean(currentWord);

      if (shouldRecordCurrentWord) {
        const lastResult = results[results.length - 1];
        const currentWordAlreadyRecorded =
          lastResult && lastResult.word === currentWord;

        if (!currentWordAlreadyRecorded) {
          results.push({
            word: currentWord,
            correct: false
          });
        }
      }

      if (reason === "timer") {
        signalTimeUp();
      }

      gameActive = false;
      gamePhase = "finished";
      timerStarted = false;
      stopRoundTimer();
      clearTimeout(countdownTimeout);
      clearInterval(orientationPollTimer);

      document.body.classList.remove("motion-game", "portrait-mode");
      gameScreen.classList.add("hidden");
      resultsScreen.classList.remove("hidden");
      finalScoreDisplay.textContent = score;
      resultsList.innerHTML = "";

      if (results.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "No words were answered.";
        resultsList.appendChild(emptyItem);
        currentWord = "";
        return;
      }

      results.forEach((result) => {
        const listItem = document.createElement("li");
        listItem.textContent =
          `${result.correct ? "Correct" : "Skipped"}: ${result.word}`;
        listItem.className =
          result.correct ? "correct-result" : "skip-result";
        resultsList.appendChild(listItem);
      });

      currentWord = "";
    }''',
    "exit and finish functions",
)

if text == original:
    raise SystemExit("No changes were made")

path.write_text(text, encoding="utf-8")
print("Added answer haptics, long timers, time-up alert, and final-word logging")
