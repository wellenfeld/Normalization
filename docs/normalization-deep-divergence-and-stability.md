# Normalization deep divergence and stability

This document covers deeper aspects of Unicode normalization that can lead to divergence across implementations, versions, or processing pipelines. It is grounded in UAX #15 and related Unicode specifications.

## 1. Composition exclusion and stability (UAX #15)

### 1.1 Four types of composition exclusion

UAX #15 §5.1 defines four types of canonically decomposable characters that are excluded from composition in the Canonical Composition Algorithm:

- **Script-specific exclusions**: e.g., U+0958 (DEVANAGARI LETTER QA).
- **Post composition version exclusions**: e.g., U+2ADC (FORKING), U+1D15F (MUSICAL SYMBOL QUARTER NOTE).
- **Singleton exclusions**: e.g., U+2126 (OHM SIGN).
- **Non-starter decomposition exclusions**: e.g., U+0344 (COMBINING GREEK DIALYTIKA TONOS).

These exclusions are **explicitly listed** in the Unicode Character Database and cannot be computed from decomposition mappings alone.

Source: UAX #15 §5.1 (https://unicode.org/reports/tr15/).

### 1.2 Stability guarantees

Normalization stability is a principle: once a string is normalized, future versions of Unicode should not change its normalized form.

Post composition version exclusions exist specifically to maintain stability when new characters are encoded after the composition version.

Source: UAX #15 §5.1.

## 2. Stream-Safe Text Format (UAX #15)

### 2.1 Definition

UAX #15 §3.12 defines **Stream-Safe Text Format**: a text format that allows incremental processing of normalization without buffering arbitrary amounts of text.

- A string is stream-safe if it does not contain any “overlong sequences” of non-starters.
- Overlong sequences are sequences of non-starters that would violate the canonical ordering limits.

### 2.2 Practical implications

- Stream-safe format enables streaming normalization (e.g., in parsers, network protocols).
- If input is not stream-safe, normalization may require unbounded buffering.

Source: UAX #15 §3.12 “Stream-Safe Text Format”.

## 3. Normalization forms and compatibility

### 3.1 Canonical vs compatibility

- **Canonical forms (NFC, NFD)**: preserve canonical equivalence; they do not perform compatibility mappings.
- **Compatibility forms (NFKC, NFKD)**: apply compatibility mappings, which can change meaning (e.g., superscripts to baseline digits, ligatures to component characters).

Compatibility normalization can change text semantics and is not safe for identifier comparison in many contexts.

Source: UAX #15 §1 “Introduction”.

## 4. Interaction with other Unicode layers

### 4.1 Normalization vs case folding

- Normalization and case folding are distinct operations.
- UAX #31 defines `toNFKC_Casefold` for combined case-insensitive, compatibility-insensitive matching.

### 4.2 Normalization vs IDNA

- IDNA (UTS #46) applies specific normalization and mapping rules for domain names.
- IDNA processing is separate from generic Unicode normalization.

### 4.3 Normalization vs confusables

- Confusable detection (UTS #39) uses skeleton computation that includes NFD, but normalization alone does not solve confusability.

## 5. Implementation divergence risks

### 5.1 Version dependence

- New characters added after the composition version may be excluded from composition.
- Implementations using older UCD data may produce different NFC results.

### 5.2 Stream processing assumptions

- Assuming all input is stream-safe can lead to incorrect normalization results.
- Non-stream-safe input requires buffering.

### 5.3 Compatibility form misuse

- Using NFKC/NFKD for identifier comparison can lead to security issues (e.g., visually distinct identifiers becoming equivalent).

## 6. Minimal vectors

Vectors illustrating these deep aspects are stored in `data/vectors/`:

- `normalization_composition_exclusions.json`
- `normalization_stream_safe.json`

## References

- UAX #15: https://unicode.org/reports/tr15/
- UAX #31: https://unicode.org/reports/tr31/
- UTS #39: https://unicode.org/reports/tr39/
- UTS #46: https://unicode.org/reports/tr46/
