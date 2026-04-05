# Identifier exploitation: normalization, default-ignorables, confusables

This document focuses on identifiers (programming language identifiers, user handles, account names, etc.).

## 1. Normalization and case in identifiers (UAX #31)

UAX #31 §5 (“Normalization and Case”) discusses the need to consider normalization and case folding for identifiers and defines requirements such as:

- **UAX31-R4**: Equivalent Normalized Identifiers (implementation specifies a normalization form; identifiers with the same normalized form are equivalent, subject to exclusions).

UAX #31 also discusses Default_Ignorable_Code_Points in identifiers and why they are problematic.

Sources:

- UAX #31 §5: https://unicode.org/reports/tr31/
- UAX #31 §2.3: https://unicode.org/reports/tr31/

## 2. Default-ignorables: invisible differences

UAX #31 §2.3 explains that Default_Ignorable_Code_Points (e.g., bidi controls, joiners, variation selectors) are problematic in identifiers because:

- They often have no visible display.
- They can create strings that look identical but contain different characters.

Source: UAX #31 §2.3 (https://unicode.org/reports/tr31/).

## 3. Confusables and skeleton matching (UTS #39)

UTS #39 defines a confusable detection mechanism via skeleton computation.

In particular, UTS #39 defines `internalSkeleton(X)` to:

1. Convert X to NFD (UAX #15).
2. Remove Default_Ignorable_Code_Point characters.
3. Map each character to a prototype per the confusables data.
4. Reapply NFD.

Source: UTS #39 §4 (https://unicode.org/reports/tr39/).

## 4. Minimal vectors

This repo includes minimal vectors illustrating:

- Mixed-script lookalikes (homoglyph-style risks)
- Identifier strings that differ only in code points but can be visually confusable

See: `data/vectors/identifier_confusable_homoglyph.json`.

## References

- UAX #15: https://unicode.org/reports/tr15/
- UAX #31: https://unicode.org/reports/tr31/
- UTS #39: https://unicode.org/reports/tr39/
- UTS #55: https://www.unicode.org/reports/tr55/
