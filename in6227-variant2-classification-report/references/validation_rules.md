# Validation Rules

## Contents
- Runtime input handling
- File discovery
- File-level validation
- Split-role validation
- Target validation
- Categorical consistency
- Blocking errors and recovery
- Train/validation/test protocol

## Runtime input handling

For Claude Web/chat, use native attachments or Project Files. Do not request a local path unless filesystem access is explicitly available. For filesystem-enabled runtimes, use the supplied folder/file as the task boundary.

Do not rename files merely to satisfy the Skill.

## File discovery

Supported formats depend on the runtime, commonly CSV, TSV, XLSX, XLS, and Parquet. Ignore hidden files, temporary lock files, generated reports, logs, notebooks, and the Skill's own artifact/output directories.

Record the candidate file list.

If one valid dataset is supplied, use **Single Dataset**. If two compatible files strongly support a train/test interpretation, use **Train + Test**. If three compatible files strongly support train/validation/test, use **Train + Validation + Test**. If roles remain ambiguous or unrelated files are mixed together, ask the user instead of guessing.

Filename hints such as `train.csv`, `test.csv`, `holdout.csv`, or `train(1).csv` are evidence only.

## File-level validation

Check:
- file exists and is readable;
- supported tabular format;
- non-empty table;
- headers present and unique;
- plausible row/column counts;
- delimiter/encoding parsing did not collapse the table unexpectedly;
- warnings are surfaced;
- rows/columns were not silently lost during parsing.

## Split-role validation

For candidate related files, perform **structural validation before model selection** using only information necessary to determine whether the files can form the claimed partitions:
- feature names and order;
- dtypes / parseability;
- target-column presence;
- row counts and basic file integrity.

Do **not** use held-out test values for model choice, preprocessing design, hyperparameter tuning, threshold selection, or exploratory comparisons. In particular, do not use pre-selection test class distributions, test category coverage, or test feature distributions to justify a model.

Checks that require inspecting test values beyond necessary structural compatibility (for example exact row-overlap checks, category coverage, or test distribution summaries) should be treated as optional data-quality diagnostics and must not influence model-selection decisions. Prefer to defer such diagnostics until after model selection, or omit them when they are not needed for validity.

The report should avoid claiming that the test set was literally never inspected. Use precise wording such as:

> “The held-out test file was inspected before model selection only for necessary structural compatibility checks. No test-set values were used for fitting preprocessing, feature selection, model selection, hyperparameter tuning, threshold selection, or repeated experimentation. Final model performance was computed on the test set only after all modelling choices were frozen.”

Before modelling, show:

```text
INPUT DECISION
Files received: ...
Interpreted as: Train + Test
Training file: ...
Test file: ...
Target: ...
Validation mechanism: 5-fold cross-validation on training data
Final test set: ...
Evidence: ...
Warnings: ...
```

In batch mode, do not wait for confirmation when the evidence is sufficient; show the inferred roles in the plan summary and continue. If evidence conflicts or is insufficient, stop and ask the user to identify the roles. In explicit interactive mode, pause for confirmation.

## Target validation

If the user supplied a target column, verify that it exists and has at least two non-missing classes. If the target is missing, look for common target-like names only as a weak heuristic. If multiple plausible targets exist, ask the user.

Never impute target labels.

For missing targets:
- training/development: exclude unlabeled rows from fitting and report the count;
- validation/test: exclude unlabeled rows from supervised metric calculation and report the evaluable count;
- if missingness is material (default warning threshold 5%) or appears systematic, ask whether a corrected dataset should be supplied.

Do not describe test rows as “dropped” merely because they are unlabeled; say they were excluded from supervised metric calculation.

## Categorical consistency

Inspect categorical values for whitespace, case, punctuation, abbreviations, Unicode/encoding variants, and likely near-duplicates. Quantify suspicious values. Do not silently merge or normalize them. Report material inconsistencies at the data-understanding checkpoint and use the safest documented handling. Pause for clarification only when the inconsistency makes data interpretation or evaluation invalid; do not add a routine checkpoint.

Be stricter with target labels: never silently collapse distinct labels.

## Blocking errors and recovery

Stop before modelling when:
- a required file is unreadable;
- training has no valid target or only one class;
- train/test feature schemas are materially incompatible;
- explicit validation/test roles cannot be reconciled;
- multiple candidate files remain ambiguous;
- a required evaluation target is absent when supervised test metrics are expected.

For every blocking error, state the exact problem, affected file/column, why it matters, and the smallest corrective action. On folder-based runtimes, prefer asking the user to replace the affected file rather than re-provide the entire folder.

Do not request re-upload for safely handled conditions such as ordinary missing feature values or unseen categorical values that can be handled by the pipeline.

## Train/validation/test protocol

### Single Dataset
Create a reproducible stratified train/test split when feasible. Use cross-validation only inside the training portion for model selection. Treat the resulting test portion as held out from modelling decisions until final evaluation.

### Train + Test
Use stratified CV on the training file for model selection. Do not use the explicit test set for preprocessing fitting, feature selection, model selection, threshold tuning, or repeated experimentation. Evaluate final frozen models on the held-out test set once after all choices are frozen.

### Train + Validation + Test
Fit preprocessing/models on training data. Use validation for configuration/model decisions. Keep test held out from modelling decisions until final evaluation. If CV is used, confine it to training data.

Record the exact data used for model selection and final evaluation in the report.
