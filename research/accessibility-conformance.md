# Accessibility conformance — bim.woodfinegroup.com

**Standard:** WCAG 2.2, Level AA.
**Method:** real browser automation (Playwright/Chromium) against a live instance loaded with the
production catalog dataset — not a static heuristic scan, not an assumption. Every criterion below was
checked with an actual measurement (computed styles, bounding boxes, contrast ratios, keyboard traversal,
accessibility-tree inspection) and, where a failure was found, re-checked after a fix with the same method.
**Last verified:** 2026-07-10, against local preview build (Round 5). Scope: `/`, `/objects`,
`/compositions`, a real composition detail page, `/method`.

This document exists because the site is expected to hold up under real audit scrutiny, not because a
badge was wanted. Two real failures were found in this pass; both are documented below with the exact
defect, the fix, and the re-verification that closed them — nothing here was declared conformant without
a live check.

---

## Summary

| Criterion | Result | Notes |
|---|---|---|
| 1.4.3 Contrast (Minimum) | **Pass** | 5/5 sampled elements checked; lowest ratio 6.71:1 against a 4.5:1 threshold |
| 1.4.10 Reflow | **Pass** (fixed this pass) | 1 real failure found and fixed; see below |
| 2.1.1 Keyboard | **Pass** | Full page reachable via Tab; no keyboard traps found in the sampled path |
| 2.4.7 Focus Visible | **Pass** | Every focused element in the sampled Tab path showed a visible indicator |
| 2.5.8 Target Size (Minimum) | **Pass** (fixed this pass) | 1 real failure found and fixed; see below |
| 4.1.2 Name, Role, Value | **Pass** | Accessible names present on search input, theme toggle, hamburger, drawer close |

---

## 1.4.10 Reflow — real failure found and fixed

**Defect found:** at a 320×400 CSS-pixel viewport (the standard proxy for 400% browser zoom), composition
detail pages overflowed horizontally by 15px (`scrollWidth` 335 vs. `clientWidth` 320 on `/compositions/po-1`).
Root cause: `.bim-bill-row__code` (the Uniclass code + "view object" link text in the parts-list table) had
`white-space: nowrap` with no `min-width: 0` on either flex sibling, so the row's content held its full
intrinsic width regardless of container size.

**Fix:** removed `nowrap`; added `min-width: 0` to both `.bim-bill-row__name` and `.bim-bill-row__code` so
the flex row can shrink and the code text wraps onto a second line at narrow widths instead of forcing the
row wider than its container.

**Re-verified:** `/compositions/po-1`, `/compositions/po-2`, `/compositions/po-3` (the three compositions
with the most bill rows) all measured `scrollWidth === clientWidth === 320` at 320×400 after the fix — zero
overflow.

## 2.5.8 Target Size (Minimum) — real failure found and fixed

**Defect found:** the compare-selection checkboxes on `/objects` measured 22×22 CSS pixels
(`.bim-cat-card__comparetoggle input` and its visible `.bim-cat-card__checkbox` sibling, both set to
`1.375rem`), below the 24×24 minimum. No exception applies — a checkbox is not an inline text link and does
not qualify for the spacing-based exception.

**Fix:** raised both to `1.5rem` (24px), with a small corresponding adjustment to the checkmark's `::after`
position so it stays centered in the larger box.

**Re-verified:** all 7 compare checkboxes on the live `/objects` page measured exactly 24×24 CSS pixels via
`getBoundingClientRect()` after the fix. Visual check confirmed the checked state (solid fill + white
checkmark) still renders correctly centered, not misaligned, at the new size.

## 1.4.3 Contrast (Minimum) — passed, no fix needed

Five real text elements sampled across the live site, contrast ratio computed between actual `color` and
`background-color`:

| Element | Ratio | Threshold | Result |
|---|---|---|---|
| Nav link ("Objects") | 7.09:1 | 4.5:1 | Pass |
| Hero body text | 6.71:1 | 4.5:1 | Pass |
| Footer text | 7.09:1 | 4.5:1 | Pass |
| Chip label (Uniclass filter) | 16.8:1 | 4.5:1 | Pass |
| Card meta text | 7.09:1 | 4.5:1 | Pass |

## 2.1.1 Keyboard / 2.4.7 Focus Visible — passed, no fix needed

Fifteen sequential `Tab` presses from the top of the homepage reached, in order: logo, four primary nav
links, search input, theme toggle, two in-page body links, footer nav links, the "Important Information"
disclosure summary, and an external link — every element in that path showed a non-`none` focus indicator
(browser-default `outline: auto` on links/buttons; a custom `2px solid` accent ring on the search input). No
keyboard trap was found in this pass.

**Known gap, not yet closed:** the mobile hamburger button's focus visibility was not directly tested at a
mobile viewport width in this pass (it is correctly absent from the desktop tab order via responsive CSS,
which is why it wasn't reached above) — a dedicated mobile-viewport Tab pass is a real follow-up item, not
yet done.

## 4.1.2 Name, Role, Value — passed, no fix needed

Confirmed via accessibility-tree inspection: search input (`aria-label="Search the registry"`), theme
toggle (`aria-label="Switch to dark theme"`), hamburger menu (`aria-label="Open menu"`, native
`<details>/<summary>` disclosure semantics), drawer close button (`aria-label="Close menu"`) — all carry a
real accessible name.

**Known gap, not yet checked:** the theme toggle's `aria-label` update when switched to dark mode was not
verified in this pass.

---

## Scope and honest limitations

This pass sampled a representative set of pages and elements — it is not an exhaustive per-page,
per-element audit of the entire site. Two known follow-up items are named above rather than silently
omitted. Compositions with zero bill rows (Corporate Office, and the 14 room-programme-only entries) were
not separately checked for reflow, since they render substantially less table content than the three
Private Office pages tested; a follow-up pass should confirm this assumption rather than take it on faith.
