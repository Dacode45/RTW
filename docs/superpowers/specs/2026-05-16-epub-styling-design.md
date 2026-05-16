# EPUB styling — design

**Date:** 2026-05-16
**Status:** Approved (pending spec review)

## Goal

Make the generated EPUBs (`RTW.epub` and `Original RTW.epub`) read like a modern trade paperback rather than a default pandoc dump. Scope is limited to **typography/body styling** and **chapter headings/scene breaks**. Cover art, front matter, and embedded fonts are out of scope.

## Aesthetic target

"Modern clean": larger serif body, generous leading, ragged-right paragraphs, restrained chapter headings with whitespace, simple centered dot-row for scene breaks. Polish comes from measure, leading, and structure — not from the specific typeface.

## Devices

Optimized for Apple Books, Kobo, and Calibre. Kindle is not a primary target; rendering there should be readable but is not tuned.

## Files added/changed

- **New:** `epub/styles.css` — single stylesheet, ~60–80 lines.
- **Changed:** `.github/workflows/build-epub.yml` — pass `--css epub/styles.css` to both pandoc invocations.
- **No changes to chapter source files.** Pandoc renders both `***` and `---` as `<hr/>`, so the existing scene-break inconsistency is resolved at the CSS layer.

## `epub/styles.css` — specification

### Body typography

- Font stack: `"Iowan Old Style", "Source Serif Pro", Charter, Georgia, serif`. Lets Apple Books pick Iowan, Kobo pick its house serif, Calibre fall back to Charter/Georgia.
- `font-size: 1em` (defer to reader's chosen base size).
- `line-height: 1.55`.
- Text alignment: `left` (ragged-right). Justified is explicitly **not** used — it is the "modern clean" choice and avoids the river-of-whitespace problem on narrow EPUB screens.
- Hyphenation: `auto`.

### Paragraphs

- `text-indent: 1.4em`.
- `margin: 0`. (Indent-not-space block style; no blank line between paragraphs.)
- First paragraph after a heading or scene break: `text-indent: 0`. Implemented via `h1 + p, hr + p { text-indent: 0; }`.

### Chapter headings (`h1`)

- `page-break-before: always` — each chapter starts on a fresh page.
- `text-align: center`.
- `margin-top: 3em; margin-bottom: 2em`.
- `font-size: 1.5em`, `font-weight: normal`, `letter-spacing: 0.04em`.
- One line; no CSS-driven break between "Chapter N:" and the title (would require source changes).

### Scene breaks (`hr`)

- `border: none`.
- Replaced by a centered three-dot row via `::before` content:
  ```css
  hr {
    border: none;
    text-align: center;
    margin: 2em 0;
  }
  hr::before {
    content: ". . .";
    letter-spacing: 0.5em;
  }
  ```
- Applies uniformly to `***` and `---` in source.

### Blockquotes (in-world documents)

- `margin: 1.2em 2em`.
- `font-size: 0.95em`.
- No left border bar; let indent and size do the work.

## Workflow changes

`.github/workflows/build-epub.yml` — add `--css epub/styles.css` to both pandoc invocations:

```yaml
- name: Build EPUB
  run: |
    pandoc -o RTW.epub --toc --toc-depth=1 \
      --css epub/styles.css \
      --metadata title="RTW" \
      --metadata author="Dacode45" \
      --metadata lang=en-US \
      $(ls book/CH*.md | sort -V)

- name: Build Original RTW EPUB
  run: |
    pandoc -o "Original RTW.epub" --toc --toc-depth=1 \
      --css epub/styles.css \
      --metadata title="Original RTW" \
      --metadata author="Dacode45" \
      --metadata lang=en-US \
      $(ls source/chapters/ch*_source.md | sort -V)
```

No other workflow changes. The rolling `latest` release step is unchanged.

## Verification

Before declaring done, build both EPUBs locally with the same pandoc invocation and open at least one in an EPUB reader (Calibre is acceptable). Spot-check:

- A chapter heading starts on a new page, centered, with generous whitespace.
- A scene-break renders as a centered three-dot row, not as a thin grey rule.
- The first paragraph after a heading and after a scene break is **not** indented; subsequent paragraphs **are** indented; there is no blank line between paragraphs.
- A blockquote (e.g. CH101's Witch's Journal entries) renders as indented italic text, not as a left-bordered box.

## Out of scope

- Cover image (`--epub-cover-image`).
- Title page, dedication, colophon, copyright page.
- Embedded fonts via `--epub-embed-font`.
- Drop caps or small caps on first line of a chapter (deferrable enhancement).
- Normalizing `***` vs `---` in source files (resolved at the CSS layer).
- Kindle-specific tuning.
- `epubcheck` validation in CI.
