# Source code exploitation: bidi controls and invisible characters

This document summarizes publicly discussed source-code exploitation classes involving Unicode control characters. It is **not** about Unicode normalization forms per se, but it is tightly related to how Unicode text is processed and displayed.

## Core problem: visual order vs logical order

Some Unicode control characters can affect how text is **displayed** (visual ordering) without changing the underlying sequence of code points.

- Compilers and interpreters generally process the **logical order** of code points.
- Humans reviewing code see a **visual order** rendered by editors/IDEs.

When those differ, reviewers can be deceived.

## Trojan Source class (public discussion)

Trojan Source describes attacks where Unicode control characters reorder tokens so code appears to do one thing while executing another.

- The overview states that this attack pattern is tracked as CVE-2021-42574.

Source: https://trojansource.codes/

## Relevant Unicode standard guidance

### UTS #55: Unicode Source Code Handling

UTS #55 defines terminology and guidance for:

- Source code display and bidirectional ordering.
- Blank and invisible characters.
- Confusables and diagnostics.

Source: UTS #55 (https://www.unicode.org/reports/tr55/).

### UAX #31 note: tooling-level diagnostics

UAX #31 observes that for programming language identifiers, spoofing issues are more comprehensively addressed by higher-level diagnostics rather than solely by syntactic restrictions, referencing UTS #55.

Source: UAX #31 §2.3 (https://unicode.org/reports/tr31/).

## Minimal vector guidance

This repo stores minimal source-code vectors under `data/vectors/`.

- Bidi controls are typically General_Category `Cf` and are often Default_Ignorable.
- Vectors must include explicit `U+XXXX` sequences.

See: `data/vectors/source_code_bidi_controls.json`.

## References

- UTS #55: https://www.unicode.org/reports/tr55/
- UAX #31: https://unicode.org/reports/tr31/
- Trojan Source overview: https://trojansource.codes/
