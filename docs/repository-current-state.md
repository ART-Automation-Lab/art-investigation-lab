# Repository Current State

Last updated: 2026-08-27

## What this repository does

ART Investigation Lab is a React/Vite application for presenting and exploring structured investigation briefs.
It renders investigation data from repository JSON files into three main product surfaces:

- Homepage
- Walkthrough
- Workflow

## Major architecture

- `src/main.tsx` mounts the app and wraps it in `BrowserRouter`.
- `src/App.tsx` defines the top-level routes and composes the shared shell.
- `src/components/Header/` contains the global header.
- `src/features/home/` contains the landing page.
- `src/features/core/walkthrough/` contains the walkthrough experience, including Markdown rendering and presentation helpers.
- `src/features/core/workflow/` contains the workflow canvas.
- `src/features/aoi/` contains the AOI explorer surface.
- `src/data/` contains the InvestigationBrief loader, validator, and repository data.
- `src/types/` contains the TypeScript types for the app data models.
- `contracts/` contains the locked schema and contract documents.
- `deployment/` contains static deployment assets and packaging material.

## Important data flows

1. InvestigationBrief JSON files are stored under `src/data/investigations/industries/...`.
2. `src/data/investigationBriefLoader.ts` loads the JSON files with Vite `import.meta.glob`.
3. `src/data/investigationBriefValidator.ts` validates the loaded JSON against the InvestigationBrief shape.
4. The app routes render the validated briefs in the homepage, walkthrough, and workflow views.
5. The build script produces a production bundle and a standalone package.

## Source-of-truth boundaries

- InvestigationBrief JSON files in `src/data/investigations/` are the working source of truth for the UI.
- `contracts/AIL-INVESTIGATION-BRIEF-JSON-SCHEMA-V1.json` is the schema contract.
- `contracts/AIL-INVESTIGATION-BRIEF-CONTRACT-V1.md` and `contracts/INVESTIGATION-BRIEF-COMPILER-CONTRACT-V1.md` describe the locked contract expectations.
- Presentation code must not invent missing research meaning, provenance, or decision states.

## Important directories

- `src/` — application code, data loading, validation, and UI features
- `src/data/investigations/` — investigation JSON inputs used by the UI
- `contracts/` — schema and contract documentation
- `deployment/` — deployable static assets and packaging files
- `public/` — browser-served static files
- `tests/` — repository tests, where present
- `scripts/` — build and validation helpers

## Build and test state

- The repository is a Vite + TypeScript app.
- `npm run build` runs TypeScript, Vite production build, and the standalone packaging step.
- `npm run lint` runs ESLint.
- `npm run aoi:validate` validates AOI integrity.

## Known limitations

- The repository keeps product data and presentation code separate, but the UI still depends on the local JSON data being valid.
- The app is intentionally data-driven, so missing or malformed InvestigationBrief JSON will fail validation rather than being silently repaired.
- The repository does not use a permanent database or backend service for this front-end application.
