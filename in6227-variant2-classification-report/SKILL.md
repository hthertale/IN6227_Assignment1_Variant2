---
name: in6227-assignment1-variant2-classification-report
description: Build an evidence-based classifier for a user-supplied tabular dataset and generate a reasoned report PDF of up to two pages.
---

# IN6227 Variant 2 — Classification Skill v2.7.1

## Purpose

Run a dataset-agnostic tabular classification workflow and generate one submission deliverable: `IN6227_assignment1_variant2_report.pdf`, no more than two pages.

The user may provide a dataset path directly. Use that path as the input boundary; do not substitute unrelated files from its parent folder. If only a folder is supplied, discover eligible dataset files within it using `validation_rules.md`. If local filesystem access is unavailable, use the provided attachment or ask for an accessible path/file.

The assignment grades the **depth and clarity of reasoning at each workflow step**. Preserve decision evidence and justification; save tokens by avoiding duplicate narration and unnecessary artifacts, not by shortening the reasoning needed to justify decisions.

## Core rules

1. Never assume schema, target, split roles, preprocessing, or best model.
2. Never use final test values for fitting, feature selection, model selection, tuning, threshold tuning, or repeated experimentation.
3. In interactive use, **split the workflow at one user-visible checkpoint after data understanding**: the first substantive response must show only the observed data understanding, implications, and proposed modelling direction; then wait for the user's correction/confirmation before running the remaining workflow. Do not start candidate screening, tuning, or report drafting before that checkpoint is acknowledged.
4. Do not pause at every phase. After the single checkpoint, continue the remaining workflow in one batch unless a blocking issue occurs. If the user explicitly requests full batch execution, skip the checkpoint and continue after the initial validation/understanding pass.
5. Guided explanations should be concise and decision-focused. Explain unfamiliar terms only when they affect a consequential decision.
6. Select the baseline from the observed data and chosen representation. Logistic Regression is a common candidate for encoded tabular data, not an automatic choice: state which observed data/representation properties make the selected baseline suitable and why it is a simpler defensible starting point than relevant alternatives. Do not tune or run several complex models by default.
7. Treat baseline performance as evidence about the problem: use its errors, class-wise metrics, and validation variability to decide whether the data justify a more complex model class.
8. Introduce additional model classes **sequentially**, only when the dataset characteristics or baseline results create a documented reason to test them. Retain added complexity only when its empirical improvement is meaningful enough to justify the added complexity, compute, or reduced interpretability.
9. Do not fabricate results, metadata, citations, user actions, or oversight.
10. Do not create Markdown reports, reflection text/files, compliance/runtime logs, model logs, or separate reproducibility artifacts. The reflection component is authored by the human user; do not draft, infer, or insert it into the report. After presenting the report PDF, remind the user to prepare their own reflection for the assignment.
11. Use bundled references and the supplied report template as authoritative resources.
12. When a methodological claim or baseline rationale is supported by external literature or official documentation, cite it in APA 7th style; never invent citations.
13. The final report must follow the template and pass the two-page quality and rendering gate.

## Reasoning contract

The assignment grades **reasoning depth and clarity**, so the final report must show not only what was done but **why the decision followed from the evidence**. A compact internal record is still required for every consequential decision:

**Observation → Implication → Baseline/Decision → Why → Evidence from evaluation → Escalation or stopping decision → Alternative → Why not**

Use only evidence from the observed data, diagnostics, validation results, runtime constraints, or explicit user requirements. Do not invent rationale after the fact.

### Reasoning minimum for each workflow step

For each Methods step that contains a substantive decision, the report must answer at least one explicit **why** question. In compact prose, connect the observed evidence to the decision using forms such as:
- “Because …, we therefore …”
- “The data showed …, so … was used rather than …”
- “This was chosen because …; the main alternative was …, but …”

Do **not** write a procedure-only sentence such as “median imputation was used” when the choice is consequential. It must be followed by the dataset-specific reason. Do not replace reasoning with generic textbook claims.

At minimum, preserve reasoning for: cleaning decisions, preprocessing choices, feature retention/removal, validation/test protocol, **baseline-model selection**, **whether the baseline justified escalation**, **which additional model class was tested and why**, **whether the added complexity was retained or rejected**, tuning budget/ranges, and metric selection.

When no change was made, explain why the evidence did **not** justify one.

The final report should elaborate the important decision records **once**. Do not regenerate the same rationale as separate logs or educational artifacts; include the brief reflective limitation and improvement in Discussion or Conclusion.

## Progressive disclosure

Read each reference at most once when needed:
- validation → `references/validation_rules.md`
- model selection/tuning/compute → `references/candidate_models.md`
- report → `references/report_guidelines.md`
- original report template → `assets/IN6227-Reports-Template.doc`
- fallback template specification → `assets/report_template_spec.md`

Do not repeatedly quote or re-read references.

## Workflow

### 0. Input validation
Read `validation_rules.md`. Resolve the user-supplied dataset path (or folder/attachment), validate readability/schema, and identify file roles only when evidence is sufficient. Stop only for blocking ambiguity/errors.

