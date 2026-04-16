# Source Map — {person_name} ({meta.role})

> Traceability matrix: every artifact in this bundle maps back to the exact interview questions it was synthesized from. This enables verification, updates, and debugging of the cognitive clone.

---

## Question Index

| Q-ID | Section | Title | Used in |
|---|---|---|---|
{one_row_per_question_with_artifacts_using_it}

---

## Artifact Index

### Agents

| Agent | Consumes Questions | Consumes Directives |
|---|---|---|
{one_row_per_agent}

### Skills

| Skill | Consumes Questions | Consumes Directives |
|---|---|---|
{one_row_per_skill}

### Commands

| Command | Consumes Questions | Consumes Directives |
|---|---|---|
{one_row_per_command}

### Rules

| Rule | Consumes Questions | Consumes Directives |
|---|---|---|
{one_row_per_rule}

### Hooks (if applicable)

| Hook | Consumes Questions | Consumes Directives |
|---|---|---|
{one_row_per_hook}

---

## Contradiction Index

| Tension | Questions | Resolution Reference |
|---|---|---|
{one_row_per_contradiction}

---

## Re-profiling Notes

When re-running CEET:

- Changing the answer to a question listed above will affect every artifact in its "Used in" column
- The system will regenerate only affected artifacts — unchanged directives stay untouched
- `profile-changelog.md` will record what moved
