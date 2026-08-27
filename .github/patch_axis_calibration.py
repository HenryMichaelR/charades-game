from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = [
(
'''    let currentTilt = null;
    let filteredTilt = null;
    let neutralTilt = null;
    let tiltLocked = true;
    let calibrationEndsAt = 0;
    let calibrationBaseTilt = null;
    let lastScreenAngle = null;
    let correctDirection = 1;
    let answerCooldownEndsAt = 0;
    let resetStartedAt = null;
''',
'''    let currentTilt = null;
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
),
(
'''    const calibrationTiltAmount = 16;
    const neutralZone = 13;
    const tiltSmoothing = 0.45;
''',
'''    const calibrationTiltAmount = 14;
    const neutralZone = 13;
    const tiltSmoothing = 0.5;
'''
),
(
'''      currentTilt = null;
      filteredTilt = null;
      neutralTilt = null;
      calibrationBaseTilt = null;
      resetStartedAt = null;
      tiltLocked = true;
''',
'''      currentTilt = null;
      filteredBeta = null;
      filteredGamma = null;
      neutralTilt = null;
      calibrationBaseAxes = null;
      activeTiltAxis = null;
      resetStartedAt = null;
      tiltLocked = true;
'''
),
(
'''      wordCard.textContent =
        "Hold the phone sideways\\nagainst your forehead";
      gameInstructions.textContent =
        "Keep it still. Then tilt the TOP EDGE DOWN when instructed.";
''',
'''      wordCard.textContent =
        "Hold the phone sideways\\nagainst your forehead";
      gameInstructions.textContent =
        "Keep it still. Then move it in the direction you want to mean CORRECT.";
'''
),
(
'''    function getLandscapeTilt(event) {
      if (event.gamma === null) {
        return null;
      }

      const angle = getScreenAngle();
      const normalizedAngle = ((angle % 360) + 360) % 360;

      return normalizedAngle === 270 ? -event.gamma : event.gamma;
    }

    function recalibrateTilt() {
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

    function handleCalibrationTilt(tiltValue) {
      if (Date.now() < calibrationEndsAt) {
        return;
      }

      if (calibrationBaseTilt === null) {
        calibrationBaseTilt = tiltValue;
        wordCard.textContent =
          "Tilt the TOP EDGE DOWN now\\nfor CORRECT";
        gameInstructions.textContent =
          "This one movement teaches the game your Correct direction.";
        return;
      }

      const difference = tiltValue - calibrationBaseTilt;

      if (Math.abs(difference) < calibrationTiltAmount) {
        return;
      }

      correctDirection = difference > 0 ? 1 : -1;
      neutralTilt = calibrationBaseTilt;
      gamePhase = "returning";

      playCorrectSound();
      showAnswerFeedback(true);
      wordCard.textContent =
        "Correct direction saved!\\nReturn the phone to centre";
      gameInstructions.textContent =
        "The opposite direction will be Skip.";
    }
''',
'''    function getSensorAxes(event) {
      const beta = Number.isFinite(event.beta) ? event.beta : null;
      const gamma = Number.isFinite(event.gamma) ? event.gamma : null;

      if (beta === null && gamma === null) {
        return null;
      }

      return { beta, gamma };
    }

    function smoothAxis(previousValue, nextValue) {
      if (nextValue === null) {
        return previousValue;
      }

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

    function getAxisDifference(value, baseValue, axis) {
      let difference = value - baseValue;

      if (axis === "beta") {
        while (difference > 180) {
          difference -= 360;
        }

        while (difference < -180) {
          difference += 360;
        }
      }

      return difference;
    }

    function recalibrateTilt() {
      currentTilt = null;
      filteredBeta = null;
      filteredGamma = null;
      neutralTilt = null;
      resetStartedAt = null;
      tiltLocked = true;
      calibrationEndsAt = Date.now() + 700;
      lastScreenAngle = getScreenAngle();
    }

    function handleCalibrationAxes(axes) {
      if (Date.now() < calibrationEndsAt) {
        return;
      }

      if (calibrationBaseAxes === null) {
        calibrationBaseAxes = {
          beta: axes.beta,
          gamma: axes.gamma
        };

        wordCard.textContent =
          "Move the phone now\\nin your CORRECT direction";
        gameInstructions.textContent =
          "The game will learn the sensor axis and direction automatically.";
        return;
      }

      const betaDifference =
        axes.beta === null || calibrationBaseAxes.beta === null
          ? 0
          : getAxisDifference(
              axes.beta,
              calibrationBaseAxes.beta,
              "beta"
            );

      const gammaDifference =
        axes.gamma === null || calibrationBaseAxes.gamma === null
          ? 0
          : getAxisDifference(
              axes.gamma,
              calibrationBaseAxes.gamma,
              "gamma"
            );

      const betaMovement = Math.abs(betaDifference);
      const gammaMovement = Math.abs(gammaDifference);
      const strongestMovement = Math.max(betaMovement, gammaMovement);

      if (strongestMovement < calibrationTiltAmount) {
        return;
      }

      activeTiltAxis =
        betaMovement >= gammaMovement ? "beta" : "gamma";

      const correctMovement =
        activeTiltAxis === "beta"
          ? betaDifference
          : gammaDifference;

      correctDirection = correctMovement >= 0 ? 1 : -1;
      neutralTilt = calibrationBaseAxes[activeTiltAxis];
      currentTilt = axes[activeTiltAxis];
      gamePhase = "returning";

      playCorrectSound();
      showAnswerFeedback(true);
      wordCard.textContent =
        "Correct gesture saved!\\nReturn the phone to centre";
      gameInstructions.textContent =
        "That movement is Correct. The opposite movement is Skip.";
    }
'''
),
(
'''      const tiltValue = getLandscapeTilt(event);

      if (tiltValue === null) {
        return;
      }

      currentTilt = smoothTilt(tiltValue);

      if (gamePhase === "calibrating") {
        handleCalibrationTilt(currentTilt);
        return;
      }
''',
'''      const sensorAxes = getSensorAxes(event);

      if (sensorAxes === null) {
        return;
      }

      const smoothedAxes = smoothSensorAxes(sensorAxes);

      if (gamePhase === "calibrating") {
        handleCalibrationAxes(smoothedAxes);
        return;
      }

      if (
        activeTiltAxis === null ||
        smoothedAxes[activeTiltAxis] === null
      ) {
        return;
      }

      currentTilt = smoothedAxes[activeTiltAxis];
'''
),
(
'''          Math.abs(currentTilt - neutralTilt) <= neutralZone
''',
'''          Math.abs(
            getAxisDifference(
              currentTilt,
              neutralTilt,
              activeTiltAxis
            )
          ) <= neutralZone
'''
),
(
'''        const resetDifference =
          (currentTilt - neutralTilt) * correctDirection;
''',
'''        const resetDifference =
          getAxisDifference(
            currentTilt,
            neutralTilt,
            activeTiltAxis
          ) * correctDirection;
'''
),
(
'''            filteredTilt = currentTilt;
''',
'''            if (activeTiltAxis === "beta") {
              filteredBeta = currentTilt;
            } else {
              filteredGamma = currentTilt;
            }
'''
),
(
'''      const difference =
        (currentTilt - neutralTilt) * correctDirection;
''',
'''      const difference =
        getAxisDifference(
          currentTilt,
          neutralTilt,
          activeTiltAxis
        ) * correctDirection;
'''
),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f'Patch block not found:\n{old[:120]}')
    text = text.replace(old, new, 1)

text = text.replace(
    'Top edge DOWN = Correct • Top edge UP = Skip',
    'Saved motion = Correct • Opposite motion = Skip'
)
text = text.replace(
    'Ready — top edge DOWN = Correct • top edge UP = Skip',
    'Ready — saved motion = Correct • opposite motion = Skip'
)

path.write_text(text, encoding='utf-8')
