# Assignment 7 — Week 7 Final Sprint & Demo Day

## Focus

Assignment 7 covers the final week of the course — **Week 7 (Sprint 6)**. Building on the trial release and customer feedback from Week 6, Assignment 7 focuses on completing the final course version **MVP v3**, executing the final product transition, confirming customer usefulness, preparing the Demo Day presentation, recording the public sanitized demo video, and submitting the final Week 7 deliverables.

This is the **last assignment** of the course. All earlier maintained assets — tests, CI, architecture, development-process documentation, hosted documentation, customer handover, contributor guidance, and agent guidance — must be current and reflect the final state of the product.

Use [Artifact Requirements](Artifact_Requirements.md) as the authoritative source for shared artifact terminology, report semantics, release artifacts, screenshot evidence, Sprint Review artifacts, maintained handover artifact structure, hosted artifact visibility, public sanitized demo video handling, presentation-slide privacy, and public/private evidence handling. Use [Process Requirements](../Process_Requirements.md) as the authoritative source for Scrum, Product Backlog, traceability, Definition of Done, quality requirements and QRTs, architecture and ADR, and UAT semantics. Use [Repository Requirements](../Repository_Requirements.md) as the authoritative source for repository workflow, releases and changelog, issue-linked workflow, configuration secrets baseline, and CI automation.

For Assignment 7:

- `docs/customer-handover.md` is the maintained customer-handover artifact.
- `reports/week7/README.md` is the Week 7 public report and final Assignment 7 submission index.
- The Week 7 Moodle PDF is the single canonical private submission wrapper containing private permalinks, identity, credentials, presentation slides, rehearsed presentation video, and access details.

## Part 1: Complete Sprint 6 and Finalize MVP v3

1. Complete all remaining Sprint 6 PBIs that were planned or discovered during Week 6 customer feedback.

2. Ensure every Sprint 6 PBI has:
   - clear expected outcome
   - acceptance criteria
   - Story Points
   - implementer
   - different reviewer
   - current Work Status

