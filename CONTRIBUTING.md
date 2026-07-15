# Contributing / Git Workflow

Day 6 deliverable (SRS §6, Intern 5, Day 6): branching strategy, so all
five interns can work in parallel without stepping on each other, per the
"parallel, domain-wise development" model in SRS §1.1.

## Branches

- **`main`** — always deployable. Only the shared `integration` branch
  merges here, never a feature branch directly.
- **`integration`** — the shared branch all five interns merge into during
  the week. Per SRS §7.3: *"Shared Git repository with each intern's own
  feature branch, merged into a common integration branch by Day 6."*
  This is where Day 7's full end-to-end integration testing happens.
- **`intern-<n>/<short-description>`** — one feature branch per piece of
  work, e.g.:
  - `intern-1/practice-page-webcam`
  - `intern-2/auth-jwt-rbac`
  - `intern-3/mediapipe-landmark-pipeline`
  - `intern-4/assessment-scoring-engine`
  - `intern-5/day5-docker-compose`

  Branch off `integration`, not `main`.

## Workflow

1. Branch off `integration`: `git checkout integration && git pull && git checkout -b intern-5/day6-ci`
2. Commit with clear messages (SRS NFR "Maintainability": *"pushed to Git
   with clear commit messages for smooth Milestone 2 handover"*).
3. Open a PR into `integration` (not `main`). CI (`.github/workflows/ci.yml`)
   runs automatically — lint + a real migration/verification run against a
   throwaway Postgres, plus a Docker build check.
4. Once your daily stand-up confirms no blocking dependency issues (SRS
   §7.1's Dependency Matrix check), merge into `integration`.
5. `integration` → `main` happens once during Day 7's full integration
   pass (SRS §8.1), after the whole team walks through the end-to-end
   learner journey together.

## Commit messages

Any reasonable convention is fine as long as it's consistent; suggested:
```
<area>: <short summary>

intern5-db: add Day 4 practice_sessions/assessments/feedback models
intern2-api: implement JWT auth middleware
```

## Daily sync (SRS §7)

Every stand-up, check the Dependency Matrix (SRS §5) — if your branch
unblocks or depends on someone else's, say so explicitly before merging
into `integration`, so nobody's PR silently breaks another intern's
in-progress work.
