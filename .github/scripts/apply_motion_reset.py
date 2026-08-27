from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

text = text.replace(
    """    let currentTilt = null;
    let neutralTilt = null;
    let tiltLocked = true;
    let calibrationEndsAt = 0;
    let calibrationBaseTilt = null;
    let lastScreenAngle = null;
    let correctDirection = 1;
""",
    """    let currentTilt = null;
    let filteredTilt = null;
    let neutralTilt = null;
    let tiltLocked = true;
    let calibrationEndsAt = 0;
    let calibrationBaseTilt = null;
    let lastScreenAngle = null;
    let correctDirection = 1;
    let answerCooldownEndsAt = 0;
    let resetStartedAt = null;
""",
    1,
)

text = text.replace(
    """    const correctTiltAmount = 26;
    const skipTiltAmount = 26;
    const calibrationTiltAmount = 18;
    const neutralZone = 10;
""",
    """    const correctTiltAmount = 22;
    const skipTiltAmount = 22;
    const calibrationTiltAmount = 16;
    const neutralZone = 13;
    const tiltSmoothing = 0.45;
    const answerCooldownMs = 650;
    const resetHoldMs = 500;
""",
    1,
)

text = text.replace(
    """    function beginDirectionCalibration() {
      gamePhase = "calibrating";
      currentTilt = null;
      neutralTilt = null;
      calibrationBaseTilt = null;
      tiltLocked = true;
""",
    """    function beginDirectionCalibration() {
      gamePhase = "calibrating";
      currentTilt = null;
      filteredTilt = null;
      neutralTilt = null;
      calibrationBaseTilt = null;
      resetStartedAt = null;
      tiltLocked = true;
""",
    1,
)

old_recalibrate = """    function recalibrateTilt() {
      currentTilt = null;
      neutralTilt = null;
      tiltLocked = true;
      calibrationEndsAt = Date.now() + 700;
      lastScreenAngle = getScreenAngle();
    }
"""
new_recalibrate = """    function recalibrateTilt() {
      currentTilt = null;
      filteredTilt = null;
      neutralTilt = null;
      resetStartedAt = null;
      tiltLocked = true;
      calibrationEndsAt = Date.now() + 700;
      lastScreenAngle = getScreenAngle();
    }

    function smoothTilt(tiltValue) {
      if (filteredTilt === null) {
        filteredTilt = tiltValue;
      } else {
        filteredTilt +=
          (tiltValue - filteredTilt) * tiltSmoothing;
      }

      return filteredTilt;
    }
"""
if old_recalibrate not in text:
    raise SystemExit("recalibrate block not found")
text = text.replace(old_recalibrate, new_recalibrate, 1)

text = text.replace(
    """      currentTilt = tiltValue;

      if (gamePhase === "calibrating") {
        handleCalibrationTilt(tiltValue);
        return;
      }
""",
    """      currentTilt = smoothTilt(tiltValue);

      if (gamePhase === "calibrating") {
        handleCalibrationTilt(currentTilt);
        return;
      }
""",
    1,
)

old_returning = """      if (gamePhase === "returning") {
        if (
          neutralTilt !== null &&
          Math.abs(tiltValue - neutralTilt) <= neutralZone
        ) {
          beginCountdown();
        }

        return;
      }

      if (gamePhase !== "playing") {
        return;
      }
"""
new_returning = """      if (gamePhase === "returning") {
        if (
          neutralTilt !== null &&
          Math.abs(currentTilt - neutralTilt) <= neutralZone
        ) {
          beginCountdown();
        }

        return;
      }

      if (gamePhase === "resetting") {
        if (Date.now() < answerCooldownEndsAt) {
          resetStartedAt = null;
          return;
        }

        const resetDifference =
          (currentTilt - neutralTilt) * correctDirection;

        if (Math.abs(resetDifference) <= neutralZone) {
          if (resetStartedAt === null) {
            resetStartedAt = Date.now();
          }

          if (Date.now() - resetStartedAt >= resetHoldMs) {
            neutralTilt = currentTilt;
            filteredTilt = currentTilt;
            tiltLocked = false;
            resetStartedAt = null;
            gamePhase = "playing";
            gameInstructions.textContent =
              "Ready — top edge DOWN = Correct • top edge UP = Skip";
            showNextWord();
          }
        } else {
          resetStartedAt = null;
        }

        return;
      }

      if (gamePhase !== "playing") {
        return;
      }
"""
if old_returning not in text:
    raise SystemExit("returning block not found")
text = text.replace(old_returning, new_returning, 1)

old_register = """    function registerTiltAnswer(wasCorrect) {
      if (tiltLocked || !gameActive || gamePhase !== "playing") {
        return;
      }

      tiltLocked = true;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }
"""
new_register = """    function registerTiltAnswer(wasCorrect) {
      if (tiltLocked || !gameActive || gamePhase !== "playing") {
        return;
      }

      tiltLocked = true;
      resetStartedAt = null;
      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }
"""
if old_register not in text:
    raise SystemExit("register block not found")
text = text.replace(old_register, new_register, 1)

old_answer_end = """      showAnswerFeedback(wasCorrect);
      showNextWord();
    }
"""
new_answer_end = """      showAnswerFeedback(wasCorrect);

      if (motionEnabled && !testMode) {
        gamePhase = "resetting";
        wordCard.textContent = wasCorrect
          ? "Correct!\\nReturn phone to centre"
          : "Skipped\\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold the phone facing forward until the next word appears.";
      } else {
        showNextWord();
      }
    }
"""
if old_answer_end not in text:
    raise SystemExit("answer block not found")
text = text.replace(old_answer_end, new_answer_end, 1)

path.write_text(text, encoding="utf-8")
Path(".github/workflows/apply-motion-reset-fix.yml").unlink()
Path(".github/scripts/apply_motion_reset.py").unlink()
