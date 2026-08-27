from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

s = s.replace(
'''        Choose a category and turn length. The game will calibrate your Correct
        gesture before every round, so Skip will always be the opposite tilt.''',
'''        Choose a category and turn length. Tilt the phone down for Correct and
        tilt it up for Skip. No gesture recording is required.'''
)

s = s.replace(
'''        Saved motion = Correct • Opposite motion = Skip''',
'''        Tilt DOWN = Correct • Tilt UP = Skip'''
)

old_vars = '''    let filteredBeta = null;
    let filteredGamma = null;
    let neutralAxes = null;
    let calibrationBaseAxes = null;
    let correctGesture = null;
    let skipGesture = null;
    let lastScreenAngle = null;
    let answerArmed = false;
    let calibrationEndsAt = 0;
    let answerCooldownEndsAt = 0;
    let centreReferenceAxes = null;
    let centreStableSince = null;
    let gestureCandidate = null;
    let gestureCandidateSince = null;
    let gesturePeak = null;
'''
new_vars = '''    let filteredPitch = null;
    let neutralPitch = null;
    let centreReferencePitch = null;
    let centreStableSince = null;
    let gestureDirection = 0;
    let gestureStartedAt = null;
    let answerArmed = false;
    let answerCooldownEndsAt = 0;
    let lastScreenAngle = null;
    let resumeCurrentWordAfterCentre = false;
'''
if old_vars not in s:
    raise SystemExit('motion variable block not found')
s = s.replace(old_vars, new_vars, 1)

old_constants = '''    const gestureThreshold = 24;
    const neutralRadius = 9;
    const centreStabilityRadius = 3.5;
    const tiltSmoothing = 0.32;
    const answerCooldownMs = 650;
    const centreHoldMs = 700;
    const gestureHoldMs = 240;
    const gestureDirectionConsistency = 0.9;
    const minimumGestureMatch = 0.5;
    const maximumSameDirectionScore = 0.25;
'''
new_constants = '''    const tiltThreshold = 24;
    const returnToCentreZone = 11;
    const centreStabilityRadius = 2.5;
    const tiltSmoothing = 0.28;
    const answerCooldownMs = 550;
    const centreHoldMs = 500;
    const gestureHoldMs = 180;
    const standardCorrectDirection = 1;
'''
if old_constants not in s:
    raise SystemExit('motion constants block not found')
s = s.replace(old_constants, new_constants, 1)

old_start = '''      if (testMode) {
        beginRound();
      } else {
        beginDirectionCalibration();
      }
'''
new_start = '''      if (testMode) {
        beginRound();
      } else {
        beginCountdown();
      }
'''
if old_start not in s:
    raise SystemExit('start mode block not found')
s = s.replace(old_start, new_start, 1)

