# Apostrophes and lookalike characters in URLs (Unicode vs bytes vs percent-encoding)

URLs often contain apostrophe-like characters. Multiple **distinct Unicode code points** can render similarly, but they are not necessarily canonically equivalent, and they typically encode to different UTF-8 bytes.

This matters when:

- A system compares URLs as raw strings.
- A system percent-encodes a URL component (encoding bytes, not code points).
- A system normalizes (or fails to normalize) text before URL serialization.

## Key principle: percent-encoding is for bytes

The WHATWG URL Standard defines percent-encoded bytes as `%` followed by two ASCII hex digits and provides explicit algorithms for percent-encoding and percent-decoding of byte sequences. (WHATWG URL Standard §1.3 “Percent-encoded bytes”: https://url.spec.whatwg.org/)

RFC 3986 defines percent-encoding (`pct-encoded`) over octets and notes that non-ASCII characters must first be encoded as UTF-8 bytes and then each octet percent-encoded when represented in a URI component that uses percent-encoding for non-ASCII. (RFC 3986: https://www.rfc-editor.org/rfc/rfc3986.html)

## Code points that commonly look like “apostrophe”

These are different characters:

- ASCII apostrophe: `U+0027` (')
- Right single quotation mark: `U+2019` (’)
- Modifier letter right half ring: `U+02BE` (ʾ)

They typically have different UTF-8 bytes, and thus different percent-encoded sequences.

Important: **Unicode Normalization Forms (UAX #15)** are defined in terms of canonical/compatibility decompositions and canonical ordering/composition. They do not claim to unify “lookalike punctuation” in general. (UAX #15: https://unicode.org/reports/tr15/)

## RFC 3986 note: literal apostrophe can be valid

Do not assume that a literal apostrophe inside a URI is malformed.

In RFC 3986, the apostrophe character `'` is included in the `sub-delims` production, and `pchar` includes `sub-delims`. Therefore, `'` may be allowed unescaped in URI path segments under the generic syntax. See the definitions in RFC 3986 (https://www.rfc-editor.org/rfc/rfc3986.html).

## Failure modes (source-agnostic)

- **Visual equivalence vs byte equivalence**
  - Two URLs may *look the same* in UI but differ in bytes and therefore be distinct as strings and as cache keys.
- **Inconsistent serialization**
  - One component serializes as a literal code point (e.g., `'`), another percent-encodes bytes (e.g., `%E2%80%99`).
  - Both can be legitimate; the risk is inconsistency in comparison and canonicalization.
- **Security review and auditing pitfalls**
  - Logs, alerts, and manual reviews can miss that multiple code points are being used.

## Recommended practice

- **Define a canonicalization strategy** for URL generation and storage.
  - If you normalize, specify the form (`NFC`/`NFKC`) and apply it consistently *before* UTF-8 encoding + percent-encoding.
- **Compare URLs on a well-defined representation**
  - Decide whether you compare on:
    - raw URL strings,
    - parsed components,
    - percent-decoded byte sequences (with UTF-8 decode),
    - plus optional Unicode normalization.
- **Add test vectors**
  - Include explicit code point and byte sequences for lookalike punctuation.

## References

- Unicode Standard Annex #15: Unicode Normalization Forms
  - https://unicode.org/reports/tr15/
- WHATWG URL Standard
  - https://url.spec.whatwg.org/
- RFC 3986: Uniform Resource Identifier (URI): Generic Syntax
  - https://www.rfc-editor.org/rfc/rfc3986.html
