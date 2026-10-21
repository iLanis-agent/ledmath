# LED Math

Series resistor arithmetic. A 2 V LED on a 9 V rail leaves 7 V for the resistor, so 20 mA calls for 350 Ω and the resistor turns 140 mW into heat.

## What it computes

- **The resistor truth** - the series resistor for one LED (rail and LED voltage 0.01 to 100 V, current 0.01 to 1000 mA) and the heat the resistor turns it into.
- **The chain truth** - several LEDs in series drop their voltages together, and the resistor takes what is left. When the drop eats the rail, it says the arithmetic has no positive answer.
- **The strings truth** - parallel strings each draw their own current, and the rail supplies the sum.

## Boundary

Arithmetic only. The voltages, currents and counts are the owner's own entries, every LED and resistor treated as ideal. It has not seen any circuit and does not know the bin, the temperature, the wiring or the supply, and it gives no verdict that a resistor, an LED or a rail is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a V and hundredths of a mA, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/ledmath/
Repo: https://github.com/iLanis-agent/ledmath