start = s.index('    function resetSensorFilters() {')
end = s.index('    function answerWord(wasCorrect) {')
replacement = r'''    function resetMotionState() {
      filteredPitch = null;
      centreReferencePitch = null;
      centreStableSince = null;
      gestureDirection = 0;
      gestureStartedAt = null;
      answerArmed = false;
    }

    function beginCountdown() {
      gamePhase = "countdown";
      let count = 3;

      gameInstructions.textContent =
        "Tilt DOWN = Correct • Tilt UP = Skip";

      function nextCount() {
        if (!gameActive || gamePhase !== "countdown") {
          return;
        }

        if (!isPhoneLandscape()) {
          countdownTimeout = setTimeout(nextCount, 250);
          return;
        }

        if (count > 0) {
          wordCard.textContent = String(count);
          count -= 1;
          countdownTimeout = setTimeout(nextCount, 750);
          return;
        }

        wordCard.textContent = "GO!";
        countdownTimeout = setTimeout(beginRound, 450);
      }

      nextCount();
    }

    function beginRound() {
      if (!gameActive) {
        return;
      }

      clearInterval(timer);
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
    }

    function getScreenAngle() {
      if (
        screen.orientation &&
        typeof screen.orientation.angle === "number"
      ) {
        return screen.orientation.angle;
      }

      if (typeof window.orientation === "number") {
        return window.orientation;
      }

      return window.innerWidth > window.innerHeight ? 90 : 0;
    }

    function getViewportDimensions() {
      const visualWidth = window.visualViewport
        ? window.visualViewport.width
        : 0;
      const visualHeight = window.visualViewport
        ? window.visualViewport.height
        : 0;
      const documentWidth = document.documentElement.clientWidth || 0;
      const documentHeight = document.documentElement.clientHeight || 0;

      return {
        width: Math.max(window.innerWidth || 0, visualWidth, documentWidth),
        height: Math.max(window.innerHeight || 0, visualHeight, documentHeight)
      };
    }

    function isPhoneLandscape() {
      const { width, height } = getViewportDimensions();

      if (width > height * 1.05) {
        return true;
      }

      if (height > width * 1.05) {
        return false;
      }

      const angle = ((getScreenAngle() % 360) + 360) % 360;
      return angle === 90 || angle === 270;
    }

    function getScreenRelativePitch(event) {
      const beta = Number.isFinite(event.beta) ? event.beta : null;
      const gamma = Number.isFinite(event.gamma) ? event.gamma : null;

      if (beta === null || gamma === null) {
        return null;
      }

      const angle = ((getScreenAngle() % 360) + 360) % 360;

      if (angle === 90) {
        return gamma;
      }

      if (angle === 270) {
        return -gamma;
      }

      if (angle === 180) {
        return -beta;
      }

      return beta;
    }

    function smoothPitch(nextPitch) {
      if (filteredPitch === null) {
        filteredPitch = nextPitch;
      } else {
        filteredPitch +=
          (nextPitch - filteredPitch) * tiltSmoothing;
      }

      return filteredPitch;
    }

    function resetGestureHold() {
      gestureDirection = 0;
      gestureStartedAt = null;
    }

    function beginAutomaticCentering(resumeCurrentWord) {
      gamePhase = "centering";
      answerArmed = false;
      resumeCurrentWordAfterCentre = resumeCurrentWord;
      filteredPitch = null;
      neutralPitch = null;
      centreReferencePitch = null;
      centreStableSince = null;
      resetGestureHold();

      wordCard.textContent = "Hold phone facing forward";
      gameInstructions.textContent =
        "Keep it still briefly. No gesture recording is happening.";
    }

    function updateAutomaticCentering(pitch) {
      const now = Date.now();

      if (centreReferencePitch === null) {
        centreReferencePitch = pitch;
        centreStableSince = now;
        return;
      }

      if (
        Math.abs(pitch - centreReferencePitch) > centreStabilityRadius
      ) {
        centreReferencePitch = pitch;
        centreStableSince = now;
        return;
      }

      if (
        centreStableSince !== null &&
        now - centreStableSince >= centreHoldMs
      ) {
        neutralPitch = pitch;
        filteredPitch = pitch;
        centreReferencePitch = null;
        centreStableSince = null;
        answerArmed = true;
        gamePhase = "playing";
        gameInstructions.textContent =
          "Tilt DOWN = Correct • Tilt UP = Skip";

        if (resumeCurrentWordAfterCentre && currentWord) {
          wordCard.textContent = currentWord;
        } else {
          showNextWord();
        }
      }
    }

    function updateResetToCentre(pitch) {
      const now = Date.now();

      if (Date.now() < answerCooldownEndsAt) {
        centreStableSince = null;
        return;
      }

      if (
        neutralPitch === null ||
        Math.abs(pitch - neutralPitch) > returnToCentreZone
      ) {
        centreStableSince = null;
        return;
      }

      if (centreStableSince === null) {
        centreStableSince = now;
        return;
      }

      if (now - centreStableSince >= centreHoldMs) {
        neutralPitch = pitch;
        filteredPitch = pitch;
        centreStableSince = null;
        resetGestureHold();
        answerArmed = true;
        gamePhase = "playing";
        gameInstructions.textContent =
          "Tilt DOWN = Correct • Tilt UP = Skip";
        showNextWord();
      }
    }

    function handlePlayingTilt(pitch) {
      if (!answerArmed || neutralPitch === null) {
        return;
      }

      const difference = pitch - neutralPitch;

      if (Math.abs(difference) <= returnToCentreZone) {
        resetGestureHold();
        neutralPitch += difference * 0.025;
        return;
      }

      let direction = 0;

      if (difference >= tiltThreshold) {
        direction = 1;
      } else if (difference <= -tiltThreshold) {
        direction = -1;
      }

      if (direction === 0) {
        resetGestureHold();
        return;
      }

      const now = Date.now();

      if (direction !== gestureDirection) {
        gestureDirection = direction;
        gestureStartedAt = now;
        return;
      }

      if (
        gestureStartedAt !== null &&
        now - gestureStartedAt >= gestureHoldMs
      ) {
        const wasCorrect = direction === standardCorrectDirection;
        resetGestureHold();
        registerTiltAnswer(wasCorrect);
      }
    }

    function handleOrientation(event) {
      if (!motionEnabled || !gameActive || !isPhoneLandscape()) {
        return;
      }

      const screenAngle = getScreenAngle();

      if (screenAngle !== lastScreenAngle) {
        lastScreenAngle = screenAngle;
        beginAutomaticCentering(Boolean(currentWord));
        return;
      }

      const rawPitch = getScreenRelativePitch(event);

      if (rawPitch === null) {
        return;
      }

      const pitch = smoothPitch(rawPitch);

      if (gamePhase === "centering") {
        updateAutomaticCentering(pitch);
        return;
      }

      if (gamePhase === "resetting") {
        updateResetToCentre(pitch);
        return;
      }

      if (gamePhase === "playing") {
        handlePlayingTilt(pitch);
      }
    }

    function registerTiltAnswer(wasCorrect) {
      if (!answerArmed || !gameActive || gamePhase !== "playing") {
        return;
      }

      answerArmed = false;
      centreStableSince = null;
      resetGestureHold();
      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }

'''
s = s[:start] + replacement + s[end:]

old_orientation = '''          if (
            gamePhase !== "idle" &&
            gamePhase !== "finished" &&
            gamePhase !== "setup"
          ) {
            beginDirectionCalibration();
          }
'''
new_orientation = '''          if (
            gamePhase !== "idle" &&
            gamePhase !== "finished" &&
            gamePhase !== "setup" &&
            gamePhase !== "countdown"
          ) {
            lastScreenAngle = getScreenAngle();
            beginAutomaticCentering(Boolean(currentWord));
          }
'''
if old_orientation not in s:
    raise SystemExit('orientation handler block not found')
s = s.replace(old_orientation, new_orientation, 1)

path.write_text(s, encoding='utf-8')
