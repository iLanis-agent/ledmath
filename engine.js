// LED Math engine: the series resistor for one LED, for a chain, and the rail draw of parallel strings. Exact integers (hundredths of a V, hundredths of a mA), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pi(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _V = "each voltage must be from 0.01 to 100 V with at most two decimal places";
var _I = "the current must be from 0.01 to 1000 mA with at most two decimal places";
var _N = "the LED count must be a whole number from 1 to 100";
var _S = "the string count must be a whole number from 1 to 100";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  if (v < 0) return "-" + _dec(-v, places);
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _v(v) { return _dec(v, 2) + " V"; }
function _ma(i) { return _dec(i, 2) + " mA"; }
function _ohm(rem100, ima100) { return _dec(_hu(rem100 * 100000, ima100), 2) + " Ω"; } // hundredths of an ohm
function _mw(rem100, ima100) { return _dec(_hu(rem100 * ima100, 100), 2) + " mW"; } // hundredths of a mW
function _in(vs, vf, ima) {
  return { vs: _p(vs, _V, 3, 2, 1, 10000), vf: _p(vf, _V, 3, 2, 1, 10000), i: _p(ima, _I, 4, 2, 1, 100000) };
}

function resistorTruth(vs, vf, ima) {
  var p = _in(vs, vf, ima), rem = p.vs - p.vf;
  if (rem <= 0) return "A " + _v(p.vf) + " LED on a " + _v(p.vs) + " rail leaves " + _v(rem) + " for the resistor, and the arithmetic has no positive answer.";
  return "A " + _v(p.vf) + " LED on a " + _v(p.vs) + " rail leaves " + _v(rem) + " for the resistor. At " + _ma(p.i) + " that calls for " + _ohm(rem, p.i) + ", and the resistor turns " + _mw(rem, p.i) + " into heat.";
}
function chainTruth(vs, vf, ima, n) {
  var p = _in(vs, vf, ima), c = _pi(n, _N, 1, 100);
  var drop = p.vf * c, rem = p.vs - drop;
  var lead = c === 1 ? "1 LED at " : c + " LEDs at ";
  if (rem <= 0) return lead + _v(p.vf) + (c === 1 ? " drops " : " drop ") + _v(drop) + ", which leaves " + _v(rem) + " on the " + _v(p.vs) + " rail - the arithmetic has no positive resistor answer.";
  return lead + _v(p.vf) + (c === 1 ? " drops " : " drop ") + _v(drop) + ". On the " + _v(p.vs) + " rail that leaves " + _v(rem) + ", so " + _ma(p.i) + " calls for " + _ohm(rem, p.i) + " and the resistor turns " + _mw(rem, p.i) + " into heat.";
}
function stringsTruth(vs, ima, s) {
  var p = _in(vs, vs, ima), c = _pi(s, _S, 1, 100);
  var tot = p.i * c; // hundredths of a mA
  var w = _hu(p.vs * tot, 100000); // hundredths of a W
  var lead = c === 1 ? "1 string at " : c + " strings at ";
  return lead + _ma(p.i) + (c === 1 ? " draws " : " draw ") + _ma(tot) + " from the " + _v(p.vs) + " rail, " + _dec(w, 2) + " W in all.";
}