### 1. Data understanding
Profile target, feature types, missingness, duplicates, class distribution, identifiers/leakage candidates, and categorical inconsistencies. Record only findings that can affect later decisions.

### 1A. Data-understanding checkpoint
In the default conversational mode, show a compact checkpoint containing:
- dataset/split interpretation;
- target and class balance;
- important data-quality findings;
- feature-type observations relevant to preprocessing/model choice;
- leakage/test-isolation considerations;
- the main modelling implications and the proposed primary metric;
- one or two assumptions the user can correct.

Then pause for the user's confirmation/correction. Do not produce a separate long plan before or after this checkpoint.

### 2. Data protocol
Choose the appropriate single-dataset or explicit split protocol. Keep final test data isolated from modelling decisions.

### 3. Candidate models
Read `candidate_models.md`. Choose and evaluate one simplest defensible baseline first. Use the baseline result as diagnostic evidence. Escalate to at most one additional model class at a time, and only when a data- or result-driven reason exists. Stop when added complexity does not produce a meaningful improvement or lacks a defensible justification. Record selected, tested, rejected, and not-considered candidates using the reasoning contract.

### 4. Tuning
Tune the baseline lightly enough to establish a fair reference, then allocate additional search budget only to model classes that survive the evidence-based escalation gate. Use bounded randomized search, safe parallelism, and early stopping where supported. Adjust compute to dataset size; do not spend equal tuning effort on candidates that the baseline evidence has already made unnecessary.

### 5. Final evaluation
Freeze modelling choices, refit on development/training data, and evaluate the final frozen model(s) on the isolated test set once. Report CV/model-selection estimates and final test results, with per-class metrics when useful.

### 6. Sanity checks
Verify target exclusion, pipeline ordering, test isolation, predicted-label compatibility, and model-specific assumptions such as HGB categorical handling. Keep exact settings in compact internal run state rather than a separate artifact.

### 7. Report
Read `report_guidelines.md` and the bundled template once. Generate the report only from observed outputs and recorded decisions. Before finalizing, run the **reasoning completeness gate** below and then deterministic + visual PDF QA.

### Reasoning completeness gate

Before accepting the report, inspect Methods steps 1–7 and verify that each consequential step contains: **evidence + implication + decision + rationale**. For model selection specifically, verify that the report states **why the baseline was the starting point, what its result revealed, why escalation was or was not warranted, what more complex model class was tested (if any), and why the final complexity level was retained or rejected**. Also verify that at least the major rejected/not-selected alternative decisions have a reason when the evidence permits one. If a step only lists actions, revise it before rendering.

The report is allowed to be concise, but it is not allowed to be a procedure log. Prefer removing repetitive dataset description, hyperparameter inventory, and generic definitions before removing decision rationale.

## Communication after the checkpoint

The initial checkpoint is intentionally user-visible and should be a standalone response. Keep it compact but substantive: data facts first, then the modelling implications those facts create. Do not repeat the same data-understanding prose later except where needed in the final report.

After the single data-understanding checkpoint, do not narrate every tool call, tuning iteration, or parameter. Provide one concise final **Findings + Decisions** summary before presenting the PDF. If the user asks “why?”, expand the relevant decision using **Decision → Evidence → Why → Alternative → Why not**.

## Output-token discipline

Do not paste raw console output, full fold logs, full parameter grids, repeated definitions, or duplicate workflow explanations. **Token saving must come from removing repetition and low-value detail, not from deleting reasoning.** Keep intermediate evidence compact, but preserve enough dataset-specific evidence to support every major decision in the final report. When space is tight, shorten the “what” and retain the “why”.

## PDF rendering discipline

The supplied Word template must remain the visual authority. **The supplied report template is single-column; the generated report must remain single-column. Never introduce a newspaper-style/two-column layout, CSS multi-column flow, side-by-side prose columns, or floating text regions.** The PDF must not contain overlapping text, clipped text, column spill, broken tables, or unreadable code/parameter strings.

When generating report content:
- prefer normal prose with natural wrapping over long unbroken tokens;
- avoid long inline monospace/code strings in narrow columns;
- put long hyperparameter configurations into compact tables or break them at safe delimiters;
- use spaces after commas and around operators where wording permits;
- do not use manual line breaks inside body paragraphs merely to force column layout;
- do not use text boxes, floating callouts, or positioned text for ordinary report content;
- keep tables inside page margins and make every cell wrap safely;
- keep normal prose in one continuous left-to-right text flow;
- do not emulate the visual layout by splitting methods/results into side-by-side columns;
- after rendering, inspect both page images and extracted text for overlap/clipping before finalizing.

If rendering QA finds a layout defect, **reflow the content** (shorten/rephrase, move long settings into a table, or remove nonessential redundancy) and re-render. Do not solve an overflow by silently reducing the template's font size or line spacing below its requirements.

## Final deliverable

Present only `IN6227_assignment1_variant2_report.pdf`, with no more than two rendered pages. PDF rendering and visual inspection are required for a submission-ready report. If rendering is unavailable, clearly state that the required PDF deliverable could not be produced; do not present Markdown as an equivalent final submission.

## Version

`2.7.1`
