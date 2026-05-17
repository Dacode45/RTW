# EPUB Styling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply a "modern clean" CSS stylesheet to both `RTW.epub` and `Original RTW.epub` builds so the generated EPUBs read like a trade paperback rather than a default pandoc dump.

**Architecture:** One new file (`epub/styles.css`) containing all typography, chapter heading, scene-break, and blockquote rules. Two lines added to `.github/workflows/build-epub.yml` to pass `--css epub/styles.css` to each pandoc invocation. No chapter source files change.

**Tech Stack:** Pandoc EPUB writer, plain CSS (no preprocessor), GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-05-16-epub-styling-design.md`

---

## File Structure

- **Create:** `epub/styles.css` — single stylesheet with body typography, paragraph rules, chapter heading, scene-break (`hr`), and blockquote rules.
- **Modify:** `.github/workflows/build-epub.yml` — add `--css epub/styles.css` to both pandoc commands (lines 26 and 34).
- **Unchanged:** All files in `book/` and `source/chapters/`.

## Verification approach

CSS for EPUB output has no automated test framework — verification is visual. The plan installs pandoc locally on Windows (via `winget`), builds both EPUBs, and opens at least one in an EPUB reader (Calibre or Apple Books via iCloud; the user picks whichever they have). A short spot-check list confirms the spec is satisfied.

---

## Task 1: Create `epub/styles.css`

**Files:**
- Create: `epub/styles.css`

- [ ] **Step 1: Confirm the `epub/` directory does not exist yet**

Run:
```powershell
Test-Path epub
```
Expected: `False`. If `True`, list its contents with `Get-ChildItem epub` and stop to investigate before proceeding.

- [ ] **Step 2: Create the file with the full stylesheet**

Use the Write tool to create `epub/styles.css` with exactly this content:

```css
/* RTW EPUB stylesheet — modern clean trade-paperback look.
   Target readers: Apple Books, Kobo, Calibre. Not tuned for Kindle. */

body {
  font-family: "Iowan Old Style", "Source Serif Pro", Charter, Georgia, serif;
  font-size: 1em;
  line-height: 1.55;
  text-align: left;
  -webkit-hyphens: auto;
  hyphens: auto;
}

p {
  text-indent: 1.4em;
  margin: 0;
}

h1 + p,
hr + p {
  text-indent: 0;
}

h1 {
  page-break-before: always;
  text-align: center;
  margin-top: 3em;
  margin-bottom: 2em;
  font-size: 1.5em;
  font-weight: normal;
  letter-spacing: 0.04em;
}

hr {
  border: none;
  text-align: center;
  margin: 2em 0;
  height: auto;
}

hr::before {
  content: ". . .";
  letter-spacing: 0.5em;
}

blockquote {
  margin: 1.2em 2em;
  font-size: 0.95em;
}
```

- [ ] **Step 3: Verify the file exists and is non-empty**

Run:
```powershell
Get-Item epub/styles.css | Select-Object Name, Length
```
Expected: A row showing `styles.css` with `Length` > 500.

---

## Task 2: Wire the stylesheet into the GitHub Actions workflow

**Files:**
- Modify: `.github/workflows/build-epub.yml` (lines 24–38)

- [ ] **Step 1: Read the current workflow file**

Use the Read tool on `.github/workflows/build-epub.yml`. Confirm the two pandoc invocations are present at lines 24–30 (first build) and 32–38 (second build).

- [ ] **Step 2: Add `--css` flag to the first pandoc invocation**

Use Edit to replace:

```
          pandoc -o RTW.epub --toc --toc-depth=1 \
            --metadata title="RTW" \
            --metadata author="Dacode45" \
            --metadata lang=en-US \
            $(ls book/CH*.md | sort -V)
```

with:

```
          pandoc -o RTW.epub --toc --toc-depth=1 \
            --css epub/styles.css \
            --metadata title="RTW" \
            --metadata author="Dacode45" \
            --metadata lang=en-US \
            $(ls book/CH*.md | sort -V)
```

- [ ] **Step 3: Add `--css` flag to the second pandoc invocation**

Use Edit to replace:

```
          pandoc -o "Original RTW.epub" --toc --toc-depth=1 \
            --metadata title="Original RTW" \
            --metadata author="Dacode45" \
            --metadata lang=en-US \
            $(ls source/chapters/ch*_source.md | sort -V)
```

with:

```
          pandoc -o "Original RTW.epub" --toc --toc-depth=1 \
            --css epub/styles.css \
            --metadata title="Original RTW" \
            --metadata author="Dacode45" \
            --metadata lang=en-US \
            $(ls source/chapters/ch*_source.md | sort -V)
```

- [ ] **Step 4: Verify both invocations now include `--css`**

Use Grep:
```
pattern: --css epub/styles.css
path: .github/workflows/build-epub.yml
output_mode: count
```
Expected: `2` matches.

---

## Task 3: Install pandoc locally and build both EPUBs

**Files:** none (operational task)

- [ ] **Step 1: Check whether pandoc is already installed**

Run:
```powershell
(Get-Command pandoc -ErrorAction SilentlyContinue).Source
```
If output is empty, proceed to Step 2. If output is a path, skip to Step 3.

- [ ] **Step 2: Install pandoc via winget**

Run:
```powershell
winget install --id JohnMacFarlane.Pandoc -e --accept-package-agreements --accept-source-agreements
```
Expected: "Successfully installed". If winget is unavailable, ask the user to install pandoc from <https://pandoc.org/installing.html> and resume from Step 3.

After install, re-run `(Get-Command pandoc -ErrorAction SilentlyContinue).Source` in a fresh shell to verify. The CI workflow uses Linux pandoc; the local Windows install is only for verification.

- [ ] **Step 3: Build `RTW.epub` locally**

Use Bash (the workflow's invocation is bash-style; reproducing it via PowerShell needs a slightly different file-listing syntax). Run:
```bash
pandoc -o RTW.epub --toc --toc-depth=1 \
  --css epub/styles.css \
  --metadata title="RTW" \
  --metadata author="Dacode45" \
  --metadata lang=en-US \
  $(ls book/CH*.md | sort -V)
