from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

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
    let centreHoldStartedAt = null;
'''
new_vars = '''    let filteredBeta = null;
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
if old_vars not in s:
    raise SystemExit('motion variables block not found')
s = s.replace(old_vars, new_vars, 1)

old_constants = '''    const gestureThreshold = 16;
    const neutralRadius = 11;
    const tiltSmoothing = 0.4;
    const answerCooldownMs = 550;
    const centreHoldMs = 500;
    const minimumGestureMatch = 0.35;
    const maximumSameDirectionScore = 0.35;
'''
new_constants = '''    const gestureThreshold = 24;
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
if old_constants not in s:
    raise SystemExit('motion constants block not found')
s = s.replace(old_constants, new_constants, 1)

start = s.index('    function beginDirectionCalibration() {')
end = s.index('    function beginCountdown() {')
new_begin_calibration = '''    function beginDirectionCalibration() {
      gamePhase = "calibration-centre";
      resetSensorFilters();
      neutralAxes = null;
      calibrationBaseAxes = null;
      correctGesture = null;
      skipGesture = null;
      answerArmed = false;
      centreReferenceAxes = null;
      centreStableSince = null;
      resetGestureCandidate();
      calibrationEndsAt = Date.now() + 400;
      lastScreenAngle = getScreenAngle();

      wordCard.textContent =
        "Hold the phone sideways\\nand facing forward";
      gameInstructions.textContent =
        "Keep it completely still until the Correct instruction appears.";
    }

