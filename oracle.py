# LED Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

V = "each voltage must be from 0.01 to 100 V with at most two decimal places"
I = "the current must be from 0.01 to 1000 mA with at most two decimal places"
N = "the LED count must be a whole number from 1 to 100"
S = "the string count must be a whole number from 1 to 100"

def p(t, err, intdigits, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or len(parts[0]) > intdigits or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def pi(t, err, lo, hi):
    t = t.strip()
    if not t.isdigit() or len(t) > 3:
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v):
    if v < 0:
        return "-" + dec(-v)
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def vv(x): return dec(x) + " V"
def ma(x): return dec(x) + " mA"
def ohm(rem100, ima100): return dec(int(hu(Fraction(rem100) * 100000, ima100))) + " Ω"
def mw(rem100, ima100): return dec(int(hu(Fraction(rem100) * ima100, 100))) + " mW"

def inn(vs, vf, ima):
    return p(vs, V, 3, 1, 10000), p(vf, V, 3, 1, 10000), p(ima, I, 4, 1, 100000)

def resistorTruth(vs, vf, ima):
    v, f, i = inn(vs, vf, ima); rem = v - f
    if rem <= 0:
        return "A " + vv(f) + " LED on a " + vv(v) + " rail leaves " + vv(rem) + " for the resistor, and the arithmetic has no positive answer."
    return "A " + vv(f) + " LED on a " + vv(v) + " rail leaves " + vv(rem) + " for the resistor. At " + ma(i) + " that calls for " + ohm(rem, i) + ", and the resistor turns " + mw(rem, i) + " into heat."

def chainTruth(vs, vf, ima, n):
    v, f, i = inn(vs, vf, ima); c = pi(n, N, 1, 100)
    drop = f * c; rem = v - drop
    lead = "1 LED at " if c == 1 else str(c) + " LEDs at "
    verb = " drops " if c == 1 else " drop "
    if rem <= 0:
        return lead + vv(f) + verb + vv(drop) + ", which leaves " + vv(rem) + " on the " + vv(v) + " rail - the arithmetic has no positive resistor answer."
    return lead + vv(f) + verb + vv(drop) + ". On the " + vv(v) + " rail that leaves " + vv(rem) + ", so " + ma(i) + " calls for " + ohm(rem, i) + " and the resistor turns " + mw(rem, i) + " into heat."

def stringsTruth(vs, ima, s):
    v, _, i = inn(vs, vs, ima); c = pi(s, S, 1, 100)
    tot = i * c
    w = int(hu(Fraction(v) * tot, 100000))
    lead = "1 string at " if c == 1 else str(c) + " strings at "
    verb = " draws " if c == 1 else " draw "
    return lead + ma(i) + verb + ma(tot) + " from the " + vv(v) + " rail, " + dec(w) + " W in all."

FNS = {"resistorTruth": resistorTruth, "chainTruth": chainTruth, "stringsTruth": stringsTruth}

cases = []
for vs in ["0.01", "5", "9", "12", "100"]:
    for vf in ["0.01", "1.8", "2", "3.2", "100"]:
        for i in ["0.01", "20", "350", "1000"]:
            cases.append(("resistorTruth", [vs, vf, i]))
for n in ["1", "2", "3", "50", "100"]:
    cases.append(("chainTruth", ["9", "2", "20", n]))
    cases.append(("chainTruth", ["9", "4", "20", n]))
    cases.append(("chainTruth", ["100", "0.01", "1000", n]))
for s in ["1", "2", "4", "100"]:
    cases.append(("stringsTruth", ["9", "20", s]))
    cases.append(("stringsTruth", ["0.01", "0.01", s]))
    cases.append(("stringsTruth", ["100", "1000", s]))
errs = ["0", "101", "1.5", "x", ""]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for bad in errs:
    for name, args in [("resistorTruth", [bad, "2", "20"]), ("resistorTruth", ["9", bad, "20"]),
                       ("resistorTruth", ["9", "2", bad]), ("chainTruth", ["9", "2", "20", bad]),
                       ("chainTruth", [bad, "2", "20", "3"]), ("stringsTruth", ["9", bad, "4"]),
                       ("stringsTruth", [bad, "20", "4"]), ("stringsTruth", ["9", "20", bad])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
