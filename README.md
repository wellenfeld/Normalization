# Unicode Normalization Research & Security

This repository provides **comprehensive research** on Unicode normalization and its security implications. It includes documented attacks, practical examples, and test vectors—all strictly reference-backed by Unicode standards and real-world CVEs.

## 🎯 Key Findings

- **8 major attack classes** documented with real CVEs
- **Timeline from 2013-2024** showing evolution of Unicode exploits  
- **Working exploit code** for Spotify hijacking, SQL injection, Android bypass
- **Step-by-step exploitation methods** with exact payloads
- **Complete implementations** with full vulnerable applications and exploit scripts
- **50 working payloads** for immediate testing and validation
- **Detection and prevention strategies** for each attack type
- **Universal vulnerability scanner** for comprehensive security testing

## 📚 Documentation

### Core Research
- **[Exploitation Landscape](docs/unicode-exploitation-landscape.md)** — Taxonomy of Unicode/normalization exploitation classes
- **[Exploit Timeline & Methods](docs/exploit-timeline-and-methods.md)** — Complete timeline with detailed exploitation techniques (2013-2024)
- **[Widely Known Attacks](docs/widely-known-normalization-attacks.md)** — Documented CVEs (Spotify hijacking, Android bypass, Trojan Source)

### Practical Examples  
- **[Working Exploits](docs/working-exploit-examples.md)** — Real working exploits with exact payloads
- **[Step-by-Step Exploits](docs/step-by-step-exploit-examples.md)** — Practical attack walkthroughs
- **[Comprehensive Examples](docs/comprehensive-exploit-examples.md)** — Complete exploit implementations with full code
- **[Practical Examples](docs/practical-normalization-examples.md)** — Copy-pastable examples with code points

### Advanced Topics
- **[Advanced Attacks](docs/advanced-normalization-attacks.md)** — Sophisticated exploitation patterns
- **[Real-World Cases](docs/real-world-normalization-exploits.md)** — Detection/mitigation strategies
- **[Identifier Normalization and Confusables](docs/identifier-normalization-and-confusables.md)** — identifiers, default-ignorables, confusables

### Technical Deep Dives
- **[Normalization Deep Divergence and Stability](docs/normalization-deep-divergence-and-stability.md)** — composition exclusions, stream-safe format, stability guarantees
- **[Linter/Parser Normalization Issues](docs/linter-parser-normalization-issues.md)** — linter/parser failure modes with Unicode
- **[URL Percent Encoding and Normalization](docs/url-percent-encoding-and-normalization.md)** — how NFC vs NFD changes percent-encoded URLs
- **[Source Code Bidi and Invisible Characters](docs/source-code-bidi-and-invisible-characters.md)** — bidi controls and source code attacks

## 🧪 Test Vectors

### Core Exploit Vectors
- **[Working Exploits](data/vectors/real_world_exploit_scenarios.json)** — Real-world exploit patterns
- **[Advanced Vectors](data/vectors/advanced_attack_vectors.json)** — Sophisticated attack vectors
- **[Comprehensive Payloads](data/vectors/comprehensive_working_payloads.json)** — 50 working Unicode exploit payloads

### Technical Vectors
- **[URL Encoding](data/vectors/url_percent_encoding_nfc_nfd.json)** — NFC vs NFD percent-encoding divergence
- **[Apostrophe Lookalikes](data/vectors/url_apostrophe_lookalikes.json)** — Distinct apostrophe-like characters
- **[Bidi Controls](data/vectors/source_code_bidi_controls.json)** — Source code control characters
- **[Identifier Confusables](data/vectors/identifier_confusable_homoglyph.json)** — Mixed-script lookalikes
- **[Composition Exclusions](data/vectors/normalization_composition_exclusions.json)** — UAX #15 exclusion types
- **[Stream-Safe Format](data/vectors/normalization_stream_safe.json)** — Stream-safe guarantees

## 🚀 Quick Start

### Test Your Applications
```bash
# Test with comprehensive payloads
python3 -c "
import json
with open('data/vectors/comprehensive_working_payloads.json') as f:
    payloads = json.load(f)
    for payload in payloads['payloads'][:5]:
        print(f'Test: {payload[\"payload\"]}')
        print(f'Target: {payload[\"category\"]}')
        print(f'Normalized: {payload[\"normalized\"]}')
        print('---')
"
```

### Scan for Vulnerabilities
```python
# Use the universal vulnerability scanner
from docs.comprehensive_exploit_examples import UnicodeVulnerabilityScanner

scanner = UnicodeVulnerabilityScanner()
scanner.scan_input("admin%uff07 UNION SELECT * FROM users --", "sql_injection")
```

