# Widely known Unicode normalization attacks

This document documents publicly known and widely discussed Unicode normalization attacks and vulnerabilities. These are real-world cases that have been discovered, exploited, and documented in security advisories, CVEs, and industry blog posts.

## 1. Spotify Account Hijacking (2013)

### Attack type: Non-idempotent canonicalization

**Summary:** Attackers could hijack any Spotify account by creating a username with mathematical bold characters that normalized differently at different stages of the authentication process.

**Technical details:**
- Attacker creates account with username `ᴮᴵᴳᴮᴵᴿᴰ` (U+1D2E U+1D35 U+1D33 U+1D2E U+1D35 U+1D3F U+1D30)
- First `nodeprep.prepare()` call: `ᴮᴵᴳᴮᴵᴿᴰ` → `BIGBIRD`
- Second `nodeprep.prepare()` call: `BIGBIRD` → `bigbird`
- Account registration used first result, password reset used second result
- Result: Password reset for `ᴮᴵᴳᴮᴵᴿᴰ` changed password for existing `bigbird` account

**Root cause:** XMPP's `nodeprep.prepare()` was not idempotent when handling mathematical characters.

**Impact:** Any Spotify account could be hijacked.

**Sources:**
- Spotify Engineering blog: https://engineering.atspotify.com/2013/06/creative-usernames
- CVE: Not assigned (pre-CVE era disclosure)

## 2. SQL Injection via NFKC Expansion

### Attack type: Post-filtering normalization

**Summary:** FULLWIDTH APOSTROPHE (U+FF07) normalizes to regular apostrophe (U+0027) after quote stripping, enabling SQL injection.

**Technical details:**
- Application strips single quotes to prevent SQL injection
- Input: `chloe%uff07 UNION SELECT username, password from users --`
- After quote stripping: `chloe%uff07 UNION SELECT username, password from users --`
- After NFKD normalization: `chloe' UNION SELECT username, password from users --`
- Result: SQL injection succeeds despite filtering

**Root cause:** Normalization applied after input sanitization.

**Impact:** SQL injection bypassing input filters.

**Sources:**
- AppCheck blog: https://appcheck-ng.com/unicode-normalization-vulnerabilities-the-special-k-polyglot/
- General technique, no specific CVE

## 3. Android File Path Filter Bypass (CVE-2024-43093)

### Attack type: Incorrect normalization in file path validation

**Summary:** Android's ExternalStorageProvider had incorrect Unicode normalization allowing bypass of file path filters designed to prevent access to sensitive directories.

**Technical details:**
- Function: `shouldHideDocument` in `ExternalStorageProvider.java`
- Issue: Incorrect Unicode normalization
- Impact: Local privilege escalation by bypassing file path filters
- Affected versions: Android 12 through 15

**Root cause:** File path normalization inconsistencies between validation and actual file access.

**Impact:** Local privilege escalation with no additional execution privileges needed.

**Sources:**
- CVE-2024-43093: https://nvd.nist.gov/vuln/detail/CVE-2024-43093
- Wiz vulnerability analysis: https://www.wiz.io/vulnerability-database/cve/cve-2024-43093

## 4. Trojan Source Attacks (CVE-2021-42574, CVE-2021-42694)

### Attack type: Bidirectional control character exploitation

**Summary:** Unicode bidirectional control characters can reorder source code visually without changing logical order, enabling hidden malicious code.

**Technical details:**
- Uses U+202E (RIGHT-TO-LEFT OVERRIDE) and other bidi controls
- Visual order differs from logical token order
- Code reviewers see safe code, compilers execute malicious code
- Affects multiple programming languages and tools

**Root cause:** Tools not handling bidirectional controls consistently.

**Impact:** Supply chain attacks, hidden malicious code in repositories.

**Sources:**
- Trojan Source website: https://trojansource.codes/
- CVE-2021-42574: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42574
- CVE-2021-42694: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42694

## 5. IDNA Homograph Attacks

### Attack type: Domain name spoofing via Unicode

**Summary:** Attackers register domain names with visually similar characters to legitimate domains, enabling phishing attacks.

**Technical details:**
- Uses characters from different scripts that look identical
- Example: `аррӏе.com` (Cyrillic) vs `apple.com` (Latin)
- IDNA processing can normalize but doesn't prevent all confusables
- Browsers may display punycode or original Unicode

**Root cause:** Unicode allows multiple representations of similar-looking characters.

**Impact:** Phishing, domain spoofing, brand impersonation.

**Sources:**
- UTS #39: Unicode Security Mechanisms
- Multiple CVEs related to IDNA processing

## 6. Unicode Normalization in Web Applications

### Attack type: Inconsistent normalization across components

**Summary:** Web applications that normalize inconsistently across different components can lead to security bypasses.

**Technical details:**
- Database stores NFC form
- Cache key uses NFD form
- Search uses NFKC form
- Results: Cache misses, authorization bypasses, data inconsistencies

**Root cause:** Different normalization forms used in different parts of the application.

**Impact:** Authorization bypass, cache poisoning, data integrity issues.

**Sources:**
- Various security blog posts and CVEs
- General architectural pattern

## 7. Special K Polyglot Technique

### Attack type: Multi-encoding bypass

**Summary:** Uses Unicode characters that can be interpreted differently in various encodings, bypassing security filters.

**Technical details:**
- Characters that normalize to dangerous sequences
- Bypasses WAFs and input filters
- Works across multiple programming languages

**Root cause:** Inconsistent handling of Unicode across security tools.

**Impact:** WAF bypass, input filter evasion, XSS/SQL injection.

**Sources:**
- AppCheck blog: https://appcheck-ng.com/unicode-normalization-vulnerabilities-the-special-k-polyglot/

## Common Patterns in These Attacks

### 1. Timing issues
- Normalization applied before vs after filtering
- Multiple normalization passes changing results
- Different components using different forms

### 2. Idempotency failures
- Functions not idempotent when they should be
- Multiple applications yielding different results
- Spotify case is classic example

### 3. Visual vs logical mismatch
- Bidirectional controls reordering display
- Homograph characters looking identical
- Trojan Source attacks

### 4. Encoding layer confusion
- UTF-8 vs UTF-16 vs UTF-32 differences
- Percent-encoding exposing byte differences
- URL encoding bypasses

## Detection and Prevention

### 1. Consistent normalization
- Use same normalization form everywhere
- Normalize before any processing
- Never normalize after filtering

### 2. Idempotency verification
- Test canonicalization functions
- Verify multiple applications yield same result
- Use Unicode-approved algorithms

### 3. Input validation
- Validate before normalization
- Use allowlists instead of blocklists
- Consider script restrictions

### 4. Output encoding
- Encode consistently
- Use proper escaping
- Consider visual rendering

## References

- CVE-2024-43093: https://nvd.nist.gov/vuln/detail/CVE-2024-43093
- CVE-2021-42574: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42574
- CVE-2021-42694: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42694
- Spotify Engineering: https://engineering.atspotify.com/2013/06/creative-usernames
- AppCheck: https://appcheck-ng.com/unicode-normalization-vulnerabilities-the-special-k-polyglot/
- Trojan Source: https://trojansource.codes/
- UTS #39: https://unicode.org/reports/tr39/
- UAX #15: https://unicode.org/reports/tr15/
