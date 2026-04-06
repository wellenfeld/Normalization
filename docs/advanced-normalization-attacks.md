# Advanced Unicode normalization attacks and complex exploitation patterns

This document covers sophisticated attack patterns involving Unicode normalization that go beyond basic confusables or bidi controls. These attacks exploit deeper Unicode properties, implementation differences, and multi-layer processing pipelines.

## 1. Normalization-aware code injection

### Attack pattern: NFKC expansion for payload smuggling

NFKC normalization can expand characters into longer sequences, enabling payload smuggling.

**Attack scenario:**
- Input: `｀｀｀` (FULLWIDTH GRAVE ACCENT, U+FF60)
- NFKC: ``````` (three backticks)
- Application filters backticks but not fullwidth equivalents
- After NFKC normalization, payload executes

**Complex variant:**
- Input: `｀｀｀${process.env.FLAG}｀｀｀`
- NFKC: ```````${process.env.FLAG}``````
- Bypasses template literal injection filters

**Detection:**
- Scan for characters with NFKC expansions
- Test normalization before and after filtering

**Mitigation:**
- Normalize before filtering
- Use allowlists instead of blocklists

Sources:
- UAX #15 §1 (Compatibility Decomposition)
- CWE-94: Improper Control of Generation of Code ('Code Injection')

## 2. Canonical ordering attacks

### Attack pattern: Non-starter reordering for logic bypass

Canonical ordering can reorder combining marks, changing logical behavior.

**Attack scenario:**
- Input: `e\u0301\u0327` (e + COMBINING ACUTE ACCENT + COMBINING CEDILLA)
- NFD: `e\u0327\u0301` (cedilla reordered before acute)
- Application processes combining marks in input order
- Logical behavior differs from visual representation

**Complex variant in source code:**
- Comment: `// e\u0301\u0327` (e with acute then cedilla)
- After NFD: `// e\u0327\u0301` (e with cedilla then acute)
- Different tokenization in some parsers

**Detection:**
- Compare input order vs canonical order
- Flag strings with non-starter sequences

**Mitigation:**
- Normalize before parsing
- Use canonical order throughout pipeline

Sources:
- UAX #15 §3.11 (Canonical Ordering)
- UAX #29: Unicode Text Segmentation

## 3. Stream-safe overflow attacks

### Attack pattern: Overlong sequences for DoS

Non-stream-safe text can require unbounded buffering during normalization.

**Attack scenario:**
- Input: `a` + 10,000 combining marks
- Normalization requires buffering entire sequence
- Memory exhaustion leads to DoS

**Complex variant:**
- Input: `a` + sequence of marks with increasing combining classes
- Requires complex sorting algorithm
- CPU exhaustion during normalization

**Detection:**
- Monitor memory usage during normalization
- Limit combining mark sequences

**Mitigation:**
- Reject non-stream-safe input
- Use streaming normalization algorithms

Sources:
- UAX #15 §3.12 (Stream-Safe Text Format)
- CWE-400: Uncontrolled Resource Consumption

## 4. Multi-layer encoding attacks

### Attack pattern: Normalization + encoding bypass

Combining normalization with multiple encoding layers.

**Attack scenario:**
1. Input: `｀｀｀` (fullwidth backticks)
2. NFKC: ``````` (backticks)
3. UTF-8 encode: `60 60 60`
4. Percent-encode: `%60%60%60`
5. Application decodes but doesn't normalize
6. Bypasses backtick filters

**Complex variant:**
1. Input: `｀｀｀${process.env.FLAG}｀｀｀`
2. NFKC: ```````${process.env.FLAG}``````
3. Base64 encode
4. Percent-encode base64
5. Multiple decode layers bypass filters

**Detection:**
- Normalize at each decoding step
- Track encoding depth

**Mitigation:**
- Normalize after each decode
- Limit encoding depth

Sources:
- UAX #15, RFC 3986, OWASP Encoding Cheat Sheet

## 5. Identifier collision in cryptographic contexts

### Attack pattern: Normalization collisions in signatures

Different normalization forms can produce different cryptographic signatures.

**Attack scenario:**
- Document A: `café` (NFC)
- Document B: `cafe\u0301` (NFD)
- Same visual content
- Different cryptographic signatures
- Attacker claims B is signed version of A

**Complex variant:**
- Use NFKC to change characters while preserving meaning
- `²` → `2` changes signature but not semantics in some contexts

**Detection:**
- Normalize before signing
- Verify normalization form in signature

**Mitigation:**
- Always normalize before cryptographic operations
- Include normalization form in signature metadata

Sources:
- UAX #15, CWE-347: Improper Verification of Cryptographic Signature

## 6. Normalization timing attacks

### Attack pattern: Side-channel via normalization differences

Different normalization forms take different time to process.

**Attack scenario:**
- Input A: `é` (NFC, fast to normalize)
- Input B: `e\u0301` (NFD, slower to normalize)
- Measure timing differences
- Infer original normalization form

**Complex variant:**
- Use characters with complex decomposition mappings
- Measure CPU cache usage patterns
- Infer character properties

**Detection:**
- Use constant-time normalization
- Add random delays

**Mitigation:**
- Implement constant-time algorithms
- Normalize all input to same form first

Sources:
- UAX #15, CWE-208: Observable Timing Discrepancy

## 7. Normalization in distributed systems

### Attack pattern: Inconsistent normalization across services

Different services normalize differently, causing state inconsistencies.

**Attack scenario:**
- Service A: Normalizes to NFC
- Service B: Normalizes to NFD
- Same identifier stored differently
- Authorization bypass possible

**Complex variant:**
- Service A: No normalization
- Service B: NFC normalization
- Service C: NFKC normalization
- Triple state inconsistency

**Detection:**
- Monitor normalization forms across services
- Alert on inconsistencies

**Mitigation:**
- Standardize normalization across all services
- Include normalization form in API contracts

Sources:
- UAX #15, CWE-436: Interpretation Conflict

## 8. Advanced detection techniques

### 8.1 Multi-layer analysis

- Combine normalization form detection with script detection
- Use machine learning for anomaly detection
- Implement context-aware normalization

### 8.2 Runtime instrumentation

- Hook normalization functions
- Track normalization form changes
- Monitor performance characteristics

### 8.3 Formal verification

- Prove normalization correctness
- Verify consistent handling across components
- Model check for edge cases

## References

- UAX #15: https://unicode.org/reports/tr15/
- UAX #29: https://unicode.org/reports/tr29/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html
- CWE-400: https://cwe.mitre.org/data/definitions/400.html
- CWE-347: https://cwe.mitre.org/data/definitions/347.html
- CWE-208: https://cwe.mitre.org/data/definitions/208.html
- CWE-436: https://cwe.mitre.org/data/definitions/436.html
