from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_css = '''    .game-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      font-size: 22px;
      font-weight: bold;
    }

    .word-card {
'''
new_css = '''    .game-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      font-size: 22px;
      font-weight: bold;
    }

    .exit-game-button {
      flex-shrink: 0;
      padding: 8px 14px;
      border: none;
      border-radius: 10px;
      background: #dc2626;
      color: white;
      font-size: 15px;
      font-weight: bold;
    }

    .exit-game-button:active {
      transform: scale(0.96);
    }

    .word-card {
'''
if old_css not in s:
    raise SystemExit('game-info CSS block not found')
s = s.replace(old_css, new_css, 1)

old_html = '''      <div class="game-info">
        <span>Time: <span id="timeRemaining">60</span></span>
        <span>Score: <span id="score">0</span></span>
      </div>
'''
new_html = '''      <div class="game-info">
        <span>Time: <span id="timeRemaining">60</span></span>
        <span>Score: <span id="score">0</span></span>
        <button
          class="exit-game-button"
          type="button"
          aria-label="End the current round"
          onclick="exitGame()"
        >
          Exit
        </button>
      </div>
'''
if old_html not in s:
    raise SystemExit('game-info HTML block not found')
s = s.replace(old_html, new_html, 1)

marker = '''    function finishGame() {
'''
exit_function = '''    function exitGame() {
      if (!gameActive) {
        return;
      }

      const shouldExit = window.confirm(
        "End this round and view your results?"
      );

      if (!shouldExit) {
        return;
      }

      finishGame();
    }

'''
if marker not in s:
    raise SystemExit('finishGame function marker not found')
s = s.replace(marker, exit_function + marker, 1)

path.write_text(s, encoding='utf-8')
