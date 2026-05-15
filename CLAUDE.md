# RTW — Prose Rewrite Agent Guide

## Project Overview

This project rewrites (pdfs and markdown files in "source" directory) (a translated web novel, "Release That Witch") into polished literary prose. Each chapter becomes an individual Pandoc Markdown file in `book/` (e.g., `book/CH001.md`, `book/CH042.md`, …, `book/CH150.md`). The source contains rough/translated prose; the output should read like published fiction in the rhythmic-precision register described by the style guide.

**Key constraint:** Only style and grammar are rewritten. Plot, characters, proper nouns, chronology, scene order, and structure are preserved exactly.

## Critical Rewriter Instructions

**You are a prose and grammar improver, not a ruthless editor.**

This is the most important principle. When you rewrite a chapter:

- **Preserve all material.** Do not cut paragraphs of Barov's musings about his career ambitions, Roland's strange orders, or a character's internal reflections just because they seem tangential or verbose. The author included these for a reason—they reveal character, build theme, and deepen reader understanding.

- **Word count is not a deciding factor.** A chapter may be long because the author *intended* it to contain extended thought or exposition. Your job is to improve the prose and fix grammar, not to shrink the chapter into minimalism. Compression should come from tightening sentences, eliminating redundancy, and improving word choice—not from deleting entire passages of character interiority or authorial reflection.

- **Distinguish between ruthless cutting and economical prose.** "Cut every word the sentence can survive without" means: *She smiled at him.* becomes *She smiled.* It does NOT mean: delete the entire paragraph where she realizes she trusts him more than she expected.

- **Respect the author's voice and pace.** Some chapters move quickly. Some linger on a character's thoughts. Some include digressions that deepen theme. These choices are intentional. Your role is to make them *clear and beautiful*, not to *eliminate* them.

- **When in doubt, ask: Does this reveal character or advance theme?** If yes, it belongs. Tighten it, sharpen it, improve its rhythm—but preserve it.

- **Ensure you don't duplicate chapters** After a rewrite, compare with the prior chapter and make sure you didn't include the same content twice. 

## Repository Layout

```
RTW/
├── source/                         # Source material (do not modify)
├── Style_Guide_and_Grading_Rubric.md    # Master style & grading document
├── agent.md                             # This file
├── book/                                # Output: one .md per chapter
│   ├── CH001.md
│   ├── CH041.md
│   └── ...                              # Target: CH001–CH150
├── docs/superpowers/specs/              # Reference docs
└── .github/workflows/build-epub.yml     # CI: builds EPUB from book/*.md
```

## The Three-Agent Pipeline

Each chapter goes through a **write → grade → revise** cycle using three distinct agent roles.

### Agent 1 — Rewriter

- **System prompt:** Part One of `Style_Guide_and_Grading_Rubric.md` (the Rewriter's Checklist).
- **Input:** The corresponding chapter from source directory. Mardown and pdf files.  (source prose).
- **Output:** A rewritten chapter saved as `book/CHXXX.md`.
- **Rules:**
  - Follow the eight essential rules and the extensive catalogue.
  - Preserve all proper nouns, plot facts, chronology, and structure.
  - **Preserve all material:** musings, reflections, character interiority, digressions that reveal theme. Do not delete content; improve its prose.
  - Use Pandoc-flavored Markdown: `# Chapter N: Title` as the heading, standard paragraph breaks, blockquotes for in-world documents, `*italics*` for emphasis/stress.
  - Do not invent plot or characterization beyond what the source implies.
  - **Compression rule:** Cut words and redundant phrases within sentences, not entire passages of thought. "She felt tired" → "Exhaustion" is compression. Deleting a paragraph where a character realizes something important is deletion, not compression.

### Agent 2 — Grader

- **System prompt:** Part Two of `Style_Guide_and_Grading_Rubric.md` (the Grading Rubric). The grader does **not** see Part One.
- **Input:** The source chapter (from the md) and the rewrite (from `book/CHXXX.md`).
- **Output:** A structured grade report with:
  1. Scores (1–5) across all ten dimensions (Fidelity, Compression, Interiority, Imagery, Rhythm, Voice, Dialogue, Atmosphere, Grammar, Restraint).
  2. Justification + specific quotations for each score.
  3. Improvement suggestions for any score ≤ 4.
  4. Total score (max 50), recommendation (ACCEPT / REVISE-LIGHT / REVISE-HEAVY / REJECT).
  5. Closing paragraph: greatest strength, greatest weakness, one-sentence revision directive.

### Agent 3 — Reviser

- **System prompt:** Part One of `Style_Guide_and_Grading_Rubric.md` plus the grader's report.
- **Input:** The current rewrite (`book/CHXXX.md`) and the grader's feedback.
- **Output:** A revised chapter that overwrites `book/CHXXX.md`.
- **Rules:**
  - Address every specific criticism from the grader's report.
  - Do not regress on dimensions that already scored well.
  - Focus revision effort on the weakest-scoring dimensions.

### Acceptance Criteria

| Total Score | Action |
|---|---|
| **45–50** | ACCEPT — chapter is done. |
| **38–44** | REVISE-LIGHT — one targeted pass on weak dimensions. |
| **28–37** | REVISE-HEAVY — full second pass warranted. |
| **10–27** | REJECT — restart from source. |

If a chapter scores REVISE, it loops back through **Grade → Revise** until it reaches ACCEPT or has completed 3 revision cycles (then flag for human review).

## File Conventions

- **Filename:** `book/CHXXX.md` — zero-padded to three digits (CH001, CH042, CH150).
- **Heading:** `# Chapter N: Title` — preserving the source chapter's title.
- **Scene breaks:** Use `***` (three asterisks) on their own line.
- **In-world documents:** Blockquote format (`>`).
- **Emphasis/stress:** `*italics*` — never for decoration, only for vocal stress or internal thought.
- **Encoding:** UTF-8, LF line endings.
- **No YAML front matter** — the EPUB build uses CLI metadata.

## Build Pipeline

The GitHub Actions workflow (`.github/workflows/build-epub.yml`) builds an EPUB on push to `main`:

```bash
pandoc -o RTW.epub --toc --toc-depth=1 \
  --metadata title="RTW" \
  --metadata author="Dacode45" \
  --metadata lang=en-US \
  $(ls book/CH*.md | sort)
```

Chapters must sort correctly by filename — hence the zero-padded numbering.

## Current Progress

- **Completed:** CH001, CH041–CH070 (31 chapters)
- **Remaining:** CH002–CH040, CH071–CH150 (119 chapters)
- **Priority:** Work sequentially from the lowest unwritten chapter number.

## Working With the Source md

source files are large mds and pdfs. When processing:
1. Extract one chapter at a time from the file.
2. Identify chapter boundaries by headings/titles in the source.
3. Process the full chapter text — do not truncate or summarize.

## Quality Principles (Quick Reference)

1. **Cut every word the sentence can survive without** — at the sentence level. This means: "She felt tired" → "Exhaustion." NOT: delete the entire paragraph of character reflection.
2. Show interiority through behavior, image, or sensation — never bare reportage.
3. One striking image per scene beat; earn your metaphors.
4. Voice lives in syntax, not vocabulary. Vary sentence length deliberately.
5. Concrete nouns and specific verbs beat adjectives.
6. Dialogue carries subtext — characters say what they can bear to say.
7. **Preserve all source facts and material.** Style is the rewrite's only domain. Do not cut content; improve it.
8. Read each paragraph aloud in your head for rhythm.