3. Verify acceptance criteria before merge according to [Process Requirements](../Process_Requirements.md#acceptance-criteria).

4. Keep PRs issue-linked and reviewed according to [Repository Requirements](../Repository_Requirements.md#issue-linked-workflow-requirements).

5. Keep all earlier assignment tests, quality gates, CI checks, QRTs, architecture documentation, and development-process documentation current when Sprint 6 changes affect those areas.

6. Update `docs/roadmap.md` to reflect MVP v3 as the final course version. Do not extend the roadmap beyond the course endpoint.

## Part 2: Finalize the Product Transition and Confirm Customer Usefulness

1. Complete the final transition in Week 7 based on the transition-readiness findings from Week 6.

2. `MVP v3` must include:
   - final product changes selected for Sprint 6
   - fixes or improvements discovered during the Week 6 customer trial
   - updated customer-facing documentation and handover material
   - the final product access arrangement for course evaluation and customer use

3. Deploy or otherwise provide `MVP v3` so the customer and TA can access it.

4. Keep the final product access artifact accessible until grading is complete.

5. Confirm the final transition outcome with the customer or relevant stakeholder.

6. Ask the customer explicitly whether they accept `docs/customer-handover.md` as sufficient for the reached handover level.

7. In `docs/customer-handover.md` and `reports/week7/README.md`, state explicitly which handover level was reached:

   - `Ready for independent use`
   - `Independently used by customer`
   - `Deployed or operated on customer side`

8. Also state the customer-confirmation status as one of:

   - `Accepted`
   - `Accepted with follow-up items`
   - `Not yet accepted`

9. Preserve inspectable evidence of customer use, deployment, or operation where practical. Sanitized public summary belongs in the Week 7 report. Private details belong only in the Moodle PDF.

10. If stronger transition levels were not reached, explain why not and what remains.

11. If customer-confirmation is `Accepted with follow-up items` or `Not yet accepted`, explain what follow-up items remain, whether the blocker is team-side, customer-side, or external, and what actions would be needed for full acceptance.

## Part 3: Release MVP v3

1. Create a new SemVer release for MVP v3 with higher precedence than the Week 6 trial release.

2. The MVP v3 release must:

   - use a SemVer tag prefixed with `v`
   - point to a commit on the protected default branch
   - identify that it maps to `MVP v3`
   - link to the Sprint 6 milestone
   - link to current run or access instructions
   - link to `docs/customer-handover.md`
   - link to `reports/week7/README.md`
   - link to the public sanitized demo video

3. Update `CHANGELOG.md` by moving the final released entries from `[Unreleased]` into a dated SemVer section.

4. Update the root `README.md` with any final changes to setup, usage, run, or deployment instructions.

## Part 4: Update and Execute User Acceptance Tests

1. Maintain active UAT scenarios in `docs/user-acceptance-tests.md`.

2. Execute relevant UAT scenarios for customer-critical or changed user-facing behavior during Week 7.

3. In `reports/week7/README.md`, summarize:

   - which UAT scenarios passed
   - which scenarios failed or still need changes
   - the most important feedback points received
   - resulting PBIs or issues

## Part 5: Conduct Sprint 6 Review

1. Conduct a Sprint Review for Sprint 6 according to [Process Requirements](../Process_Requirements.md#sprint-cadence-and-scrum-events).

2. The Sprint Review must discuss at minimum:

   - the planned Sprint 6 Goal
   - delivered MVP v3
   - resolved and unresolved follow-up issues from Week 6
   - final transition status and usefulness
   - customer use, deployment, or operational status
   - remaining risks and post-course limitations

3. Write the Sprint Review summary in:

   ```text
   reports/week7/sprint-review-summary.md
   ```

4. If using a transcript (when publication is permitted), write it in:

   ```text
   reports/week7/sprint-review-transcript.md
   ```

5. If using notes instead (when recording or private sharing is refused), write detailed English notes in:

   ```text
   reports/week7/sprint-review-notes.md
   ```

## Part 6: Conduct Sprint 6 Retrospective

1. Conduct a Sprint Retrospective after the Sprint Review.

2. Write to:

   ```text
   reports/week7/retrospective.md
   ```

3. Use the retrospective structure defined in [Artifact Requirements](Artifact_Requirements.md#retrospective-artifact).

## Part 7: Reflect on Week 7 and Report LLM Usage

1. Write the Week 7 reflection emphasizing what the team learned from follow-up maintenance, final transition, customer usefulness feedback, and final delivery of MVP v3.

2. Write to:

   ```text
   reports/week7/reflection.md
   ```

3. Write the LLM usage report to:

   ```text
   reports/week7/llm-report.md
   ```

## Part 8: Prepare, Rehearse, and Present at Demo Day

1. Refine the slide deck based on Week 7 lab rehearsal feedback.

2. Submit the updated slide deck as a PDF together with the Week 7 Moodle PDF.

3. The Week 7 Moddle PDF must include a private link to the rehearsed presentation video showing team members standing and presenting.

4. All team members must attend the Week 8 Demo Day presentation.

5. Each team member must present at least one slide during Demo Day.

6. Timing for Demo Day:

   - 7 minutes for the presentation
   - 7 minutes for Q&A
   - the presentation will be stopped when the time runs out

7. Include a well-rehearsed pre-recorded demo under 2 minutes.

8. Suggested presentation structure:

   - project context and target users
   - final product and most important delivered requirements
   - pre-recorded demo under 2 minutes
   - customer usefulness: what part is in use and whether deployed on customer side
   - key engineering, process, and quality evidence
   - remaining limitations and handover status
   - team contribution and reflection
   - links to deployed product and repository

9. Keep the presentation concise and narrative-driven. Do not read notes from a phone or laptop.

10. Explain clearly whether the customer is actually using the product and if not, why not.

11. During Q&A, the person who worked on the relevant part should answer where possible.

## Part 9: Record a Public Sanitized Demo Video for MVP v3

1. Record a public sanitized demo video according to [Artifact Requirements](Artifact_Requirements.md#public-sanitized-demo-video-artifact).

2. The video must explain the final state of MVP v3, including what was improved, fixed, or added during Sprint 6.

3. Link the video from `reports/week7/README.md` and from the MVP v3 release.

## Part 10: Keep Maintained Documentation Current

1. Ensure all maintained documentation reflects the final state:

   - `README.md` — final entry point
   - `CONTRIBUTING.md` — final contributor guidance
   - `AGENTS.md` — final agent guidance
   - `docs/customer-handover.md` — final handover state
   - `docs/roadmap.md` — final sprint history
   - `docs/backlog.md` — complete PBI history
   - All architecture, ADR, testing, quality, dev-process docs

2. Update when any access details, deployment steps, limitations, transition status, or workflow expectations changed during Sprint 6.

## Week 7 Report

Create the following public report structure:

```text
reports/week7/
|-- README.md
|-- sprint-review-summary.md
|-- sprint-review-transcript.md  # if publication is permitted
|-- sprint-review-notes.md       # if recording or private sharing is refused
|-- reflection.md
|-- retrospective.md
|-- llm-report.md
`-- images/
```

`reports/week7/README.md` is the final Assignment 7 submission index. It must link the complete relevant Week 6 evidence instead of duplicating it.

### Week 7 Report Contents

Include:

1. Link to `reports/week6/README.md`.
2. Link to the Product Backlog board or view.
3. Link to the Sprint 6 Backlog board or view.
4. Link to the Sprint 6 milestone.
5. Sprint 6 Goal, Sprint dates, and short scope summary.
6. Total Sprint 6 size in Story Points.
7. Summary of Week 7 follow-up maintenance and final MVP v3 changes.
8. Link to the final product access artifact.
9. Link to current access or run instructions.
10. Link to `README.md`.
11. Link to `CONTRIBUTING.md`.
12. Link to `AGENTS.md`.
13. Link to `docs/customer-handover.md`.
14. Link to the hosted documentation site.
15. Final transition outcome summary stating handover level and customer-confirmation status.
16. Summary of what was transferred, delegated, or made available during final transition.
17. Explanation of remaining blockers, limitations, or follow-up items.
18. Summary of customer-independent use, deployment, or operation evidence.
19. Customer feedback response table for Sprint 6 follow-up work.
20. Summary of relevant Week 7 UAT results.
21. Link to the final MVP v3 SemVer release.
22. Link to `CHANGELOG.md`.
23. Link to the public sanitized demo video.
24. Demo Day preparation summary.
25. Link to sprint-review summary/transcript/notes.
26. Link to `reports/week7/reflection.md`.
27. Link to `reports/week7/retrospective.md`.
28. Link to `reports/week7/llm-report.md`.
29. Summary of final product status.
30. Contribution traceability table for each team member.
31. Embedded screenshots from `reports/week7/images/` for Sprint milestone, final release, final product access, example PR, and other inspectable evidence.

## Week 7 Moodle PDF

Create one Moodle PDF named `Team_28_TickFrame.pdf` containing:

1. Project name and team number.
2. Team table with full names, emails, GitHub usernames, Scrum roles, technical responsibilities.
3. Who did what during Sprint 6.
4. Who did not participate.
5. Commit-hash permalink to `reports/week7/README.md`.
6. Commit-hash permalink to the final product repository tree.
7. Link to Week 7 private recording for Sprint Review, transition confirmation, UAT.
8. Exact private timecodes if one recording covers multiple activities.
9. Sanitized transcript or detailed notes if publication was refused.
10. Private access instructions for final product access artifact.
11. Private proof of transition-confirmation request and response.
12. Any other instructor-only evidence (consent, credentials, customer-identifying details).

## Submission Procedure

- Submit the Week 7 PDF through Moodle together with the updated slide-deck PDF by the end of Week 7.
- Include the private link to the rehearsed presentation video inside the Week 7 Moodle PDF.
- One Week 7 PDF and one slide-deck PDF per team.

## AI and LLM Usage

You may use AI tools and LLMs. However:

1. Explicitly report which tools were used and how.
2. The submission must contain meaningful analysis and original team effort.
3. Do not submit filler text, generic AI-generated content, or unnecessary explanations.

Failure to disclose AI usage or submitting low-value AI-generated content may result in a failing grade.
