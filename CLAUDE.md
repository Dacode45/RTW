# RTW — Prose Rewrite Agent Guide

## Project Overview

This project rewrites a translated web novel ("Release That Witch") into polished literary prose. Each chapter becomes an individual Pandoc Markdown file in `book/` (e.g., `book/CH001.md`, `book/CH042.md`, …, `book/CH1498.md`). The source contains rough/translated prose; the output should read like published fiction in the rhythmic-precision register described by the style guide.

**Key constraint:** Only style and grammar are rewritten. Plot, characters, proper nouns, chronology, scene order, and structure are preserved exactly.

## Critical Rewriter Instructions

**You are a prose and grammar improver, not a ruthless editor.**

This is the most important principle. When you rewrite a chapter:

- **Preserve all material.** Do not cut paragraphs of Barov's musings about his career ambitions, Roland's strange orders, or a character's internal reflections just because they seem tangential or verbose. The author included these for a reason—they reveal character, build theme, and deepen reader understanding.

- **Word count is not a deciding factor.** A chapter may be long because the author *intended* it to contain extended thought or exposition. Your job is to improve the prose and fix grammar, not to shrink the chapter into minimalism. Compression should come from tightening sentences, eliminating redundancy, and improving word choice—not from deleting entire passages of character interiority or authorial reflection.

- **Distinguish between ruthless cutting and economical prose.** "Cut every word the sentence can survive without" means: *She smiled at him.* becomes *She smiled.* It does NOT mean: delete the entire paragraph where she realizes she trusts him more than she expected.

- **Respect the author's voice and pace.** Some chapters move quickly. Some linger on a character's thoughts. Some include digressions that deepen theme. These choices are intentional. Your role is to make them *clear and beautiful*, not to *eliminate* them.

- **When in doubt, ask: Does this reveal character or advance theme?** If yes, it belongs. Tighten it, sharpen it, improve its rhythm—but preserve it.

- **Ensure you don't duplicate chapters.** After a rewrite, read the opening of `ch{N+1}_source.md` and the closing of `ch{N-1}_source.md` and confirm that no content from either has been absorbed into this rewrite. Duplication can bleed in either direction — a rewrite may accidentally pull content from the *next* chapter just as easily as from the prior one. 

## Repository Layout

```
RTW/
├── source/                              # Source material (do not modify)
│   ├── chapters/                        # Individual per-chapter source files
│   │   ├── ch0001_source.md             #   ch0001_source.md … ch1498_source.md
│   │   └── ...                          #   (1498 files, zero-padded to 4 digits)
│   ├── CH1-150.md                       # Original bulk files (do not modify)
│   └── ...
├── Style_Guide_and_Grading_Rubric.md    # Master style & grading document
├── CLAUDE.md                            # This file
├── book/                                # Output: one .md per chapter
│   ├── CH001.md
│   ├── CH041.md
│   └── ...                              # Target: CH001–CH1498
├── docs/superpowers/specs/              # Reference docs
└── .github/workflows/build-epub.yml     # CI: builds EPUB from book/*.md
```

## The Three-Agent Pipeline

Each chapter goes through a **write → grade → revise** cycle using three distinct agent roles.

### Agent 1 — Rewriter

- **System prompt:** Part One of `Style_Guide_and_Grading_Rubric.md` (the Rewriter's Checklist).
- **Input:** The corresponding pre-split source file from `source/chapters/ch{NNNN}_source.md` (zero-padded to 4 digits, e.g. `ch0001_source.md`, `ch0042_source.md`, `ch1201_source.md`).
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
- **Input:** The source chapter (from `source/chapters/ch{NNNN}_source.md`), the rewrite (from `book/CHXXX.md`), the source file for the immediately preceding chapter (for continuity checking), and the source file for the immediately following chapter (to detect forward bleed — content from the next chapter absorbed into this rewrite). The preceding chapter source is **not** required for CH001; the following chapter source is **not** required for CH1498.
- **Output:** A structured grade report with:
  1. Scores (1–5) across all eleven dimensions (Fidelity, Compression, Interiority, Imagery, Rhythm, Voice, Dialogue, Atmosphere, Grammar, Restraint, Logical & Continuity Consistency).
  2. Justification + specific quotations for each score.
  3. Improvement suggestions for any score ≤ 4.
  4. Total score (max 55), recommendation (ACCEPT / REVISE-LIGHT / REVISE-HEAVY / REJECT).
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
| **50–55** | ACCEPT — chapter is done. |
| **42–49** | REVISE-LIGHT — one targeted pass on weak dimensions. |
| **31–41** | REVISE-HEAVY — full second pass warranted. |
| **11–30** | REJECT — restart from source. |

If a chapter scores REVISE, it loops back through **Grade → Revise** until it reaches ACCEPT or has completed 3 revision cycles (then flag for human review).

## File Conventions

- **Filename:** `book/CHXXX.md` — zero-padded to at least three digits: CH001, CH042, CH999, CH1000, CH1498. Chapters below 1000 use three digits; chapters 1000+ use four digits naturally.
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
  $(ls book/CH*.md | sort -V)
```

Chapters must sort correctly by filename — hence the zero-padded numbering.

## Current Progress

- **Completed:** CH001, CH041–CH070 (31 chapters)
- **Remaining:** CH002–CH040, CH071–CH1498 (1,467 chapters)
- **Priority:** Work sequentially from the lowest unwritten chapter number.

## Working With the Source Files

Each chapter has its own pre-split source file in `source/chapters/`:

- **Filename pattern:** `source/chapters/ch{NNNN}_source.md` — 4-digit zero-padded number.
- **Examples:** `ch0001_source.md`, `ch0042_source.md`, `ch1201_source.md`, `ch1498_source.md`.
- To rewrite chapter N, read `source/chapters/ch{NNNN}_source.md` directly — no extraction needed.
- Process the full file text — do not truncate or summarize.

## Quality Principles (Quick Reference)

1. **Cut every word the sentence can survive without** — at the sentence level. This means: "She felt tired" → "Exhaustion." NOT: delete the entire paragraph of character reflection.
2. Show interiority through behavior, image, or sensation — never bare reportage.
3. One striking image per scene beat; earn your metaphors.
4. Voice lives in syntax, not vocabulary. Vary sentence length deliberately.
5. Concrete nouns and specific verbs beat adjectives.
6. Dialogue carries subtext — characters say what they can bear to say.
7. **Preserve all source facts and material.** Style is the rewrite's only domain. Do not cut content; improve it.
8. Read each paragraph aloud in your head for rhythm.
