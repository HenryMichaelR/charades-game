from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_reset = '''      if (now - centreStableSince >= centreHoldMs) {
        neutralPitch = pitch;
        filteredPitch = pitch;
        centreStableSince = null;
        resetGestureHold();
        answerArmed = true;
        gamePhase = "playing";
        gameInstructions.textContent =
          "Tilt screen toward FLOOR = Correct • toward CEILING = Skip";
        showNextWord();
      }
'''
new_reset = '''      if (now - centreStableSince >= centreHoldMs) {
        neutralPitch = pitch;
        filteredPitch = pitch;
        centreStableSince = null;
        resetGestureHold();
        answerArmed = true;
        gamePhase = "playing";
        gameInstructions.textContent =
          "Tilt screen toward FLOOR = Correct • toward CEILING = Skip";
      }
'''
if old_reset not in s:
    raise SystemExit('reset-to-centre block not found')
s = s.replace(old_reset, new_reset, 1)

old_answer = '''      if (motionEnabled && !testMode) {
        gamePhase = "resetting";
        wordCard.textContent = wasCorrect
          ? "Correct!\\nReturn phone to centre"
          : "Skipped\\nReturn phone to centre";
        gameInstructions.textContent =
          "Hold the phone facing forward until the next word appears.";
      } else {
        showNextWord();
      }
'''
new_answer = '''      if (motionEnabled && !testMode) {
        // Show the next word immediately, but keep motion locked until the
        // phone returns to centre. This preserves the reset protection without
        // interrupting the word flow with a separate message screen.
        showNextWord();

        if (!gameActive) {
          return;
        }

        gamePhase = "resetting";
        gameInstructions.textContent =
          "Tilt screen toward FLOOR = Correct • toward CEILING = Skip";
      } else {
        showNextWord();
      }
'''
if old_answer not in s:
    raise SystemExit('answer feedback block not found')
s = s.replace(old_answer, new_answer, 1)

if 'Return phone to centre' in s or 'Return phone to center' in s:
    raise SystemExit('between-word return message still remains')

path.write_text(s, encoding='utf-8')
