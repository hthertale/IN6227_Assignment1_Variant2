# Candidate Models, Tuning, and Compute Policy

## Candidate-selection principles

Use a **baseline-first, evidence-driven escalation** process. The purpose is not to compare a large menu of algorithms; it is to learn what the dataset requires and add complexity only when the evidence supports doing so.

Start with the simplest model that is both technically compatible with the observed representation and capable of answering the classification task. **Logistic Regression is a common candidate, not an automatic default.** Choose it only when evidence from the current dataset supports it—for example, one-hot/dense numeric representation is workable, a linear decision boundary is a reasonable starting hypothesis, and a coefficient-based baseline is useful for interpretability. State the actual observed properties that support the choice; generic claims that LR is simple, common, or interpretable are not sufficient by themselves. Its regularization, dense/sparse input support, and coefficients are implementation characteristics documented by scikit-learn, not evidence that it suits every dataset or will perform best. Cite official documentation for such implementation claims when used in the report.

If Logistic Regression is not defensible for the observed representation or task, choose the next-simplest compatible baseline (for example, a Decision Tree for low-dimensional nonlinear structure or a Naive Bayes variant for sparse/count-like features) and explicitly document the reason.

Useful implementation source: scikit-learn, `LogisticRegression` documentation: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

## Baseline-first protocol

### Step 1 — Establish the baseline

Fit one baseline model before running more complex model classes. Use the same development/validation protocol and primary metric that will be used for later comparisons. Keep the baseline pipeline fully leakage-safe.

Record:
- the observed dataset and representation properties that support this baseline, and why those properties make it a technically defensible first model;
- the most relevant simpler or alternative baseline considered and why it was not chosen;
- the baseline mean CV primary metric and variability;
- macro-F1 and per-class metrics when relevant;
- the dominant error pattern (for example, a confusion between specific classes);
- any evidence that linear decision boundaries are likely insufficient (for example, systematic class overlap, interaction-heavy features, or large residual/error structure that the linear model cannot capture).

### Step 2 — Interpret the baseline as evidence

Do not treat the baseline score as a leaderboard entry only. Ask what the result says about the problem:

- **Baseline already strong and stable:** stop unless there is a clear domain or methodological reason to test extra complexity. A simple model can be the final model when added complexity is unlikely to change the conclusion materially.
- **Baseline adequate but with plausible nonlinear structure:** test one nonlinear model class next, such as a Decision Tree or tree ensemble, depending on scale and data shape.
- **Baseline weak in a sparse/high-dimensional representation:** consider a sparse-aware linear alternative such as LinearSVC or a suitable Naive Bayes model before using heavier tree ensembles.
- **Baseline weak with categorical interactions or nonlinear effects that are plausible from the data:** consider a tree-based model or another model class that can represent interactions, but test only one next step at a time.

The rationale must be dataset-specific. Do not write “Random Forest was selected because it is more powerful” without evidence showing why additional nonlinear capacity is relevant.

## Sequential escalation rule

Add **one new model class at a time**. After each added class, compare it against the current retained model using the same folds, preprocessing logic, primary metric, and evaluation protocol. The test set remains reserved for the final frozen comparison.

For each escalation, record:
1. **Reason to test:** the specific data characteristic or baseline failure that motivates the model class.
2. **Hypothesis:** what capability the new class adds (for example, nonlinear splits or interactions).
3. **Evidence:** CV mean, variability, and relevant class-level metrics.
4. **Complexity cost:** extra hyperparameters, computation, or reduced interpretability. State only costs that are documented or measured.
5. **Retention decision:** keep the added model only when the observed improvement is meaningful enough to justify those costs.

### What counts as meaningful improvement

Do not use a universal numerical threshold for “meaningful improvement.” Define meaningful improvement from the task, primary metric, assignment requirements, class distribution, or documented application constraints **before using the held-out test set**. Report both the magnitude of the improvement and the fold-to-fold variability. When no defensible task-specific threshold exists, do not invent one: describe the practical difference qualitatively and explain whether the observed gain is clearly distinguishable from ordinary validation variability.

A model with a small numerical improvement may still be retained when the report provides a concrete, non-performance reason (for example, a required capability or materially better class coverage) and clearly labels that reason. Conversely, a numerically larger gain should not automatically justify retention if it is unstable, depends on extensive tuning, or does not justify the added complexity or reduced interpretability.

## Stopping rule

Stop escalating when any of the following applies:
- the baseline is already adequate and no data-driven weakness justifies more complexity;
- the next model class fails to achieve a meaningful improvement;
- the improvement is too uncertain to distinguish from validation variability;
- the added model introduces complexity or compute cost that is not justified by the observed gain;
- the available evidence does not support another model class.

Do not continue adding models merely to make the comparison section look comprehensive.

## Candidate library

These models are **available options, not a simultaneous shortlist**:

