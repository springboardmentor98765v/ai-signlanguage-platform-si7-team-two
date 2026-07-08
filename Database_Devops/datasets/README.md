# Datasets — Database & DevOps (Intern 5)

This folder contains the raw and processed datasets used to seed and validate the Sign Language Platform database.

## Files

### `sign_dataset.csv`

| Property | Value |
|---|---|
| **Source** | MediaPipe hand-landmark extraction (mirrored from `dataset/` in `main`) |
| **Rows** | ~100 samples (Day 1 seed; grows each sprint) |
| **Columns** | 63 landmark coordinates (`x0–z20`) + 1 label column |
| **Label** | Single uppercase letter (`A`–`Z`) representing the ASL sign |

#### Column Layout

```
x0, y0, z0,   # Landmark 0 (wrist)
x1, y1, z1,   # Landmark 1
...
x20, y20, z20, # Landmark 20 (pinky tip)
label          # e.g. "A", "B", ..., "Z"
```

Each row is one normalized hand pose captured from a 21-point MediaPipe skeleton.

## Usage

- **Schema seeding**: referenced by `db/schema/seed.sql` for inserting sample gesture records
- **Model training**: consumed by the AIML_CV pipeline to train the gesture classifier
- **DB validation**: used to cross-check that `raw_landmarks` JSONB columns store data correctly

## Notes

- Do **not** commit large binary datasets (>50 MB) — use a cloud storage link instead and reference it here
- Coordinate values are normalized (0–1 range relative to image frame)
