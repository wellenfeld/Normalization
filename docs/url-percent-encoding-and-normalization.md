# Percent-encoding, UTF-8, and Unicode normalization: why NFC vs NFD changes URLs

This document explains a common failure mode in systems that ingest, generate, lint, or parse URLs:

- A user-visible string can be **canonically equivalent** under Unicode (e.g., NFC vs NFD), yet
- Its **UTF-8 bytes differ**, therefore
- Its **percent-encoded form differs**, therefore
- URL comparisons, routing, caching, signatures, and “same-link” checks may disagree.

## Definitions (strict)

- A **URL/URI percent-escape** (aka percent-encoding) is a textual encoding of a single **byte** as `%` followed by two hex digits.
  - WHATWG URL calls these “percent-encoded bytes” and defines a percent-encoded byte as `U+0025 (%)` followed by two ASCII hex digits. (WHATWG URL Standard, §1.3 “Percent-encoded bytes”: https://url.spec.whatwg.org/)
- In URIs, percent-encoding is defined over **octets**, not code points. RFC 3986 uses `pct-encoded` for these escapes. (RFC 3986, §2.1; overall spec: https://www.rfc-editor.org/rfc/rfc3986.html)
- When representing **non-ASCII characters** inside URI components that allow it, RFC 3986 describes a two-step process:
  - Encode the characters as **UTF-8** bytes, then percent-encode each byte.
  - RFC 3986 explicitly states: “Non-ASCII characters must first be encoded according to UTF-8 … and then each octet … must be percent-encoded …” (RFC 3986, in the discussion of `reg-name` / host; see https://www.rfc-editor.org/rfc/rfc3986.html)

## Unicode normalization recap (why two strings can be “the same” but byte-different)

UAX #15 defines canonical equivalence and explains that normalization works by:

- Full decomposition (canonical or compatibility)
- Canonical ordering (by Canonical_Combining_Class)
- Optional canonical composition (for NFC/NFKC)

Source: UAX #15 §1.1 and §1.3 (https://unicode.org/reports/tr15/).

### Canonical equivalence is not byte equivalence

Two canonically equivalent strings can have different sequences of code points:

- Precomposed: `U+00EA` ("ê")
- Decomposed: `U+0065 U+0302` ("e" + COMBINING CIRCUMFLEX ACCENT)

They are canonically equivalent, but have different UTF-8 encodings.

## Core pitfall: percent-encoding exposes UTF-8 byte differences

Percent-encoding is performed on bytes. Therefore:

- NFC text containing precomposed characters yields one set of UTF-8 bytes.
- NFD text containing base+combining marks yields a different set of UTF-8 bytes.
- Percent-encoding those bytes yields different `%xx` sequences.

This means:

- **Two canonically equivalent paths can serialize to different URLs.**
- Some stacks normalize (or not) at different layers, creating mismatches.

## Failure modes (source-agnostic)

- **Cache key divergence**
  - Cache keyed on URL string / path bytes may treat NFC and NFD as different resources.
- **Router mismatch**
  - If a server routes on raw path bytes but an upstream normalized, the route can fail.
- **Signature / HMAC mismatch**
  - If one side signs an NFC URL string and the other verifies against an NFD form (or vice versa), verification fails.
- **Linter/parser false positives**
  - Tools that treat a URL as a Unicode string may “see” a stable label, while a URL library percent-encodes bytes and changes the textual representation.

## Canonical example vector (NFC vs NFD)

Consider a URL path segment containing a circumflexed vowel and an acute vowel.

### Code point sequences

- NFC form:
  - `... U+00EA ... U+00E1 ...`
- NFD form:
  - `... U+0065 U+0302 ... U+0061 U+0301 ...`

### UTF-8 bytes (for the differing characters)

- `U+00EA` → UTF-8 bytes `C3 AA`
- `U+0065 U+0302` → UTF-8 bytes `65 CC 82`
- `U+00E1` → UTF-8 bytes `C3 A1`
- `U+0061 U+0301` → UTF-8 bytes `61 CC 81`

### Percent-encoding

If these bytes are percent-encoded in a URL component, you get:

- NFC:
  - `ê` → `%C3%AA`
  - `á` → `%C3%A1`
- NFD:
  - `e◌̂` → `%65%CC%82`
  - `a◌́` → `%61%CC%81`

These strings are **not identical**, even though the underlying Unicode text can be canonically equivalent.

## Requirements for robust systems

- **Choose a normalization policy for URL generation and storage**
  - If you normalize, specify **which form** (`NFC` is common for interchange; see UAX #15).
  - Document whether you normalize **before** UTF-8 + percent-encoding.
- **Never assume percent-encoding implies normalization**
  - Percent-encoding is a byte escape mechanism; it does not impose NFC/NFD.
- **Test with explicit NFC/NFD vectors**
  - Always include vectors that differ only by canonical decomposition.

## References

- Unicode Standard Annex #15: Unicode Normalization Forms
  - https://unicode.org/reports/tr15/
- WHATWG URL Standard (Percent-encoded bytes)
  - https://url.spec.whatwg.org/
- RFC 3986: Uniform Resource Identifier (URI): Generic Syntax
  - https://www.rfc-editor.org/rfc/rfc3986.html
