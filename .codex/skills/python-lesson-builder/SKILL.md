---
name: python-lesson-builder
description: Build or update static GitHub Pages lessons for a high-school Python learning web app. Use when creating new lesson HTML pages, updating lesson content, maintaining the shared design system, using tools/generate_lesson.py, or adding links to the lesson index for this class-github-python project.
---

# Python Lesson Builder

Use this skill to create consistent Korean high-school Python lessons for GitHub Pages.

## Workflow

1. Reuse the static app structure:
   - `index.html` lists all lessons.
   - `lessons/lesson-NN.html` contains one lesson.
   - `assets/styles.css` owns the design system.
   - `assets/lesson-runner.js` owns the Pyodide execution behavior.
2. Prefer `tools/generate_lesson.py` for new lesson drafts.
3. Edit generated lesson content only where the lesson needs specific teaching material.
4. Update `index.html` whenever adding a lesson.
5. Keep GitHub Pages deployment static; do not add a backend or build framework unless the user explicitly asks.

## Lesson Requirements

- Write for Korean high-school students who are new to programming.
- Use a calm classroom tone: short explanations, concrete examples, and direct practice prompts.
- Keep every lesson structure consistent:
  - lesson hero with objectives
  - concept cards
  - example code
  - practice section with questions on the left and a runnable Python editor on the right
  - checklist panel
- Use the shared CSS classes instead of inline styles.
- Use the shared runner attributes:
  - `data-python-editor`
  - `data-run-python`
  - `data-runner-status`
  - `data-python-output`

## Generator

Run the default lesson generator from the repository root:

```bash
python tools/generate_lesson.py --force
```

For future lessons, create a JSON content file with these fields and run:

```bash
python tools/generate_lesson.py --content lessons/data/lesson-02.json
```

Required JSON fields:

- `number`
- `title`
- `summary`
- `objectives`
- `concepts`
- `example_code`
- `practices`
- `starter_code`

## Design Rules

- Keep cards at 8px border radius or less.
- Favor readable layouts and clear state changes over decorative elements.
- Preserve the two-column practice layout on desktop and one-column layout on mobile.
- Do not duplicate Pyodide loading logic inside lesson pages.
- Do not create one-off lesson-specific CSS unless the shared design system cannot express the need.

## Verification

- Open `index.html` and the new lesson page locally.
- Confirm all relative links work from the lesson page.
- Confirm the Python runner initializes, executes `print("hello")`, and displays errors.
- Confirm the page remains usable at mobile width.
