from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = '''    let currentTilt = null;
    let filteredBeta = null;
    let filteredGamma = null;
    let neutralTilt = null;
    let tiltLocked = true;
    let calibrationEndsAt = 0;
    let calibrationBaseAxes = null;
    let activeTiltAxis = null;
    let lastScreenAngle = null;
    let correctDirection = 1;
    let answerCooldownEndsAt = 0;
    let resetStartedAt = null;
'''
new = '''    let filteredBeta = null;
    let filteredGamma = null;
    let neutralAxes = null;
    let calibrationBaseAxes = null;
    let correctGesture = null;
    let skipGesture = null;
    let lastScreenAngle = null;
    let answerArmed = false;
    let calibrationEndsAt = 0;
    let answerCooldownEndsAt = 0;
    let centreHoldStartedAt = null;
'''
if old not in s:
    raise SystemExit('motion variable block not found')
s = s.replace(old, new, 1)

old = '''    const correctTiltAmount = 22;
    const skipTiltAmount = 22;
    const calibrationTiltAmount = 14;
    const neutralZone = 13;
    const tiltSmoothing = 0.5;
    const answerCooldownMs = 650;
    const resetHoldMs = 500;
'''
new = '''    const gestureThreshold = 16;
    const neutralRadius = 11;
    const tiltSmoothing = 0.4;
    const answerCooldownMs = 550;
    const centreHoldMs = 500;
    const minimumGestureMatch = 0.35;
    const maximumSameDirectionScore = 0.35;
'''
if old not in s:
    raise SystemExit('motion constants block not found')
s = s.replace(old, new, 1)

