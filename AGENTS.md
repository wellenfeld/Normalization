# AGENTS

This file defines **strict, non-negotiable rules** for any automated agent or human contributor working in this repository.

This repository is about Unicode normalization across languages and ecosystems. The work must be **reference-backed, test-backed, and reproducible**.

## 1. Non-negotiable principles

- **No unreferenced claims**
  - If you state a behavioral rule about normalization (NFC/NFD/NFKC/NFKD, ordering, composition, exclusions, stability, stream-safe, IDNA), you must:
    - Cite an authoritative source (Unicode UAX/UTS/TR, Unicode Standard, UCD data file, RFC where applicable), and
    - Add a test vector and at least one executable check (when a harness exists).
- **No invented APIs / versions / behaviors**
  - Do not claim a language runtime does X unless you can point to:
    - its documentation, or
    - its source code, or
    - a reproducible test in this repo.
- **Normalization is not “text comparison”**
  - Do not conflate normalization with case folding, collation, grapheme segmentation, or security confusable handling.
  - If you discuss them, label them explicitly as separate layers.

## 2. Definitions must match Unicode terminology

When you use a term, use it precisely:

- “canonical equivalence” and “compatibility equivalence” per UAX #15.
- “starter” and “non-starter” based on canonical combining class.
- “normalize to NFC” means *exactly* the Unicode normalization form, not additional mapping.

If you introduce a new term (e.g., “identifier normalization pipeline”), define it in `docs/` with citations and a normative algorithm.

## 3. Behavioral claims require explicit input/output examples

Any time you describe behavior, include at least one explicit example using Unicode code point notation.

Rules:

- Include both a human-readable form and a `U+XXXX` sequence.
- Specify whether strings are sequences of code points (not code units).
- If the example depends on a Unicode version, state the version.

## 4. Data provenance rules (for external test files)

When importing external conformance files (e.g., `NormalizationTest.txt`, `IdnaTestV2.txt`):

- Record the source URL.
- Record the Unicode version.
- Record a checksum.
- Do not edit the content except for line ending normalization if required by tooling; if you must, document it.

## 5. Repository modification rules

- Prefer additive changes.
- Do not delete existing tests or vectors unless you prove they are wrong.
- If you change a definition in `README.md` or `docs/`, you must update associated tests/vectors.

## 6. Output format rules

- Use `NFC`, `NFD`, `NFKC`, `NFKD` exactly (case sensitive).
- Use `U+XXXX` notation for code points.
- When listing strings, also list their code points if ambiguity is possible.

## 7. Minimum quality bar for PRs / changes

A change is acceptable only if it includes:

- A precise description of the behavioral claim.
- A reference.
- A test or a vector.
- A clear statement of what is still unknown / unverified (if anything).

## 8. Safety and interoperability

Normalization can change strings and may affect:

- Identifiers
- Security boundaries
- Database keys
- Filenames
- Network names (IDNA)

Any proposal to normalize in a security-sensitive context must include:

- Threat model discussion (at least a paragraph)
- Counterexamples
- Justification for chosen form (NFC vs NFKC)
- Explicit note of what is *not* solved (e.g., confusables)
