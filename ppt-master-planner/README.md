# PPT Master Planner

> AI-driven presentation generator with integrated project planning. An open-source skill merging PPT Master's execution pipeline with explicit planning workflows.

**Core Pipeline**: `Source Document → Planning Phase → Create Project → [Template] → Strategist → [Image_Generator] → Executor → Quality Check → Post-processing → Export`

## Quick Install

```shell
npx skills add https://github.com/<your-org>/ppt-master-planner/tree/main/ppt-master-planner --skill ppt-master-planner
```

Or clone and copy:

```shell
git clone https://github.com/<your-org>/ppt-master-planner.git
cp -R ppt-master-planner/ppt-master-planner ~/.claude/skills/ppt-master-planner
```

Then ask your agent:

```
Use ppt-master-planner to turn this document into an editable PPTX with planning.
Start from content planning, then show me the outline before generating SVG pages.
```

## Project Structure

```
ppt-master-planner/
├── SKILL.md              ← Main workflow authority (start here)
├── agents/               ← Agent config files
├── references/           ← Role definitions and technical specs
├── scripts/              ← Python tool scripts
├── templates/            ← Layout, chart, icon, brand templates
└── workflows/            ← Standalone workflow files
```

## License

MIT