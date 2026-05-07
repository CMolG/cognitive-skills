# Eval report — seed-2026-05-07

> schemaVersion: `1.0.0`
> tasks scored: 3

| Task | Arm | Words | Phrases | Sections | Voice | Composite |
|---|---|---:|---:|---:|---:|---:|
| `copy-headlines` | `baseline` | 61 | 0.33 | 1.00 | 0.2732 | 0.54 |
| `copy-headlines` | `ceet` | 113 | 1.00 | 1.00 | 0.3107 | 0.77 |
| `copy-headlines` | `generic` | 50 | 0.00 | 1.00 | 0.2187 | 0.41 |
| `engineering-pr-review` | `baseline` | 177 | 0.40 | 1.00 | 0.366 | 0.59 |
| `engineering-pr-review` | `ceet` | 451 | 1.00 | 1.00 | 0.5615 | 0.85 |
| `engineering-pr-review` | `generic` | 132 | 0.20 | 1.00 | 0.1304 | 0.44 |
| `product-prd-draft` | `baseline` | 101 | 1.00 | 1.00 | 0.3524 | 0.78 |
| `product-prd-draft` | `ceet` | 454 | 1.00 | 1.00 | 0.4421 | 0.81 |
| `product-prd-draft` | `generic` | 112 | 1.00 | 1.00 | 0.197 | 0.73 |

## Deltas (ceet vs control arms)

| Task | ceet − baseline | ceet − generic |
|---|---:|---:|
| `copy-headlines` | 0.2347 | 0.364 |
| `engineering-pr-review` | 0.2651 | 0.4103 |
| `product-prd-draft` | 0.0299 | 0.0817 |