```
Expected: command exits 0, `RTW.epub` appears at the repo root.

- [ ] **Step 4: Build `Original RTW.epub` locally**

Run:
```bash
pandoc -o "Original RTW.epub" --toc --toc-depth=1 \
  --css epub/styles.css \
  --metadata title="Original RTW" \
  --metadata author="Dacode45" \
  --metadata lang=en-US \
  $(ls source/chapters/ch*_source.md | sort -V)
```
Expected: command exits 0, `Original RTW.epub` appears at the repo root.

- [ ] **Step 5: Confirm both EPUBs exist and are non-trivial in size**

Run:
```powershell
Get-Item RTW.epub, "Original RTW.epub" | Select-Object Name, Length
```
Expected: both rows show `Length` > 500,000 (each EPUB is hundreds of KB to a few MB given 600+ chapters).

---

## Task 4: Visually verify the rendering

**Files:** none (visual inspection)

- [ ] **Step 1: Open `RTW.epub` in an EPUB reader**

Options (pick whichever is already installed):
- **Calibre** — `calibre RTW.epub` from a shell, or drag-drop into the Calibre library and click "View".
- **Apple Books** — copy `RTW.epub` into `~/iCloud Drive/Books` (Mac) or use iCloud sync from Windows.
- **Thorium Reader** — free Windows EPUB reader, drag-drop the file.

If none are installed, install Calibre: `winget install --id calibre.calibre -e`.

- [ ] **Step 2: Spot-check four specifics on Chapter 1 ("From Today Onwards, I Am a Royal Prince")**

Confirm each:

1. **Chapter heading:** "Chapter 1: From Today Onwards, I Am a Royal Prince" appears centered, on a fresh page, with generous whitespace above and below. Font weight is regular (not bold) and roughly 1.5× body size.
2. **Scene break:** the `---` between paragraphs (around the original line 47) renders as a centered three-dot row ("`. . .`"), not as a thin grey horizontal rule.
3. **Paragraph indents:** the first paragraph under the chapter heading is **not** indented. The second paragraph **is** indented. There is no blank line between paragraphs.
4. **Body text:** ragged-right (not justified), comfortable line height, serif font.

- [ ] **Step 3: Spot-check blockquote rendering on Chapter 101**

Open Chapter 101 (the Witch's Journal scene). Confirm the blockquoted journal entries render as indented italic paragraphs **without** a left-border bar or a coloured background. The italics come from the source markdown's `*...*`.

- [ ] **Step 4: If anything fails the spot-check, fix the CSS and rebuild**

If a check fails, edit `epub/styles.css` to address it, re-run Task 3 Steps 3–4 to rebuild, and re-verify. Document any deviation from the spec in the commit message in Task 5.

---

## Task 5: Commit and clean up

**Files:**
- Add: `epub/styles.css`
- Modify: `.github/workflows/build-epub.yml`
- Do NOT commit: `RTW.epub`, `Original RTW.epub` (local build artifacts only)

- [ ] **Step 1: Confirm the EPUB build artifacts are not staged**

Run:
```powershell
git status
```
Expected: `epub/styles.css` listed as untracked, `.github/workflows/build-epub.yml` listed as modified. `RTW.epub` and `Original RTW.epub` may show as untracked — they should remain untracked (CI rebuilds them; the rolling release publishes them).

If `RTW.epub` or `Original RTW.epub` are in the index, unstage with `git restore --staged RTW.epub "Original RTW.epub"`.

- [ ] **Step 2: Consider adding `.gitignore` entries for the local artifacts**

Check whether `.gitignore` exists and already ignores them:
```powershell
Test-Path .gitignore
```
If `.gitignore` exists, use Grep to look for `*.epub`. If neither file ignores `.epub`, add them. Use the Edit or Write tool to append:
```
RTW.epub
Original RTW.epub
```
(If `.gitignore` does not exist, create it with just those two lines.)

- [ ] **Step 3: Stage only the intended files**

Run:
```powershell
git add epub/styles.css .github/workflows/build-epub.yml
```
If `.gitignore` was created or modified in Step 2, also: `git add .gitignore`.

- [ ] **Step 4: Commit**

Run:
```powershell
git commit -m @'
Add EPUB stylesheet for modern-clean trade-paperback look

Apply epub/styles.css to both RTW.epub and Original RTW.epub builds.
Centers chapter headings, replaces hr scene-breaks with a three-dot
row, sets indent-not-space paragraphs, ragged-right serif body.

Implements docs/superpowers/specs/2026-05-16-epub-styling-design.md.
'@
```

- [ ] **Step 5: Verify the commit landed cleanly**

Run:
```powershell
git status
git log -1 --stat
```
Expected: working tree clean (aside from the untracked `.epub` artifacts if not gitignored), and the commit shows the two (or three) intended files.

---

## Out of scope (intentionally not in this plan)

These are listed in the spec as deferred — do not implement here:
- Cover image (`--epub-cover-image`).
- Title page, dedication, copyright/colophon.
- Embedded fonts via `--epub-embed-font`.
- Drop caps or small caps.
- Source-file normalization of `***` vs `---`.
- Kindle-specific tuning.
- `epubcheck` validation in CI.