- **Logistic Regression** — default baseline for compatible one-hot/sparse or dense tabular representations.
- **Decision Tree** — first nonlinear step when a simple tree is enough to test interaction/nonlinearity.
- **Random Forest** — stronger nonlinear ensemble when the baseline and/or single-tree evidence justifies an ensemble.
- **HistGradientBoostingClassifier** — conditional boosting candidate when scale, representation, and implementation support make it defensible.
- **LinearSVC** — useful for high-dimensional or sparse spaces when a linear margin-based alternative is warranted.
- **Naive Bayes variants** — useful for sparse/count-like representations.
- **KNN** — consider only on smaller, appropriately scaled datasets where local similarity is plausible.
- **SVC** — consider on moderate-sized numeric spaces when nonlinear boundaries are plausible and compute is acceptable.
- **CatBoostClassifier** — consider for categorical-heavy data only when the runtime and implementation are actually available.

## Candidate screening and status labels

Distinguish three statuses:
- **Not considered:** no evidence-based reason to test the model class, or incompatible representation/runtime.
- **Tested and rejected:** evaluated after the escalation gate but did not justify its added complexity.
- **Retained:** provided a meaningful improvement or a separately required capability that justified its complexity.

For every tested model, report the reason it entered the sequence. Do not produce a generic “finalists” list before any empirical result exists.

## Baseline and complexity citations

Use citations only when they materially support a methodological or implementation statement. Recommended sources include:

- scikit-learn developers. (2026). *LogisticRegression*. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- Varma, S., & Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. *BMC Bioinformatics, 7*, 91. https://doi.org/10.1186/1471-2105-7-91

The Varma and Simon paper supports the caution that repeatedly using CV for model selection can bias the resulting performance estimate; therefore CV scores used for screening/tuning should be described as model-selection estimates rather than unbiased final generalisation estimates.

## Default comparison size

There is **no default requirement to compare three finalists**. The default is one baseline followed by zero, one, or more sequentially justified escalations. More complex classes are added only when each escalation survives the evidence gate above.

## Runtime preflight and user-facing estimate

Before expensive tuning, estimate the workload using the observed dataset size, approximate feature dimensionality, current number of active model classes, CV folds, planned search trials, and whether parallelism/early stopping are available. This is a rough estimate, not a promise of completion time.

Use a range plus workload category rather than false-precision. Suggested categories:
- **Light:** usually under ~1 minute
- **Moderate:** roughly ~1–5 minutes
- **Heavy:** roughly ~5–15 minutes
- **Very heavy:** potentially >15 minutes

These are heuristic categories, not guarantees. The estimate must be based on the current run rather than copied from an example.

### Compute-plan adjustment

If the estimate is heavy or very heavy, automatically apply a lighter compute plan in batch mode. Briefly explain the trade-off in the plan summary. Prefer changes such as:
- reducing CV folds from 5 to 3;
- reducing random trials from 10 to 5;
- performing light baseline screening before any full tuning;
- reducing ensemble size toward the default 100–150 range;
- using early stopping for boosting;
- avoiding tuning of model classes that failed the escalation gate.

Explain the trade-off: lower compute reduces search depth and may increase uncertainty in model-selection decisions. Do not optimize for speed at the expense of a trustworthy comparison.

Do not add a second routine checkpoint after the data-understanding checkpoint. Apply the lighter plan automatically when needed and include the estimate and trade-off in the concise plan/results summary. If the user explicitly asks to choose the compute budget, present the estimate and wait for that choice before tuning.

## Evaluation protocol and CV bias

### Default protocol

Use cross-validation on the development/training data for baseline establishment, model escalation, and hyperparameter selection. When the same CV process is used to choose the model/configuration, treat its score as a **model-selection estimate**, not as an unbiased estimate of final generalisation performance. Varma and Simon (2006) discuss this source of bias.

When an independent held-out test set exists, use the frozen final model on that test set once for the principal out-of-sample evaluation. State the CV-selection limitation in the report.

### Nested cross-validation — conditional, not mandatory

Use nested CV when one or more of the following is true:
- the user explicitly requests a more rigorous internal generalisation estimate;
- no independent test set exists and an unbiased internal estimate is important;
- the dataset/task is being evaluated for research-grade methodological reporting;
- the cost is acceptable relative to the dataset size and compute budget.

Do not force nested CV into ordinary coursework runs with a valid independent test set merely for methodological sophistication; it can substantially increase runtime.

If nested CV is not used, write the limitation clearly rather than implying that the CV score is unbiased.

### CV reporting

Keep fold-level primary-metric results in temporary/internal state. Report mean ± standard deviation in the final results when useful; do not expose raw fold logs.

### Close-result rule

If two sequentially tested models have a very small test-metric difference relative to observed CV variability, do not describe the difference as decisive. When the decision materially depends on a close result, perform a paired uncertainty analysis when feasible; otherwise state that the difference was not subjected to additional uncertainty testing.

## Hyperparameter tuning

