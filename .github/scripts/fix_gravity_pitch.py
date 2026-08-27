from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_angle = '''    function getScreenAngle() {
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
'''
new_angle = '''    function getScreenAngle() {
      if (typeof window.orientation === "number") {
        return window.orientation;
      }

      if (
        screen.orientation &&
        typeof screen.orientation.angle === "number"
      ) {
        return screen.orientation.angle;
      }

      return window.innerWidth > window.innerHeight ? 90 : 0;
    }
'''
if old_angle not in s:
    raise SystemExit('getScreenAngle block not found')
s = s.replace(old_angle, new_angle, 1)

old_pitch = '''    function getScreenRelativePitch(event) {
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
'''
new_pitch = '''    function getScreenRelativePitch(event) {
      if (!Number.isFinite(event.beta) || !Number.isFinite(event.gamma)) {
        return null;
      }

      const beta = event.beta * Math.PI / 180;
      const gamma = event.gamma * Math.PI / 180;

      // Convert the Euler angles into a gravity vector in device coordinates.
      // This stays continuous when gamma approaches its ±90° limit.
      const gravityX = Math.sin(gamma) * Math.cos(beta);
      const gravityY = -Math.sin(beta);
      const gravityZ = -Math.cos(beta) * Math.cos(gamma);

      const angle = ((getScreenAngle() % 360) + 360) % 360;
      let gravityTowardScreenTop;

      if (angle === 90) {
        gravityTowardScreenTop = -gravityX;
      } else if (angle === 270) {
        gravityTowardScreenTop = gravityX;
      } else if (angle === 180) {
        gravityTowardScreenTop = -gravityY;
      } else {
        gravityTowardScreenTop = gravityY;
      }

      const uprightComponent = -gravityTowardScreenTop;

      return Math.atan2(gravityZ, uprightComponent) * 180 / Math.PI;
    }
'''
if old_pitch not in s:
    raise SystemExit('getScreenRelativePitch block not found')
s = s.replace(old_pitch, new_pitch, 1)

s = s.replace(
    'Tilt DOWN = Correct • Tilt UP = Skip',
    'Tilt screen toward FLOOR = Correct • toward CEILING = Skip'
)

path.write_text(s, encoding='utf-8')
