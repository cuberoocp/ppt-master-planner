# PPT Master Planner

> AI-driven presentation generator with integrated project planning. An open-source skill for AI agents to convert source documents into editable PPTX.

**Version**: 0.1.0

## Quick Install

```shell
npx skills add https://github.com/cuberoocp/ppt-master-planner/tree/main/ppt-master-planner --skill ppt-master-planner
```

Or clone and copy:

```shell
git clone https://github.com/cuberoocp/ppt-master-planner.git
cp -R ppt-master-planner/ppt-master-planner ~/.claude/skills/ppt-master-planner
```

Then ask your agent:

```
Use ppt-master-planner to turn this document into an editable PPTX with planning.
```

## Structure

```
ppt-master-planner-repo/
├── ppt-master-planner/    ← Skill root
│   ├── SKILL.md           ← Main workflow authority
│   ├── agents/            ← Agent config files
│   ├── references/        ← Role definitions and technical specs
│   ├── scripts/           ← Python tool scripts
│   ├── templates/          ← Layout, chart, icon, brand templates
│   └── workflows/         ← Standalone workflow files
└── projects/              ← User project workspace (gitignored)
```

## License

MIT