# Report Guidelines and Quality Gates

## Template fidelity

Before drafting, read `assets/IN6227-Reports-Template.doc`. If the runtime cannot parse `.doc`, use `assets/report_template_spec.md`.

Preserve the template's main heading structure and visual hierarchy. The supplied template uses a **single-column page layout**. Do not invent a two-column or multi-column paper format.

## Report structure

Use these main headings exactly as presented in the template:

- `INTRODUCTION`
- `METHODS OR PROCEDURES`
- `RESULTS`
- `DISCUSSION`
- `CONCLUSION`
- `REFERENCES`

Under `METHODS OR PROCEDURES`, use numbered workflow sub-steps:

1. Data exploration and cleaning
2. Preprocessing
3. Feature selection/engineering, if applicable
4. Train/validation/test protocol
5. Candidate model selection
6. Hyperparameter tuning
7. Evaluation metrics

Do not replace the template's main headings with numbered headings. Keep numbering inside Methods.

## Methods content

State the actual dataset dimensions, target, data-quality treatment, preprocessing, split protocol, model-selection rationale, tuning approach, and evaluation metrics. **For every consequential choice, connect evidence to the decision.** Model selection must follow a baseline-first narrative rather than a predeclared multi-model shortlist. The Methods section should read as a chain of reasoning, not a list of procedures:

**Observed evidence → implication → chosen action → why that action fits → relevant alternative and why it was not used.**

At minimum this applies to: missing-value handling, encoding/scaling, feature retention or exclusion, train/validation/test protocol, **baseline-model choice**, **why the observed data and representation make that baseline suitable**, **why a relevant alternative was not selected**, **what the baseline result revealed about the problem**, **why any additional model class was tested**, **why added complexity was retained or rejected**, tuning budget/ranges, and metric selection. When a choice is routine but still consequential, a short dataset-specific justification is enough. Do not use generic textbook statements such as “LR is simple and interpretable” or “LR is the standard baseline” as substitutes for observed evidence.

A strong compact sentence is: “Because X was observed, Y was used so that Z; A was not used because B.”

State whether cross-validation served as the validation mechanism when there was no separate validation file.

When an explicit test file exists, distinguish **structural compatibility checks before model selection** from the final held-out evaluation. Do not write that the test set was literally “untouched” if it was loaded earlier for structural validation.

When the same CV process informed model screening and hyperparameter tuning, describe the CV results as **model-selection estimates** and include a limitation stating that they are not fully unbiased generalisation estimates. Held-out test results are the principal final comparison.

## Results content

Use a compact model comparison table containing:
- model name;
- mean CV primary metric (and variability when useful);
- final test primary metric;
- macro-F1 when relevant;
- optionally ROC-AUC/PR-AUC when informative.

Also report the **best hyperparameters** for each model that was actually retained or materially discussed in the final comparison, in a compact, wrap-safe form. Do not list untested “finalists.” Prefer short parameter tables over long inline code strings in narrow columns.

When relevant, include per-class precision, recall, and F1 so that class-level claims in the Discussion can be traced to reported values.

Include a confusion matrix or another small diagnostic plot only when it adds useful evidence and fits the template/page constraint.

## Discussion

Explain meaningful differences and trade-offs using observed evidence. Do not merely restate the Results table. Interpret what the observed differences imply for model choice, class errors, complexity, interpretability, and uncertainty where evidence exists. Avoid declaring a model superior on one metric alone when results are mixed. Do not make unsupported threshold-optimization, calibration, cost, latency, or memory claims.

When a model is selected, explicitly state the selection criterion and the evidence supporting it. Start by explaining why the baseline was the simplest defensible starting point. Then state what its performance revealed, why escalation was or was not warranted, and whether the added model delivered a meaningful improvement relative to its added complexity. A point estimate alone is not enough when competing models are practically tied. When the evidence supports multiple defensible choices, say so and explain the non-accuracy trade-offs rather than forcing a single “winner.”

If top results are very close, do not call the difference decisive from point estimates alone. Prefer CV variability and, when materially needed and feasible, a paired uncertainty analysis. Otherwise explicitly state the uncertainty limitation.

## Research citations and APA references

Use 0, 1, 2, or more scholarly/authoritative references as genuinely needed. Cite a source when it materially supports a methodological or implementation claim—especially the baseline-model rationale, cross-validation/model-selection limitations, or model-specific assumptions. Prefer original/seminal research or authoritative technical documentation. Do not add citations merely to decorate the report, and do not fabricate bibliographic details.

Use APA 7th edition for in-text citations and the References section. Do not fabricate bibliographic details. Every in-text citation must have a matching reference, and every reference must be cited.

## Metadata

Include:
- **LLM model name & version**: the actual language model running the workflow (not the classifier), from runtime metadata;
- **LLM interface & version**: actual interface such as an API, ChatUI, or agent harness, with version if exposed;
- **Skill version**: `2.7.1`;
- GitHub repository link/placeholder as required by the assignment.

Never guess runtime metadata. Use `Unavailable in this runtime` if it cannot be determined. The generated report deliverable is one PDF of no more than two pages; do not require a Markdown companion. The assignment's reflection is written separately by the human user. Do not draft, infer, or insert reflection text in the report; after delivering the PDF, remind the user to complete that human-authored component.

## Two-page and rendering quality gate

The two-page limit is a rendered-PDF requirement.

After rendering:
1. run `scripts/check_report.py` when available;
2. count actual PDF pages;
3. inspect each rendered page visually;
4. confirm all required main sections remain present;
5. check for overlapping text, clipped text, text escaping margins/columns, broken headings, unreadable parameter strings, and table overflow;
6. confirm numbered Methods steps are visible and in order;
7. if any defect appears, reflow the content and re-render;
8. do not reduce font size or line spacing below the template requirements merely to meet the limit.

### Layout and common wrap hazards

The report body must remain a single continuous column. Avoid or reformat:
- long `parameter=value` chains;
- long file paths/URLs in the body;
- long unbroken code expressions;
- manual hard line breaks inside paragraphs;
- floating text boxes or side-by-side prose regions for ordinary prose;
- CSS/newspaper multi-column layout or manually positioned second-column text;
- tables whose cells contain very long unbroken strings.

Use compact tables, natural spaces, or short prose descriptions instead.

## Reproducibility and uncertainty

Keep exact runtime/settings in internal run state. The two-page report should include only the compact settings needed to understand and reproduce the reasoning: data protocol, preprocessing structure, CV strategy, search strategy, finalist models, and winning hyperparameters. **Do not spend report space listing settings that do not support a decision.** Use the saved settings to explain why the search/tuning design was appropriate and computationally bounded. Do not create a separate reproducibility file unless explicitly requested.
