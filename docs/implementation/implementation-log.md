# Implementation Log

A concise record of completed work, tracked per merged PR.

---

## PR #1
**Title:** chore: initialize repo structure, CI/CD & docs

**Changes:**
- Created project structure with `src/workflow_clinic` package
- Added Ruff linter and MyPy type checker configuration
- Added Pytest with coverage reporting
- Added GitHub Actions CI pipeline (lint, typecheck, test)
- Added architecture documentation and README

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/1

---

## PR #2
**Title:** feat: add workflow bundle data model

**Changes:**
- Added `WorkflowBundle` Pydantic model
- Added `WorkflowMetadata` model (name, version, author, description)
- Added `Task` and `TaskResources` models
- Added `pydantic` dependency to `pyproject.toml`
- Added unit tests for WorkflowBundle creation

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/2

---

## PR #3
**Title:** ci: fix broken conventional commits parser

**Changes:**
- Fixed bash regex parsing error in PR title validation
- Assigned regex to a variable before evaluation to prevent shell metacharacter issues
- Added explicit `shell: bash` to the validation step

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/3

---

## PR #4
**Title:** style: fix CI linting

**Changes:**
- Removed unused import in `src/workflow_clinic/main.py`

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/4

---

## PR #5
**Title:** ci: upgrade checkout and split PR validation

**Changes:**
- Upgraded `actions/checkout` from v4 to v6 (resolves Node.js 20 deprecation warnings)
- Split PR title validation into a dedicated `pr-title.yml` workflow
- Removed `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` env variable (no longer needed)

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/5

---

## PR #6
**Title:** docs: restructure documentation into architecture and implementation log

**Changes:**
- Renamed `implementation-summary.md` to `architecture.md` (design-only, no PR history)
- Created `implementation-log.md` to track all merged PRs
- Removed empty `docs/research/` and `docs/workflow-analysis/` directories

**Link:** https://github.com/ga4gh/ga4gh_workflow_clinic_gsoc_2026/pull/6