'''
s = s[:start] + new_begin_calibration + s[end:]

start = s.index('    function beginRound() {')
end = s.index('    function getScreenAngle() {')
new_begin_round = '''    function beginRound() {
      if (!gameActive) {
        return;
      }

      resetSensorFilters();
      neutralAxes = null;
      centreReferenceAxes = null;
      centreStableSince = null;
      resetGestureCandidate();
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
          "Keep it still. The first word appears after the centre is stable.";
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

'''
s = s[:start] + new_begin_round + s[end:]

start = s.index('    function isNearCentre(axes, baseAxes) {')
end = s.index('    function answerWord(wasCorrect) {')
new_motion = r'''    function isNearCentre(axes, baseAxes, radius = neutralRadius) {
      return vectorMagnitude(getDisplacement(axes, baseAxes)) <= radius;
    }

    function resetGestureCandidate() {
      gestureCandidate = null;
      gestureCandidateSince = null;
      gesturePeak = null;
    }

    function updateStableCentre(axes, onReady) {
      const now = Date.now();

      if (centreReferenceAxes === null) {
        centreReferenceAxes = { ...axes };
        centreStableSince = now;
        return;
      }

      const movement = vectorMagnitude(
        getDisplacement(axes, centreReferenceAxes)
      );

      if (movement > centreStabilityRadius) {
        centreReferenceAxes = { ...axes };
        centreStableSince = now;
        return;
      }

      if (
        centreStableSince !== null &&
        now - centreStableSince >= centreHoldMs
      ) {
        const stableAxes = { ...axes };
        centreReferenceAxes = null;
        centreStableSince = null;
        onReady(stableAxes);
      }
    }

    function holdAtRecordedCentre(axes, baseAxes, onReady) {
      const now = Date.now();

      if (!isNearCentre(axes, baseAxes)) {
        centreStableSince = null;
        return;
      }

      if (centreStableSince === null) {
        centreStableSince = now;
        return;
      }

      if (now - centreStableSince >= centreHoldMs) {
        centreStableSince = null;
        onReady({ ...axes });
      }
    }

    function trackDeliberateGesture(displacement) {
      const magnitude = vectorMagnitude(displacement);

      if (magnitude < gestureThreshold) {
        resetGestureCandidate();
        return null;
      }

      const direction = normalizeVector(displacement);
      const now = Date.now();

      if (direction === null) {
        resetGestureCandidate();
        return null;
      }

      if (
        gestureCandidate === null ||
        vectorDot(direction, gestureCandidate) < gestureDirectionConsistency
      ) {
        gestureCandidate = direction;
        gestureCandidateSince = now;
        gesturePeak = { ...displacement };
        return null;
      }

      if (
        gesturePeak === null ||
        magnitude > vectorMagnitude(gesturePeak)
      ) {
        gesturePeak = { ...displacement };
      }

      if (now - gestureCandidateSince < gestureHoldMs) {
        return null;
      }

      const result = normalizeVector(gesturePeak);
      resetGestureCandidate();
      return result;
    }

    function handleCalibration(axes) {
      if (gamePhase === "calibration-centre") {
        if (Date.now() < calibrationEndsAt) {
          return;
        }

        updateStableCentre(axes, (stableAxes) => {
          calibrationBaseAxes = stableAxes;
          gamePhase = "calibration-correct";
          resetGestureCandidate();
          wordCard.textContent =
            "Do your CORRECT motion now";
          gameInstructions.textContent =
            "Make one clear tilt and hold it briefly.";
        });
        return;
      }

      if (gamePhase === "calibration-correct") {
        const displacement = getDisplacement(axes, calibrationBaseAxes);
        const recordedGesture = trackDeliberateGesture(displacement);

        if (recordedGesture === null) {
          return;
        }

        correctGesture = recordedGesture;
        gamePhase = "return-after-correct";
        centreStableSince = null;
        playCorrectSound();
        showAnswerFeedback(true);
        wordCard.textContent =
          "Correct saved!\\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold it facing forward and still.";
        return;
      }

      if (gamePhase === "return-after-correct") {
        holdAtRecordedCentre(axes, calibrationBaseAxes, (stableAxes) => {
          calibrationBaseAxes = stableAxes;
          gamePhase = "calibration-skip";
          resetGestureCandidate();
          wordCard.textContent =
            "Do your SKIP motion now";
          gameInstructions.textContent =
            "Make one clear tilt in a different direction and hold it briefly.";
        });
        return;
      }

      if (gamePhase === "calibration-skip") {
        const displacement = getDisplacement(axes, calibrationBaseAxes);
        const candidateSkip = trackDeliberateGesture(displacement);

        if (candidateSkip === null) {
          return;
        }

        const sameDirectionScore = vectorDot(correctGesture, candidateSkip);

        if (sameDirectionScore > maximumSameDirectionScore) {
          gamePhase = "retry-skip-centre";
          centreStableSince = null;
          wordCard.textContent =
            "That looked too similar\\nReturn to centre";
          gameInstructions.textContent =
            "Then demonstrate a clearly different Skip motion.";
          return;
        }

        skipGesture = candidateSkip;
        gamePhase = "return-after-skip";
        centreStableSince = null;
        playSkipSound();
        showAnswerFeedback(false);
        wordCard.textContent =
          "Skip saved!\\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold it facing forward and still to begin.";
        return;
      }

      if (gamePhase === "retry-skip-centre") {
        holdAtRecordedCentre(axes, calibrationBaseAxes, (stableAxes) => {
          calibrationBaseAxes = stableAxes;
          gamePhase = "calibration-skip";
          resetGestureCandidate();
          wordCard.textContent =
            "Do your SKIP motion now";
          gameInstructions.textContent =
            "Use a clearly different direction from Correct.";
        });
        return;
      }

      if (gamePhase === "return-after-skip") {
        holdAtRecordedCentre(axes, calibrationBaseAxes, () => {
          beginCountdown();
        });
      }
    }

    function classifyGesture(direction) {
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

      if (
        gamePhase.startsWith("calibration-") ||
        gamePhase.startsWith("return-after-") ||
        gamePhase === "retry-skip-centre"
      ) {
        handleCalibration(axes);
        return;
      }

      if (gamePhase === "round-centre") {
        updateStableCentre(axes, (stableAxes) => {
          neutralAxes = stableAxes;
          answerArmed = true;
          gamePhase = "playing";
          resetGestureCandidate();
          gameInstructions.textContent =
            "Use your saved Correct and Skip motions.";
          showNextWord();
        });
        return;
      }

      if (gamePhase === "resetting") {
        if (Date.now() < answerCooldownEndsAt) {
          centreReferenceAxes = null;
          centreStableSince = null;
          return;
        }

        updateStableCentre(axes, (stableAxes) => {
          neutralAxes = stableAxes;
          filteredBeta = stableAxes.beta;
          filteredGamma = stableAxes.gamma;
          answerArmed = true;
          gamePhase = "playing";
          resetGestureCandidate();
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
      const magnitude = vectorMagnitude(displacement);

      if (magnitude <= neutralRadius) {
        resetGestureCandidate();
        return;
      }

      const deliberateDirection = trackDeliberateGesture(displacement);

      if (deliberateDirection === null) {
        return;
      }

      const classification = classifyGesture(deliberateDirection);

      if (classification !== null) {
        registerTiltAnswer(classification);
      }
    }

    function registerTiltAnswer(wasCorrect) {
      if (!answerArmed || !gameActive || gamePhase !== "playing") {
        return;
      }

      answerArmed = false;
      centreReferenceAxes = null;
      centreStableSince = null;
      resetGestureCandidate();
      answerCooldownEndsAt = Date.now() + answerCooldownMs;
      answerWord(wasCorrect);

      if ("vibrate" in navigator) {
        navigator.vibrate(wasCorrect ? 120 : [70, 60, 70]);
      }
    }

'''
s = s[:start] + new_motion + s[end:]

path.write_text(s, encoding='utf-8')
