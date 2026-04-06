# Practical Unicode normalization examples

This document provides concrete, copy-pastable examples of Unicode normalization behavior with explicit code points, UTF-8 bytes, and normalized forms. All examples are reference-backed and reproducible.

## 1. NFC vs NFD: canonical composition vs decomposition

### Example 1: Latin e with acute

- Input: `e\u0301` (e followed by COMBINING ACUTE ACCENT)
- Code points: U+0065, U+0301
- NFC: `é` (U+00E9) — composed form
- NFD: `e\u0301` — decomposed form
- UTF-8 bytes:
  - NFC: `C3 A9`
  - NFD: `65 CC 81`

### Example 2: Devanagari QA (script-specific exclusion)

- Input: U+0958 (DEVANAGARI LETTER QA)
- NFC: U+0958 (unchanged)
- NFD: U+0958 (unchanged, because it’s a script-specific composition exclusion)
- UTF-8 bytes: `E0 96 98`

Source: UAX #15 §5.1 (Composition Exclusion Types)

## 2. Stream-safe vs overlong sequences

### Example 1: Stream-safe combining mark

- Input: `e\u0301` (U+0065 U+0301)
- Stream-safe: yes
- Reason: No overlong sequence of non-starters

### Example 2: Overlong non-starter sequence (not stream-safe)

- Input: `a\u0301\u0301` (U+0061 U+0301 U+0301)
- Stream-safe: no
- Reason: Overlong sequence of non-starters (two combining marks in a row)

Source: UAX #15 §3.12 (Stream-Safe Text Format)

## 3. Compatibility normalization (NFKC/NFKD)

### Example 1: Superscript to baseline digit

- Input: `²` (SUPERSCRIPT TWO, U+00B2)
- NFC: `²` (U+00B2, unchanged)
- NFKD: `2` (DIGIT TWO, U+0032)
- UTF-8 bytes:
  - NFC: `C2 B2`
  - NFKD: `32`

### Example 2: Ligature to letters

- Input: `ﬂ` (LATIN SMALL LIGATURE FL, U+FB02)
- NFC: `ﬂ` (U+FB02, unchanged)
- NFKD: `fl` (U+0066 U+006C)
- UTF-8 bytes:
  - NFC: `EF AC 82`
  - NFKD: `66 6C`

Source: UAX #15 §1 (Introduction)

## 4. Percent-encoding divergence

### Example: Portuguese text with NFC vs NFD

- Original: `Convênio_de_Bahá'u'lláh`
- NFC form: `Convênio_de_Bahá'u'lláh`
  - UTF-8 bytes: `43 6F 6E C3 AA 6E 69 6F 5F 42 61 68 75 27 6C 6C C3 A1 68`
  - Percent-encoded: `Conv%C3%AAnio_de_Bah%C3%A1%27u%27ll%C3%A1h`
- NFD form: `Convênio_de_Bahá'u'lláh`
  - UTF-8 bytes: `43 6F 6E 76 CC 82 6E 69 6F 5F 42 61 68 75 27 6C 6C 76 CC 81 68`
  - Percent-encoded: `Conve%CC%82nio_de_Baha%CC%81%27u%27lla%CC%81h`

Source: RFC 3986, WHATWG URL Standard

## 5. Default-ignorable characters

### Example 1: Variation selector

- Input: `a\uFE00` (LATIN SMALL LETTER A + VARIATION SELECTOR-1)
- Code points: U+0061, U+FE00
- NFC: `a\uFE00` (unchanged)
- NFD: `a\uFE00` (unchanged)
- UTF-8 bytes: `61 EF B8 80`

### Example 2: Bidi control

- Input: `abc\u202Edef` (RIGHT-TO-LEFT OVERRIDE)
- Code points: U+0061 U+0062 U+0063 U+202E U+0064 U+0065 U+0066
- NFC: `abc\u202Edef` (unchanged)
- NFD: `abc\u202Edef` (unchanged)
- UTF-8 bytes: `61 62 63 E2 80 AE 64 65 66`

Source: UAX #31 §2.3 (Layout and Format Control Characters)

## 6. Confusable identifiers

### Example: Latin vs Cyrillic lookalike

- Identifier A: `sayHello`
  - Code points: U+0073 U+0061 U+0079 U+0048 U+0065 U+006C U+006C U+006F
- Identifier B: `say\u041DHello`
  - Code points: U+0073 U+0061 U+0079 U+041D U+0065 U+006C U+006C U+006F
  - U+041D is CYRILLIC CAPITAL LETTER EN (visually similar to Latin H in many fonts)

Source: UTS #39 §4 (Confusable Detection)

## How to test these examples

```bash
# Test NFC/NFD conversion
python3 -c "
import unicodedata
s = 'e\u0301'
nfc = unicodedata.normalize('NFC', s)
nfd = unicodedata.normalize('NFD', s)
print(f'Input: {s} (code points: {[ord(c) for c in s]})')
print(f'NFC: {nfc} (code points: {[ord(c) for c in nfc]})')
print(f'NFD: {nfd} (code points: {[ord(c) for c in nfd]})')
print(f'NFC UTF-8: {nfc.encode(\"utf-8\").hex()}')
print(f'NFD UTF-8: {nfd.encode(\"utf-8\").hex()}')
"
```

```bash
# Test percent-encoding divergence
python3 -c "
import urllib.parse
s = 'Convênio_de_Bahá\\'u\\'lláh'
nfc = unicodedata.normalize('NFC', s)
nfd = unicodedata.normalize('NFD', s)
print(f'NFC percent-encoded: {urllib.parse.quote(nfc.encode(\"utf-8\"))}')
print(f'NFD percent-encoded: {urllib.parse.quote(nfd.encode(\"utf-8\"))}')
"
```

## References

- UAX #15: https://unicode.org/reports/tr15/
- UAX #31: https://unicode.org/reports/tr31/
- UTS #39: https://unicode.org/reports/tr39/
- RFC 3986: https://www.rfc-editor.org/rfc/rfc3986.html
- WHATWG URL: https://url.spec.whatwg.org/