start = s.index('    function beginDirectionCalibration() {')
end = s.index('    function registerTiltAnswer(wasCorrect) {')
replacement = r'''    function resetSensorFilters() {
      filteredBeta = null;
      filteredGamma = null;
    }

    function beginDirectionCalibration() {
      gamePhase = "calibration-centre";
      resetSensorFilters();
      neutralAxes = null;
      calibrationBaseAxes = null;
      correctGesture = null;
      skipGesture = null;
      answerArmed = false;
      centreHoldStartedAt = null;
      calibrationEndsAt = Date.now() + 1000;
      lastScreenAngle = getScreenAngle();

      wordCard.textContent =
        "Hold the phone sideways\nand facing forward";
      gameInstructions.textContent =
        "Keep it still while the game finds the centre position.";
    }

    function beginCountdown() {
      gamePhase = "countdown";
      let count = 3;

      gameInstructions.textContent =
        "Use the two motions you just demonstrated.";

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

      resetSensorFilters();
      neutralAxes = null;
      centreHoldStartedAt = null;
      lastScreenAngle = getScreenAngle();

      if (testMode) {
        gamePhase = "playing";
        answerArmed = true;
        gameInstructions.textContent = "Use the test buttons below";
        showNextWord();
      } else {
        gamePhase = "round-centre";
        answerArmed = false;
        wordCard.textContent = "Hold phone facing forward";
        gameInstructions.textContent =
          "The first word appears after the phone is centred.";
      }

      clearInterval(timer);

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

    function getSensorAxes(event) {
      const beta = Number.isFinite(event.beta) ? event.beta : null;
      const gamma = Number.isFinite(event.gamma) ? event.gamma : null;

      if (beta === null || gamma === null) {
        return null;
      }

      return { beta, gamma };
    }

    function smoothAxis(previousValue, nextValue) {
      if (previousValue === null) {
        return nextValue;
      }

      return previousValue +
        (nextValue - previousValue) * tiltSmoothing;
    }

    function smoothSensorAxes(axes) {
      filteredBeta = smoothAxis(filteredBeta, axes.beta);
      filteredGamma = smoothAxis(filteredGamma, axes.gamma);

      return {
        beta: filteredBeta,
        gamma: filteredGamma
      };
    }

    function angleDifference(value, baseValue) {
      let difference = value - baseValue;

      while (difference > 180) {
        difference -= 360;
      }

      while (difference < -180) {
        difference += 360;
      }

      return difference;
    }

    function getDisplacement(axes, baseAxes) {
      return {
        beta: angleDifference(axes.beta, baseAxes.beta),
        gamma: axes.gamma - baseAxes.gamma
      };
    }

    function vectorMagnitude(vector) {
      return Math.hypot(vector.beta, vector.gamma);
    }

    function normalizeVector(vector) {
      const magnitude = vectorMagnitude(vector);

      if (magnitude === 0) {
        return null;
      }

      return {
        beta: vector.beta / magnitude,
        gamma: vector.gamma / magnitude
      };
    }

    function vectorDot(first, second) {
      return first.beta * second.beta + first.gamma * second.gamma;
    }

    function isNearCentre(axes, baseAxes) {
      return vectorMagnitude(getDisplacement(axes, baseAxes)) <= neutralRadius;
    }

    function holdAtCentre(axes, baseAxes, onReady) {
      if (!isNearCentre(axes, baseAxes)) {
        centreHoldStartedAt = null;
        return;
      }

      if (centreHoldStartedAt === null) {
        centreHoldStartedAt = Date.now();
        return;
      }

      if (Date.now() - centreHoldStartedAt >= centreHoldMs) {
        centreHoldStartedAt = null;
        onReady();
      }
    }

    function handleCalibration(axes) {
      if (gamePhase === "calibration-centre") {
        if (Date.now() < calibrationEndsAt) {
          return;
        }

        calibrationBaseAxes = { ...axes };
        gamePhase = "calibration-correct";
        wordCard.textContent =
          "Do your CORRECT motion now";
        gameInstructions.textContent =
          "Tilt once in the direction you want to mean Correct.";
        return;
      }

      if (gamePhase === "calibration-correct") {
        const displacement = getDisplacement(axes, calibrationBaseAxes);

        if (vectorMagnitude(displacement) < gestureThreshold) {
          return;
        }

        correctGesture = normalizeVector(displacement);
        gamePhase = "return-after-correct";
        centreHoldStartedAt = null;
        playCorrectSound();
        showAnswerFeedback(true);
        wordCard.textContent =
          "Correct saved!\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold it facing forward until the next instruction.";
        return;
      }

      if (gamePhase === "return-after-correct") {
        holdAtCentre(axes, calibrationBaseAxes, () => {
          calibrationBaseAxes = { ...axes };
          gamePhase = "calibration-skip";
          wordCard.textContent =
            "Do your SKIP motion now";
          gameInstructions.textContent =
            "Tilt once in the direction you want to mean Skip.";
        });
        return;
      }

      if (gamePhase === "calibration-skip") {
        const displacement = getDisplacement(axes, calibrationBaseAxes);

        if (vectorMagnitude(displacement) < gestureThreshold) {
          return;
        }

        const candidateSkip = normalizeVector(displacement);
        const sameDirectionScore = vectorDot(correctGesture, candidateSkip);

        if (sameDirectionScore > maximumSameDirectionScore) {
          gamePhase = "retry-skip-centre";
          centreHoldStartedAt = null;
          wordCard.textContent =
            "That looked like Correct\nReturn to centre";
          gameInstructions.textContent =
            "Then demonstrate a clearly different Skip motion.";
          return;
        }

        skipGesture = candidateSkip;
        gamePhase = "return-after-skip";
        centreHoldStartedAt = null;
        playSkipSound();
        showAnswerFeedback(false);
        wordCard.textContent =
          "Skip saved!\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold it facing forward to start the countdown.";
        return;
      }

      if (gamePhase === "retry-skip-centre") {
        holdAtCentre(axes, calibrationBaseAxes, () => {
          calibrationBaseAxes = { ...axes };
          gamePhase = "calibration-skip";
          wordCard.textContent =
            "Do your SKIP motion now";
          gameInstructions.textContent =
            "Use a clearly different direction from Correct.";
        });
        return;
      }

      if (gamePhase === "return-after-skip") {
        holdAtCentre(axes, calibrationBaseAxes, () => {
          beginCountdown();
        });
      }
    }

    function classifyGesture(displacement) {
      const direction = normalizeVector(displacement);

      if (!direction || !correctGesture || !skipGesture) {
        return null;
      }

      const correctScore = vectorDot(direction, correctGesture);
      const skipScore = vectorDot(direction, skipGesture);
      const bestScore = Math.max(correctScore, skipScore);

      if (bestScore < minimumGestureMatch) {
        return null;
      }

      return correctScore > skipScore;
    }

    function handleOrientation(event) {
      if (!motionEnabled || !gameActive || !isPhoneLandscape()) {
        return;
      }

      const screenAngle = getScreenAngle();

      if (screenAngle !== lastScreenAngle) {
        beginDirectionCalibration();
        return;
      }

      const sensorAxes = getSensorAxes(event);

      if (sensorAxes === null) {
        return;
      }

      const axes = smoothSensorAxes(sensorAxes);

      if (gamePhase.startsWith("calibration-") ||
          gamePhase.startsWith("return-after-") ||
          gamePhase === "retry-skip-centre") {
        handleCalibration(axes);
        return;
      }

      if (gamePhase === "round-centre") {
        if (neutralAxes === null) {
          neutralAxes = { ...axes };
          centreHoldStartedAt = Date.now();
          return;
        }

        if (!isNearCentre(axes, neutralAxes)) {
          neutralAxes = { ...axes };
          centreHoldStartedAt = Date.now();
          return;
        }

        if (Date.now() - centreHoldStartedAt >= centreHoldMs) {
          neutralAxes = { ...axes };
          answerArmed = true;
          gamePhase = "playing";
          gameInstructions.textContent =
            "Use your saved Correct and Skip motions.";
          showNextWord();
        }

        return;
      }

      if (gamePhase === "resetting") {
        if (Date.now() < answerCooldownEndsAt) {
          centreHoldStartedAt = null;
          return;
        }

        holdAtCentre(axes, neutralAxes, () => {
          neutralAxes = { ...axes };
          filteredBeta = axes.beta;
          filteredGamma = axes.gamma;
          answerArmed = true;
          gamePhase = "playing";
          gameInstructions.textContent =
            "Ready — use your saved Correct and Skip motions.";
          showNextWord();
        });
        return;
      }

      if (gamePhase !== "playing" || !answerArmed) {
        return;
      }

      const displacement = getDisplacement(axes, neutralAxes);

      if (vectorMagnitude(displacement) < gestureThreshold) {
        return;
      }

      const classification = classifyGesture(displacement);

      if (classification !== null) {
        registerTiltAnswer(classification);
      }
    }

'''
s = s[:start] + replacement + s[end:]

old = '''    function registerTiltAnswer(wasCorrect) {
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
'''
new = '''    function registerTiltAnswer(wasCorrect) {
      if (!answerArmed || !gameActive || gamePhase !== "playing") {
        return;
      }

      answerArmed = false;
      centreHoldStartedAt = null;
      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }
'''
if old not in s:
    raise SystemExit('register function not found')
s = s.replace(old, new, 1)

old = '''          if (gamePhase === "playing") {
            recalibrateTilt();
          } else if (
            gamePhase === "calibrating" ||
            gamePhase === "returning"
          ) {
            beginDirectionCalibration();
          }
'''
new = '''          if (
            gamePhase !== "idle" &&
            gamePhase !== "finished" &&
            gamePhase !== "setup"
          ) {
            beginDirectionCalibration();
          }
'''
if old not in s:
    raise SystemExit('orientation-change block not found')
s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')
