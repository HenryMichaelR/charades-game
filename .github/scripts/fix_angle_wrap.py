from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = '''    function smoothPitch(nextPitch) {
      if (filteredPitch === null) {
        filteredPitch = nextPitch;
      } else {
        filteredPitch +=
          (nextPitch - filteredPitch) * tiltSmoothing;
      }

      return filteredPitch;
    }
'''
new = '''    function normalizeAngle(angle) {
      return ((angle + 180) % 360 + 360) % 360 - 180;
    }

    function angleDifference(currentAngle, referenceAngle) {
      return normalizeAngle(currentAngle - referenceAngle);
    }

    function smoothPitch(nextPitch) {
      if (filteredPitch === null) {
        filteredPitch = normalizeAngle(nextPitch);
      } else {
        const difference = angleDifference(nextPitch, filteredPitch);
        filteredPitch = normalizeAngle(
          filteredPitch + difference * tiltSmoothing
        );
      }

      return filteredPitch;
    }
'''
if old not in s:
    raise SystemExit('smoothPitch block not found')
s = s.replace(old, new, 1)

s = s.replace(
    'Math.abs(pitch - centreReferencePitch) > centreStabilityRadius',
    'Math.abs(angleDifference(pitch, centreReferencePitch)) > centreStabilityRadius'
)

s = s.replace(
    'Math.abs(pitch - neutralPitch) > returnToCentreZone',
    'Math.abs(angleDifference(pitch, neutralPitch)) > returnToCentreZone'
)

old = '''      const difference = pitch - neutralPitch;
'''
new = '''      const difference = angleDifference(pitch, neutralPitch);
'''
if old not in s:
    raise SystemExit('playing tilt difference not found')
s = s.replace(old, new, 1)

old = '''        neutralPitch += difference * 0.025;
'''
new = '''        neutralPitch = normalizeAngle(
          neutralPitch + difference * 0.025
        );
'''
if old not in s:
    raise SystemExit('neutral drift update not found')
s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')