## Scope (authoritative)

- **Unicode Normalization Forms (UAX #15 / ISO 10646 alignment)**
  - `NFD`, `NFC`, `NFKD`, `NFKC`
  - Canonical ordering (combining mark reordering)
  - Canonical composition (recomposition)
  - Hangul algorithmic decomposition/composition
  - Stream-Safe Text Format (UAX #15 §13)
- **Normalization-adjacent processes** (not “Normalization Forms”, but commonly confused with them)
  - **IDNA processing** and its normalization requirements (UTS #46 uses NFC as a step)
  - Case folding (not normalization, but often combined with NFKC for “identifier normalization”)
  - Security-related normalization guidance (e.g., confusables are not solved by NFC/NFKC)

Out of scope unless explicitly added later:

- Locale-specific collation or “string comparison” beyond normalization.
- Grapheme cluster segmentation, rendering, shaping (normalization can affect them, but does not define them).

## Documentation

- `docs/unicode-exploitation-landscape.md` — taxonomy of Unicode/normalization exploitation classes
- `docs/widely-known-normalization-attacks.md` — documented CVEs and public exploits (Spotify, Android, Trojan Source)
- `docs/step-by-step-exploit-examples.md` — practical, easy-to-understand exploit walkthroughs
- `docs/advanced-normalization-attacks.md` — sophisticated Exploitationsmuster and complex exploitation
- `docs/real-world-normalization-exploits.md` — concrete exploit cases and detection/mitigation strategies
- `docs/practical-normalization-examples.md` — concrete, copy-pastable examples with code points and UTF-8 bytes
- `docs/identifier-normalization-and-confusables.md` — identifiers, default-ignorables, confusables
- `docs/normalization-deep-divergence-and-stability.md` — composition exclusions, stream-safe format, stability guarantees
- `docs/linter-parser-normalization-issues.md` — linter/parser failure modes with Unicode
- `docs/url-percent-encoding-and-normalization.md` — how NFC vs NFD changes percent-encoded URLs
- `docs/source-code-bidi-and-invisible-characters.md` — bidi controls and source code attacks
- `docs/exploit-timeline-and-methods.md` — complete timeline with detailed exploitation techniques
- `docs/working-exploit-examples.md` — real working exploits with exact payloads
- `docs/comprehensive-exploit-examples.md` — complete exploit implementations with full code

## Test vectors

- `data/vectors/url_percent_encoding_nfc_nfd.json` — NFC vs NFD percent-encoding divergence
- `data/vectors/url_apostrophe_lookalikes.json` — distinct apostrophe-like characters
- `data/vectors/source_code_bidi_controls.json` — bidi control characters in source code
- `data/vectors/identifier_confusable_homoglyph.json` — mixed-script lookalike identifiers
- `data/vectors/normalization_composition_exclusions.json` — composition exclusion types
- `data/vectors/normalization_stream_safe.json` — stream-safe format guarantees
- `data/vectors/real_world_exploit_scenarios.json` — real-world exploit patterns
- `data/vectors/advanced_attack_vectors.json` — sophisticated attack vectors
- `data/vectors/comprehensive_working_payloads.json` — 50 working Unicode exploit payloads

## Terminology (precise)

- **Code point**: A Unicode scalar value (e.g., `U+00E9`).
- **Code unit**: Encoding unit (UTF-8 byte, UTF-16 16-bit unit, etc.). Normalization is defined over code points, not code units.
- **Canonical equivalence**: Two strings represent the “same abstract character” under canonical decomposition and canonical ordering. (UAX #15 §1.1)
- **Compatibility equivalence**: Weaker relationship where characters may differ stylistically or semantically in some contexts, but can be treated the same in others. (UAX #15 §1.1)
- **Starter**: A code point with canonical combining class (ccc) = 0.
- **Non-starter**: A code point with ccc != 0.

## The Unicode Normalization Algorithm (UAX #15 summary)

UAX #15 describes normalization as:

1. **Full decomposition**
   - For `NFD`/`NFC`: full **canonical** decomposition.
   - For `NFKD`/`NFKC`: full **compatibility** decomposition.
   - Uses `Decomposition_Mapping` values (from the Unicode Character Database), plus special algorithmic rules for Hangul syllables.
2. **Canonical Ordering Algorithm**
   - Reorders combining marks based on `Canonical_Combining_Class` (ccc).
   - Only affects non-starters (ccc != 0).
3. **Canonical Composition Algorithm** (only for composed forms)
   - For `NFC` and `NFKC`: recomposes where allowed and not blocked/excluded.
   - Must account for composition exclusions and blocking rules.

Source: UAX #15 §1.3.

## What each normalization form guarantees

- **NFD**
  - Full canonical decomposition + canonical ordering.
  - No canonical composition performed.
- **NFC**
  - Equivalent to NFD, then canonical composition.
  - Common “recommended interchange” normalization for general text.
- **NFKD**
  - Full compatibility decomposition + canonical ordering.
  - May remove formatting distinctions (e.g., compatibility characters).
- **NFKC**
  - Equivalent to NFKD, then canonical composition.
  - Often used as part of “identifier normalization” pipelines, but can change meaning in some domains (not safe as a universal default).

## Behavioral notes on specific input categories

This section is intentionally concrete. When you add claims here, you must back them with:

- A citation to the Unicode Standard / UAX / UTS / UCD, **and**
- A runnable cross-language test (in `tests/` or `data/vectors/`).

### ASCII

- All normalization forms leave pure ASCII (`U+0000..U+007F`) unchanged.
  - UAX #15 explicitly notes this property (UAX #15 §1.3).

### Latin-1

- Text exclusively in Latin-1 (`U+0000..U+00FF`) is unchanged by `NFC`.
  - UAX #15 §1.3.

### Precomposed vs decomposed characters

Example (canonical equivalence):

- `"e" + U+0301 COMBINING ACUTE ACCENT` (decomposed) and `U+00E9 "é"` (precomposed) are canonically equivalent.
- `NFD("é")` produces the decomposed sequence.
- `NFC("e\u0301")` produces the precomposed form when composition is available and not blocked.

### Combining mark reordering (canonical ordering)

Normalization reorders *only* by canonical combining class (ccc), not by visual preference.

Key implications:

- Canonical ordering can move a combining mark earlier in the string relative to other combining marks.
- It does **not** cross a starter boundary.
- Extremely long sequences of non-starters are legal; stream-safe format addresses buffering hazards.

### Hangul syllables (algorithmic)

Hangul syllables decompose/compose algorithmically (not via explicit tables) per the Unicode standard.

Practical implications:

- `NFD` of Hangul syllables produces Jamo sequences.
- `NFC` can recombine valid Jamo sequences back into syllables.

### Composition exclusions

Some characters are excluded from composition.

- UAX #15 describes a `Composition_Exclusion` derived property and notes that **no composition exclusion character occurs in any normalized form**. (UAX #15 §5)

### Stream-Safe Text Format (UAX #15)

This is not a normalization form, but a format helpful for streaming/buffered implementations.

- Stream-safe text has no sequences of non-starters longer than 30 when normalized to NFKD.
- The stream-safe process may insert `U+034F COMBINING GRAPHEME JOINER (CGJ)` to break up sequences.

Source: UAX #15 §13.

## IDNA and normalization (UTS #46)

Internationalized Domain Names involve a separate processing pipeline.

- UTS #46 performs mapping, then **normalizes the domain name string to NFC** as an explicit step. (UTS #46 §4 “Normalize. Normalize the domain_name string to Unicode Normalization Form C.”)
- Validity criteria for labels include being in NFC. (UTS #46 §4.1)

Important: IDNA processing is not “just NFC”. It includes mapping tables, disallowed/ignored code points, punycode conversion, and additional validation.

## Cross-language reality (what you must verify)

Different ecosystems expose Unicode normalization differently, and may include extra behavior around:

- Which Unicode version their normalization data corresponds to.
- Whether they also offer “NFKC_Casefold”-style pipelines.
- Whether they normalize by default in identifiers, file systems, or networking stacks.

This repo treats cross-language behavior as *testable artifacts*, not assumptions.

## Repository structure

- `docs/`
  - Long-form notes and deep dives (must be reference-backed).
- `data/`
  - Canonical test vectors and externally sourced conformance data.
- `data/vectors/`
  - Curated examples with expected outputs and explanations.
- `implementations/`
  - Per-language experiments and wrappers.
- `tests/`
  - Cross-language test harnesses (added over time).

## Conformance and test data

UAX #15 requires that normalizers be able to produce results matching the Unicode conformance test data.

- UAX #15 conformance clause references `NormalizationTest.txt` (UAX #15 §4, clause UAX15-C3).
- UTS #46 provides `IdnaTestV2.txt` for conformance testing.

This repo will track:

- Where test data originates.
- Exact Unicode version.
- Checksums (when we start importing files).

## Strict rules for contributions

All contributions must follow `AGENTS.md`.

## References (primary)

- Unicode Standard Annex #15: Unicode Normalization Forms
  - https://unicode.org/reports/tr15/
- Unicode Technical Standard #46: Unicode IDNA Compatibility Processing
  - https://unicode.org/reports/tr46/
