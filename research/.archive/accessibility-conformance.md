# Accessibility conformance — bim.woodfinegroup.com

**Standard:** WCAG 2.2, Level AA.
**Method:** we test with real browser automation (Playwright/Chromium) against a live instance loaded with
the production catalog dataset — not a static heuristic scan. We check every criterion below with an actual
measurement (computed styles, bounding boxes, contrast ratios, keyboard traversal, accessibility-tree
inspection), and re-check after any fix with the same method.
**Last verified:** July 2026. Scope: `/`, `/objects`, `/key-plans`, a real Key Plan detail page, `/method`.

We found two failures in this pass. Both are documented below with the exact defect, the fix we made, and
the re-verification that closed them.

---

## Summary

| Criterion | Result | Notes |
|---|---|---|
| 1.4.3 Contrast (Minimum) | **Pass** | 5/5 sampled elements checked; lowest ratio 6.71:1 against a 4.5:1 threshold |
| 1.4.10 Reflow | **Pass** (fixed this pass) | 1 failure found and fixed; see below |
| 2.1.1 Keyboard | **Pass** | Full page reachable via Tab; no keyboard traps found in the sampled path |
| 2.4.7 Focus Visible | **Pass** | Every focused element in the sampled Tab path showed a visible indicator |
| 2.5.8 Target Size (Minimum) | **Pass** (fixed this pass) | 1 failure found and fixed; see below |
| 4.1.2 Name, Role, Value | **Pass** | Accessible names present on search input, theme toggle, hamburger, drawer close |

---

## 1.4.10 Reflow — failure found and fixed

**Defect:** at a 320×400 CSS-pixel viewport (the standard proxy for 400% browser zoom), Key Plan detail
pages overflowed horizontally by 15px (`scrollWidth` 335 vs. `clientWidth` 320 on `/key-plans/po-1`). Root
cause: `.bim-bill-row__code` (the Uniclass code + "view object" link text in the parts-list table) had
`white-space: nowrap` with no `min-width: 0` on either flex sibling, so the row's content held its full
intrinsic width regardless of container size.

**Fix:** we removed `nowrap` and added `min-width: 0` to both `.bim-bill-row__name` and
`.bim-bill-row__code`, so the flex row can shrink and the code text wraps onto a second line at narrow
widths instead of forcing the row wider than its container.

**Re-verified:** `/key-plans/po-1`, `/key-plans/po-2`, `/key-plans/po-3` (the three Key Plans with the most
bill rows) all measured `scrollWidth === clientWidth === 320` at 320×400 after the fix — zero overflow.

## 2.5.8 Target Size (Minimum) — failure found and fixed

**Defect:** the compare-selection checkboxes on `/objects` measured 22×22 CSS pixels
(`.bim-cat-card__comparetoggle input` and its visible `.bim-cat-card__checkbox` sibling, both set to
`1.375rem`), below the 24×24 minimum. No exception applies — a checkbox is not an inline text link and does
not qualify for the spacing-based exception.

**Fix:** we raised both to `1.5rem` (24px), with a small corresponding adjustment to the checkmark's
`::after` position so it stays centered in the larger box.

**Re-verified:** all 7 compare checkboxes on the live `/objects` page measured exactly 24×24 CSS pixels via
`getBoundingClientRect()` after the fix. The checked state (solid fill + white checkmark) still renders
correctly centered at the new size.

## 1.4.3 Contrast (Minimum) — passed, no fix needed

We sampled five text elements across the live site and computed the contrast ratio between actual `color`
and `background-color`:

| Element | Ratio | Threshold | Result |
|---|---|---|---|
| Nav link ("Objects") | 7.09:1 | 4.5:1 | Pass |
| Hero body text | 6.71:1 | 4.5:1 | Pass |
| Footer text | 7.09:1 | 4.5:1 | Pass |
| Chip label (Uniclass filter) | 16.8:1 | 4.5:1 | Pass |
| Card meta text | 7.09:1 | 4.5:1 | Pass |

## 2.1.1 Keyboard / 2.4.7 Focus Visible — passed, no fix needed

Fifteen sequential `Tab` presses from the top of the homepage reach, in order: logo, four primary nav
links, search input, theme toggle, two in-page body links, footer nav links, the "Important Information"
disclosure summary, and an external link. Every element in that path shows a visible focus indicator
(browser-default `outline: auto` on links/buttons; a custom `2px solid` accent ring on the search input).
We found no keyboard trap in this pass.

We have not yet tested the mobile hamburger button's focus visibility at a mobile viewport width — it is
correctly absent from the desktop tab order via responsive CSS, which is why it wasn't reached above. A
dedicated mobile-viewport pass is a real follow-up item.

## 4.1.2 Name, Role, Value — passed, no fix needed

We confirmed via accessibility-tree inspection that the search input (`aria-label="Search the registry"`),
theme toggle (`aria-label="Switch to dark theme"`), hamburger menu (`aria-label="Open menu"`, native
`<details>/<summary>` disclosure semantics), and drawer close button (`aria-label="Close menu"`) all carry
a real accessible name.

We have not yet verified the theme toggle's `aria-label` update when switched to dark mode.

---

## Scope and limitations

This pass samples a representative set of pages and elements — it is not an exhaustive per-page,
per-element audit of the entire site. We name two follow-up items above. We have not separately checked
Key Plans with zero bill rows for reflow, since they render substantially less table content than the
three Private Office pages we tested; a follow-up pass will confirm this.
