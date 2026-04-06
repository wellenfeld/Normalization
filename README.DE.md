# Unicode-Normalisierungsforschung & Sicherheit

Dieses Repository bietet **umfassende Forschung** zur Unicode-Normalisierung und ihren Sicherheitsimplikationen. Es enthält dokumentierte Angriffe, praktische Beispiele und Testvektoren – alles streng referenzbasiert durch Unicode-Standards und reale CVEs.

## 🎯 Kernaussagen

- **8 wichtige Angriffsklassen** dokumentiert mit echten CVEs
- **Zeitleiste von 2013-2024** zeigt die Evolution von Unicode-Exploits
- **Funktionierender Exploit-Code** für Spotify-Entführung, SQL-Injection, Android-Umgehung
- **Schritt-für-Schritt Exploit-Methoden** mit exakten Payloads
- **Vollständige Implementierungen** mit vollständigen verwundbaren Anwendungen und Exploit-Skripten
- **50 funktionierende Payloads** für sofortiges Testen und Validieren
- **Erkennungs- und Präventionsstrategien** für jeden Angriffstyp
- **Universal Vulnerability Scanner** für umfassende Sicherheitstests

## 📚 Dokumentation

### Kernforschung
- **[Exploitation Landscape](docs/unicode-exploitation-landscape.md)** — Taxonomie von Unicode/Normalisierungs-Exploitationsklassen
- **[Exploit Timeline & Methods](docs/exploit-timeline-and-methods.md)** — Vollständige Zeitleiste mit detaillierten Exploitationstechniken (2013-2024)
- **[Widely Known Attacks](docs/widely-known-normalization-attacks.md)** — Dokumentierte CVEs (Spotify-Entführung, Android-Umgehung, Trojan Source)

### Praktische Beispiele
- **[Working Exploits](docs/working-exploit-examples.md)** — Echte funktionierende Exploits mit exakten Payloads
- **[Step-by-Step Exploits](docs/step-by-step-exploit-examples.md)** — Praktische Angriffsdurchgänge
- **[Comprehensive Examples](docs/comprehensive-exploit-examples.md)** — Vollständige Exploit-Implementierungen mit vollem Code
- **[Practical Examples](docs/practical-normalization-examples.md)** — Kopierbare Beispiele mit Code-Points

### Fortgeschrittene Themen
- **[Advanced Attacks](docs/advanced-normalization-attacks.md)** — Sophisticated Exploitationsmuster
- **[Real-World Cases](docs/real-world-normalization-exploits.md)** — Erkennungs- und Abwehrstrategien
- **[Identifier Normalization and Confusables](docs/identifier-normalization-and-confusables.md)** — Bezeichner, Default-Ignorables, Confusables

### Technische Tiefenanalyse
- **[Normalization Deep Divergence and Stability](docs/normalization-deep-divergence-and-stability.md)** — Kompositions-Ausschlüsse, Stream-Safe-Format, Stabilitätsgarantien
- **[Linter/Parser Normalization Issues](docs/linter-parser-normalization-issues.md)** — Linter/Parser-Fehlermodi mit Unicode
- **[URL Percent Encoding and Normalization](docs/url-percent-encoding-and-normalization.md)** — Wie NFC vs NFD percent-kodierte URLs verändert
- **[Source Code Bidi and Invisible Characters](docs/source-code-bidi-and-invisible-characters.md)** — Bidi-Steuerzeichen und Quellcode-Angriffe

## 🧪 Testvektoren

### Kern-Exploit-Vektoren
- **[Working Exploits](data/vectors/real_world_exploit_scenarios.json)** — Real-World-Exploits-Muster
- **[Advanced Vectors](data/vectors/advanced_attack_vectors.json)** — Sophisticated Angriffsvektoren
- **[Comprehensive Payloads](data/vectors/comprehensive_working_payloads.json)** — 50 funktionierende Unicode-Exploit-Payloads

### Technische Vektoren
- **[URL Encoding](data/vectors/url_percent_encoding_nfc_nfd.json)** — NFC vs NFD Percent-Encoding-Divergenz
- **[Apostrophe Lookalikes](data/vectors/url_apostrophe_lookalikes.json)** — Unterscheidbare Apostroph-ähnliche Zeichen
- **[Bidi Controls](data/vectors/source_code_bidi_controls.json)** — Quellcode-Steuerzeichen
- **[Identifier Confusables](data/vectors/identifier_confusable_homoglyph.json)** — Mixed-Script-Lookalikes
- **[Composition Exclusions](data/vectors/normalization_composition_exclusions.json)** — UAX #15 Ausschlusstypen
- **[Stream-Safe Format](data/vectors/normalization_stream_safe.json)** — Stream-Safe-Garantien

