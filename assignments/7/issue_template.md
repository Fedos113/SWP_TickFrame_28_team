# Assignment 7 — Issue Template (Week 7 / Sprint 6)

> Use this template for every Sprint 6 (Week 7) issue. Fill out all applicable sections.
> **For non-PBI issues** (documentation reports, repo management, course tasks, transition work): skip sections marked _PBI-only_.

---

## Issue Metadata

| Field | Instructions |
|---|---|
| **Title** | `{PBI-XXX} Short description` or `DOC: short description` or `TRA: short description` |
| **Type** | Enhancement / Bug / Documentation / Testing / Architecture / Course Task / Transition |
| **Sprint** | [Sprint 6 — MVP v3 (Week 7)](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7) |
| **Backlog Location** | Product Backlog → Sprint 6 section in [`docs/backlog.md`](../../docs/backlog.md) |
| **MVP Version** | `MVP v3` |

---

## Description

_What is this issue about? Why does it matter for MVP v3, final transition, Demo Day, or Assignment 7?_

---

## Expected Outcome

_What should be true after this issue is completed?_

---

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Story Points _(PBI-only — skip for course tasks / docs / transition / repo management)_

Modified Fibonacci: 1, 2, 3, 5 — no more than 5, opt for 1 or 2.

**SP: _ _**

---

## Roles _(PBI-only — skip for course tasks / docs / transition / repo management)_

| Role | Person |
|---|---|
| **Implementer** | @username |
| **Reviewer** | @username (must be a different person) |

---

## Work Status

- [ ] **To Do** — not yet started
- [ ] **Ready** — refined, estimated, ready to start
- [ ] **In Progress** — actively being worked on
- [ ] **Review** — PR/MR is open, awaiting review
- [ ] **Done** — merged to `main`, AC satisfied, DoD met

---

## Links to Assignment 7 Artifacts

| Artifact | Link |
|---|---|
| PR/MR | `#_` (link after creation) |
| PR added to contributions table | [contributions.md](contributions.md) |
| Related ADR (if applicable) | [`docs/architecture/adr/ADR-NNN-*.md`](../../docs/architecture/adr/) |
| Related quality requirement | QR-00X |
| Related UAT scenario | UAT-00X |
| Related customer handover section | [`docs/customer-handover.md`](../../docs/customer-handover.md) |

> **PR requirement:** The PR/MR must link to this issue and verify the relevant acceptance criteria before merging ([Repository_Requirements.md §Issue-Linked Workflow](../Repository_Requirements.md#issue-linked-workflow-requirements)).

---

## Definition of Done Checklist

- [ ] All acceptance criteria are satisfied
- [ ] Reviewed and approved by a different team member
- [ ] All CI checks pass (ruff, mypy, pytest+cov, bandit, lychee)
- [ ] No secrets, credentials, or PII committed
- [ ] CHANGELOG.md updated for user-visible changes _(PBI-only)_
- [ ] Relevant documentation updated
- [ ] PR/MR links to this issue and verifies acceptance criteria before merge
- [ ] PR is recorded in the [contributions.md](contributions.md) table
- [ ] Branch deleted after merge