Use cross-validation on development/training data only.

Default CV: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` when class counts support it; otherwise reduce folds and document why.

Prefer `RandomizedSearchCV` for larger spaces. Default `n_iter=10` for a finalist unless the problem is trivial or evidence warrants a smaller/larger search. Avoid exhaustive grids over many dimensions.

Typical compact search ranges:

### Logistic Regression
- `C`: 0.01, 0.1, 1, 10, 100
- `class_weight`: None / balanced when imbalance warrants testing

### Decision Tree
- `max_depth`: None, 3, 5, 10, 20
- `min_samples_leaf`: 1, 2, 5, 10
- `class_weight`: None / balanced when appropriate

### Random Forest
- `n_estimators`: 100, 150
- `max_depth`: None, 10, 20
- `min_samples_leaf`: 1, 2, 5
- `max_features`: sqrt, log2
- class weighting when appropriate

### HistGradientBoostingClassifier
- `learning_rate`: 0.03, 0.1
- `max_iter`: 100, 200, 400
- `max_leaf_nodes`: 15, 31, 63
- `l2_regularization`: 0, 1
- use early stopping when supported and appropriate

For adaptive models, use similarly bounded spaces rather than uncontrolled searches.

## Compute budget

Do not promise a universal runtime because dataset size and hardware vary. Instead estimate workload before tuning and choose an appropriate budget.

### Suggested policy
- **Small/easy:** up to 5 CV folds, 5–10 random trials per finalist.
- **Medium:** 3–5 CV folds, about 10 random trials per finalist.
- **Large:** 3 CV folds, about 5–10 trials per finalist, with light screening before tuning.
- **Very large / costly:** reduce folds/trials further, sample or screen candidates when statistically defensible, and explain the trade-off.

Use parallelism where supported (`n_jobs=-1` or runtime-equivalent) while avoiding nested oversubscription. A safe pattern is parallelizing the search and keeping estimators single-threaded during search when necessary.

For tree ensembles, start around 100–150 trees and increase only when validation evidence suggests a meaningful benefit. Do not impose 150 as a universal hard ceiling.

Use early stopping for boosting algorithms when supported.

If expected compute is still excessive, apply the documented budget reduction in batch mode and briefly explain the trade-off in the plan summary.

## Model-specific implementation checks

### HistGradientBoostingClassifier categorical handling

If HistGradientBoostingClassifier is used with categorical variables, explicitly configure categorical handling through `categorical_features` (or the documented equivalent for the installed scikit-learn version). Merely ordinal-encoding categories as integers is not sufficient; without explicit categorical handling those integers may be treated as ordered numeric values.

When a preprocessing pipeline transforms categories before HGB:
- record the categorical feature mapping after transformation;
- verify that the intended encoded columns are passed as categorical features;
- verify category cardinality is compatible with the installed scikit-learn constraints;
- record the scikit-learn version because categorical behavior and parameters can be version-sensitive.

If the implementation cannot reliably preserve the categorical-feature specification through the pipeline, do not claim that HGB used native categorical splits; either use a technically valid alternative representation or exclude HGB from the finalist set.

### Unsupported performance/cost claims

Do not claim a model has the lowest training cost, inference cost, memory footprint, latency, or deployment cost unless the corresponding quantity was actually measured or directly established from a reliable runtime artifact.

Do not infer that HGB is cheaper than Logistic Regression or other models simply from algorithm family. If runtime cost matters, measure it and label the result as an observed runtime measurement.

## Primary metric and reporting

Use **balanced accuracy** as the primary tuning metric when class imbalance is material. Otherwise, accuracy can be primary, with macro-F1 as a robust secondary metric. Explain the choice using the observed class distribution.

When supported, report ROC-AUC for binary classification and appropriate multiclass ROC-AUC. Add PR-AUC when class imbalance makes it informative.

Do not claim probability calibration unless a calibration metric/curve was actually computed.

Report, at minimum:
- mean CV primary metric and variability;
- fold-level CV scores in internal run state;
- final test primary metric;
- macro-F1 where useful;
- best hyperparameters;
- compact model comparison table;
- per-class precision, recall, and F1 when class-level interpretation is relevant;
- at least one useful diagnostic (usually a confusion matrix) when space and relevance permit.

Maintain a reproducibility record in temporary/internal state (or the repository source when appropriate), containing, where applicable:
- Python and package versions;
- LLM model/interface metadata available at runtime;
- random seeds;
- train/validation/test protocol;
- CV strategy and fold count;
- tuning/search strategy, `n_iter`, scoring, and search random state;
- preprocessing pipeline structure and whether `Pipeline`/`ColumnTransformer` was used;
- target-label encoding;
- model-specific solver/iteration/thread settings;
- HGB early-stopping and `categorical_features` configuration;
- winning hyperparameters.

The main two-page report should contain only the compact subset needed for reproducibility; keep exhaustive settings in the repository/artifact rather than padding the report.
