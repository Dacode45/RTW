# EPUB release workflow — design

**Date:** 2026-05-12
**Status:** Approved (pending spec review)

## Goal

Every push to `main` builds an EPUB from the repo's chapter markdown files using pandoc, and publishes it as the single rolling `latest` GitHub release so a stable download URL always points at the newest build.

## Inputs

- Chapter files at the repo root matching `CH*.md` (currently `CH001.md` and `CH041.md`–`CH070.md`). The gap from chapters 2–40 is expected; pandoc concatenates whatever files match in sorted order.
- Each chapter file begins with a `# Chapter N: …` heading, which pandoc uses to build the table of contents.

## Output

- A single GitHub release tagged `latest`, with `RTW.epub` attached. The release is recreated/updated in place on each push, so the asset URL `releases/download/latest/RTW.epub` stays stable.

## Workflow

**File:** `.github/workflows/build-epub.yml`

**Triggers:**
- `push` to `main`
- `workflow_dispatch` (manual override)

**Permissions:** `contents: write` (required to create/update the release and move the `latest` tag).

**Job (`ubuntu-latest`):**

1. **Checkout** — `actions/checkout@v4`.
2. **Install pandoc (cached)** — `awalsh128/cache-apt-pkgs-action@v1` with `packages: pandoc`. Caches the apt package so subsequent runs skip the ~30 MB download.
3. **Build EPUB:**
   ```bash
   pandoc -o RTW.epub --toc --toc-depth=1 \
     --metadata title="RTW" \
     --metadata author="Dacode45" \
     --metadata lang=en-US \
     $(ls CH*.md | sort)
   ```
4. **Publish rolling release** — `softprops/action-gh-release@v2`:
   - `tag_name: latest`
   - `name: "RTW (latest build)"`
   - `files: RTW.epub`
   - `make_latest: true`

## Design choices

- **Pandoc via `cache-apt-pkgs-action`** rather than plain `apt-get install` — caches the apt package between runs so pandoc isn't redownloaded every push. The Ubuntu pandoc package is current enough for EPUB output.
- **Glob + sort** rather than an explicit file list — keeps the workflow stable as new chapters are added. The lexicographic sort works because filenames are zero-padded (`CH001`, `CH041`, …).
- **Rolling `latest` release** rather than per-push tags — matches user choice; gives a stable download URL for an in-progress work.
- **TOC depth 1** — each `# Chapter N:` heading becomes a top-level TOC entry. Sub-headings inside chapters (if any) won't clutter the TOC.

## Out of scope

- Cover image
- Custom EPUB stylesheet
- PDF output
- Filling the chapter 2–40 gap
- Validation of EPUB output (e.g. `epubcheck`)
