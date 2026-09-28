# IN6227 Assignment 1 — Variant 2 (v2.7.1)

Reusable Skill for end-to-end tabular classification and automated report generation.

## Design priorities

- The assignment grades **depth and clarity of reasoning at each workflow step**, not algorithm complexity or accuracy alone.
- v2.7.1 uses a baseline-first, evidence-driven model escalation process: start with the simplest defensible model, treat its result as evidence about the problem, and add complexity only when justified.
- Baseline selection and escalation decisions require explicit dataset-specific reasoning. Logistic Regression is a candidate, not a preset; explain why observed data and representation support the chosen baseline and why a relevant alternative was not selected. Cite sources for externally supported implementation claims.
- Default conversational flow uses **one user-facing checkpoint after data understanding**, then a continuous batch through model selection, tuning, evaluation, and report generation.
- Phase-by-phase interaction is not required unless the user asks for it.
- The reflection is a separate human-authored assignment component. The skill must not draft or insert it into the generated report.
- Candidate selection remains adaptive rather than a fixed whitelist.
- There is no default three-finalist requirement; models are introduced sequentially only when the baseline or data justify them.
- More complex models must show a meaningful empirical improvement or a clearly documented required capability before being retained.
- Tuning uses bounded randomized search, safe parallelism, early stopping where supported, and an adaptive compute budget.
- Test-set isolation is enforced for modelling decisions.
- Close results are interpreted cautiously rather than treating tiny metric differences as decisive.
- The report preserves the supplied template's **single-column layout**; multi-column rendering is prohibited.
- The supplied Word template remains the visual authority; the PDF QA explicitly checks overlap, clipping, column spill, and long-token wrapping problems.

## Token-efficiency principle

**Reason once, reuse the evidence.** For consequential decisions, maintain:

`Observation → Implication → Baseline/Decision → Why → Evaluation → Escalation/Stopping Rule → Alternative → Why not`

Keep the record compact and elaborate it once in the final report. Do not generate duplicate prose or separate reproducibility artifacts.

## Submission output

- One PDF: `IN6227_assignment1_variant2_report.pdf`, no more than two pages.
- Include the actual LLM model name/version and interface/version in the PDF. The reflection is written separately by the human user.

## Version

2.7.1