## 🚀 Schnellstart

### Testen Sie Ihre Anwendungen
```bash
# Test mit umfassenden Payloads
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

### Scannen Sie auf Schwachstellen
```python
# Universal Vulnerability Scanner verwenden
from docs.comprehensive_exploit_examples import UnicodeVulnerabilityScanner

scanner = UnicodeVulnerabilityScanner()
scanner.scan_input("admin%uff07 UNION SELECT * FROM users --", "sql_injection")
```

## Geltungsbereich (autoritativ)

- **Unicode-Normalisierungsformen (UAX #15 / ISO 10646 Ausrichtung)**
  - `NFD`, `NFC`, `NFKD`, `NFKC`
  - Kanonische Ordnung (Neuordnung kombinierender Markierungen)
  - Kanonische Komposition (Rekomposition)
  - Hangul algorithmische Dekomposition/Komposition
  - Stream-Safe Text Format (UAX #15 §13)
- **Normalisierungs-adjacente Prozesse** (nicht "Normalisierungsformen", aber oft damit verwechselt)
  - **IDNA-Verarbeitung** und ihre Normalisierungsanforderungen (UTS #46 verwendet NFC als Schritt)
  - Case Folding (nicht Normalisierung, aber oft kombiniert mit NFKC für "Bezeichner-Normalisierung")
  - Sicherheitsbezogene Normalisierungsanleitungen (z.B. Confusables werden nicht durch NFC/NFKC gelöst)

Außerhalb des Geltungsbereichs, es sei denn, später explizit hinzugefügt:

- Locale-spezifische Kollation oder "String-Vergleich" über Normalisierung hinaus.
- Grapheme-Cluster-Segmentierung, Rendering, Shaping (Normalisierung kann sie beeinflussen, definiert sie aber nicht).

## Dokumentation

- `docs/unicode-exploitation-landscape.md` — Taxonomie von Unicode/Normalisierungs-Exploitationsklassen
- `docs/widely-known-normalization-attacks.md` — dokumentierte CVEs und öffentliche Exploits (Spotify, Android, Trojan Source)
- `docs/step-by-step-exploit-examples.md` — praktische, leicht verständliche Exploit-Durchgänge
- `docs/advanced-normalization-attacks.md` — sophisticated Exploitationsmuster und komplexe Ausbeutung
- `docs/real-world-normalization-exploits.md` — konkrete Exploit-Fälle und Erkennungs-/Abwehrstrategien
- `docs/practical-normalization-examples.md` — konkrete, kopierbare Beispiele mit Code-Points und UTF-8-Bytes
- `docs/identifier-normalization-and-confusables.md` — Bezeichner, Default-Ignorables, Confusables
- `docs/normalization-deep-divergence-and-stability.md` — Kompositions-Ausschlüsse, Stream-Safe-Format, Stabilitätsgarantien
- `docs/linter-parser-normalization-issues.md` — Linter/Parser-Fehlermodi mit Unicode
- `docs/url-percent-encoding-and-normalization.md` — wie NFC vs NFD percent-kodierte URLs verändert
- `docs/source-code-bidi-and-invisible-characters.md` — Bidi-Steuerzeichen und Quellcode-Angriffe
- `docs/exploit-timeline-and-methods.md` — vollständige Zeitleiste mit detaillierten Exploitationstechniken
- `docs/working-exploit-examples.md` — echte funktionierende Exploits mit exakten Payloads
- `docs/comprehensive-exploit-examples.md` — vollständige Exploit-Implementierungen mit vollem Code

## Testvektoren

- `data/vectors/url_percent_encoding_nfc_nfd.json` — NFC vs NFD Percent-Encoding-Divergenz
- `data/vectors/url_apostrophe_lookalikes.json` — unterscheidbare Apostroph-ähnliche Zeichen
- `data/vectors/source_code_bidi_controls.json` — Bidi-Steuerzeichen im Quellcode
- `data/vectors/identifier_confusable_homoglyph.json` — Mixed-Script-Lookalike-Bezeichner
- `data/vectors/normalization_composition_exclusions.json` — Kompositions-Ausschlusstypen
- `data/vectors/normalization_stream_safe.json` — Stream-Safe-Format-Garantien
- `data/vectors/real_world_exploit_scenarios.json` — Real-World-Exploits-Muster
- `data/vectors/advanced_attack_vectors.json` — sophisticated Angriffsvektoren
- `data/vectors/comprehensive_working_payloads.json` — 50 funktionierende Unicode-Exploit-Payloads

## Terminologie (präzise)

- **Code Point**: Ein Unicode-Skalarwert (z.B. `U+00E9`).
- **Code Unit**: Kodierungseinheit (UTF-8 Byte, UTF-16 16-Bit-Einheit, etc.). Normalisierung ist über Code-Points definiert, nicht über Code-Units.
- **Kanonische Äquivalenz**: Zwei Strings repräsentieren das "gleiche abstrakte Zeichen" unter kanonischer Dekomposition und kanonischer Ordnung. (UAX #15 §1.1)
- **Kompatibilitätsäquivalenz**: Schwächere Beziehung, bei der Zeichen in bestimmten Kontexten stilistisch oder semantisch unterschiedlich sein können, aber in anderen gleich behandelt werden können. (UAX #15 §1.1)
- **Starter**: Ein Code-Point mit kanonischer kombinierender Klasse (ccc) = 0.
- **Non-Starter**: Ein Code-Point mit ccc != 0.

## Der Unicode-Normalisierungsalgorithmus (UAX #15 Zusammenfassung)

UAX #15 beschreibt Normalisierung als:

1. **Vollständige Dekomposition**
   - Für `NFD`/`NFC`: vollständige **kanonische** Dekomposition.
   - Für `NFKD`/`NFKC`: vollständige **Kompatibilitäts**-Dekomposition.
   - Verwendet `Decomposition_Mapping`-Werte (aus der Unicode Character Database), plus spezielle algorithmische Regeln für Hangul-Silben.
2. **Kanonischer Ordnungsalgorithmus**
   - Ordnet kombinierende Markierungen basierend auf `Canonical_Combining_Class` (ccc) neu.
   - Betrifft nur Non-Starters (ccc != 0).
3. **Kanonischer Kompositionsalgorithmus** (nur für komponierte Formen)
   - Für `NFC` und `NFKC`: Rekombination wo erlaubt und nicht blockiert/ausgeschlossen.
   - Muss Kompositions-Ausschlüsse und Blockierungsregeln berücksichtigen.

Quelle: UAX #15 §1.3.

## Was jede Normalisierungsform garantiert

- **NFD**
  - Vollständige kanonische Dekomposition + kanonische Ordnung.
  - Keine kanonische Komposition durchgeführt.
- **NFC**
  - Äquivalent zu NFD, dann kanonische Komposition.
  - Häufige "empfohlene Interchange"-Normalisierung für allgemeinen Text.
- **NFKD**
  - Vollständige Kompatibilitäts-Dekomposition + kanonische Ordnung.
  - Kann Formatierungsunterschiede entfernen (z.B. Kompatibilitätszeichen).
- **NFKC**
  - Äquivalent zu NFKD, dann kanonische Komposition.
  - Wird oft als Teil von "Bezeichner-Normalisierungs"-Pipelines verwendet, kann aber die Bedeutung in einigen Domänen ändern (nicht sicher als universelle Voreinstellung).

## Verhaltenshinweise zu spezifischen Eingabekategorien

Dieser Abschnitt ist absichtlich konkret. Wenn Sie hier Behauptungen hinzufügen, müssen Sie sie untermauern mit:

- Ein Zitat zum Unicode-Standard / UAX / UTS / UCD, **und**
- Ein ausführbarer sprachübergreifender Test (in `tests/` oder `data/vectors/`).

### ASCII

- Alle Normalisierungsformen lassen reinen ASCII (`U+0000..U+007F`) unverändert.
  - UAX #15 merkt diese Eigenschaft explizit an (UAX #15 §1.3).

### Latin-1

- Text ausschließlich in Latin-1 (`U+0000..U+00FF`) wird durch `NFC` nicht verändert.
  - UAX #15 §1.3.

### Vorkomponierte vs dekomponierte Zeichen

Beispiel (kanonische Äquivalenz):

- `"e" + U+0301 COMBINING ACUTE ACCENT` (dekomponiert) und `U+00E9 "é"` (vorkomponiert) sind kanonisch äquivalent.
- `NFD("é")` erzeugt die dekomponierte Sequenz.
- `NFC("e\u0301")` erzeugt die vorkomponierte Form, wenn Komposition verfügbar und nicht blockiert ist.

### Neuordnung kombinierender Markierungen (kanonische Ordnung)

Normalisierung ordnet **nur** nach kanonischer kombinierender Klasse (ccc) neu, nicht nach visueller Präferenz.

Wichtige Implikationen:

- Kanonische Ordnung kann eine kombinierende Markierung früher im String relativ zu anderen kombinierenden Markierungen verschieben.
- Sie überschreitet **keine** Starter-Grenze.
- Extrem lange Sequenzen von Non-Startern sind legal; Stream-Safe-Format adressiert Puffer-Hazards.

### Hangul-Silben (algorithmisch)

Hangul-Silben dekomponieren/komponieren algorithmisch (nicht über explizite Tabellen) gemäß dem Unicode-Standard.

Praktische Implikationen:

- `NFD` von Hangul-Silben erzeugt Jamo-Sequenzen.
- `NFC` kann gültige Jamo-Sequenzen wieder zu Silben rekombinieren.

### Kompositions-Ausschlüsse

Einige Zeichen sind von der Komposition ausgeschlossen.

- UAX #15 beschreibt eine `Composition_Exclusion`-abgeleitete Eigenschaft und merkt an, dass **kein Kompositions-Ausschluss-Zeichen in irgendeiner normalisierten Form auftritt**. (UAX #15 §5)

### Stream-Safe Text Format (UAX #15)

Dies ist keine Normalisierungsform, sondern ein Format nützlich für Streaming/gepufferte Implementierungen.

- Stream-Safe-Text hat keine Sequenzen von Non-Startern länger als 30, wenn zu NFKD normalisiert.
- Der Stream-Safe-Prozess kann `U+034F COMBINING GRAPHEME JOINER (CGJ)` einfügen, um Sequenzen aufzubrechen.

Quelle: UAX #15 §13.

## IDNA und Normalisierung (UTS #46)

Internationalisierte Domain-Namen beinhalten eine separate Verarbeitungs-Pipeline.

- UTS #46 führt Mapping durch, dann **normalisiert den Domain-Namen-String zu NFC** als expliziten Schritt. (UTS #46 §4 "Normalize. Normalize the domain_name string to Unicode Normalization Form C.")
- Gültigkeitskriterien für Labels beinhalten, dass sie in NFC sind. (UTS #46 §4.1)

Wichtig: IDNA-Verarbeitung ist nicht "nur NFC". Sie umfasst Mapping-Tabellen, verbotene/ignorierte Code-Points, Punycode-Konversion und zusätzliche Validierung.

## Sprachübergreifende Realität (was Sie verifizieren müssen)

Verschiedene Ökosysteme exposieren Unicode-Normalisierung unterschiedlich und können zusätzliches Verhalten umfassen bezüglich:

- Welcher Unicode-Version ihre Normalisierungsdaten entsprechen.
- Ob sie auch "NFKC_Casefold"-artige Pipelines anbieten.
- Ob sie standardmäßig in Bezeichnern, Dateisystemen oder Networking-Stacks normalisieren.

Dieses Repository behandelt sprachübergreifendes Verhalten als *testbare Artefakte*, nicht Annahmen.

## Repository-Struktur

- `docs/`
  - Langform-Notizen und Deep-Dives (müssen referenzbasiert sein).
- `data/`
  - Kanonische Testvektoren und extern bezogene Konformanzdaten.
- `data/vectors/`
  - Kuratierte Beispiele mit erwarteten Ausgaben und Erklärungen.
- `implementations/`
  - Pro-Sprache-Experimente und Wrapper.
- `tests/`
  - Sprachübergreifende Test-Harnesses (im Laufe der Zeit hinzugefügt).

## Konformanz und Testdaten

UAX #15 erfordert, dass Normalizer Ergebnisse erzeugen können, die den Unicode-Konformanz-Testdaten entsprechen.

- UAX #15 Konformanzklausel referenziert `NormalizationTest.txt` (UAX #15 §4, Klausel UAX15-C3).
- UTS #46 stellt `IdnaTestV2.txt` für Konformanztests bereit.

Dieses Repository wird verfolgen:

- Woher Testdaten stammen.
- Exakte Unicode-Version.
- Prüfsummen (wenn wir mit dem Import von Dateien beginnen).

## Strikte Regeln für Beiträge

Alle Beiträge müssen `AGENTS.md` folgen.

## Referenzen (primär)

- Unicode Standard Annex #15: Unicode Normalization Forms
  - https://unicode.org/reports/tr15/
- Unicode Technical Standard #46: Unicode IDNA Compatibility Processing
  - https://unicode.org/reports/tr46/
