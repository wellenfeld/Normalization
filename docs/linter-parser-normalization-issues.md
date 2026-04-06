# Linter/parser issues involving Unicode normalization

This document describes common failure modes in linters and parsers when Unicode normalization is not handled consistently or correctly. It is grounded in Unicode standards and practical failure patterns.

## 1. Inconsistent normalization pipelines

### 1.1 Ambiguous canonicalization order

Parsers may apply steps in different orders:

- Normalize? (which form?)
- UTF-8 encode?
- Percent-encode?
- Percent-decode?
- Normalize again?

Because percent-encoding is byte-based (WHATWG URL §1.3), NFC vs NFD changes UTF-8 bytes, which changes `%xx` sequences.

Sources:

- WHATWG URL: https://url.spec.whatwg.org/
- RFC 3986: https://www.rfc-editor.org/rfc/rfc3986.html
- UAX #15: https://unicode.org/reports/tr15/

### 1.2 Normalization not applied before comparison

Two identifiers that are canonically equivalent may compare unequal if normalization is omitted or applied inconsistently.

Source: UAX #31 §5 “Normalization and Case” (https://unicode.org/reports/tr31/).

## 2. Default-ignorable characters not filtered

### 2.1 Invisible characters in identifiers

UAX #31 §2.3 warns that Default_Ignorable_Code_Points (General_Category `Cf`, variation selectors, joiners, bidi controls) in identifiers can be invisible or stylistic, creating strings that look identical but differ.

Source: UAX #31 §2.3 (https://unicode.org/reports/tr31/).

### 2.2 Undetected bidi controls

Source code and identifiers containing bidi controls (e.g., U+202E RIGHT-TO-LEFT OVERRIDE) may pass linters that are not aware of UTS #55 guidance.

Source: UTS #55 (https://www.unicode.org/reports/tr55/).

## 3. Compatibility normalization misuse

### 3.1 Using NFKC/NFKD for identifiers

NFKC/NFKD can change visual appearance and meaning (e.g., superscripts to baseline digits, ligatures to components). Using compatibility forms for identifier comparison can lead to security issues.

Source: UAX #15 §1 “Introduction” (https://unicode.org/reports/tr15/).

## 4. Stream processing assumptions

### 4.1 Assuming stream-safe input

If a parser assumes all input is stream-safe (UAX #15 §3.12), it may produce incorrect normalization results when encountering overlong sequences of non-starters.

Source: UAX #15 §3.12 “Stream-Safe Text Format” (https://unicode.org/reports/tr15/).

## 5. Implementation divergence risks

### 5.1 Version dependence

New characters added after composition version may be excluded from composition. Implementations using older UCD data may produce different NFC results.

Source: UAX #15 §5.1 (https://unicode.org/reports/tr15/).

## 6. Minimal vectors

Vectors illustrating these issues are stored in `data/vectors/`:

- `normalization_composition_exclusions.json`
- `normalization_stream_safe.json`
- `url_percent_encoding_nfc_nfd.json`
- `url_apostrophe_lookalikes.json`

## References

- UAX #15: https://unicode.org/reports/tr15/
- UAX #31: https://unicode.org/reports/tr31/
- UTS #55: https://www.unicode.org/reports/tr55/
- WHATWG URL: https://url.spec.whatwg.org/
- RFC 3986: https://www.rfc-editor.org/rfc/rfc3986.html
