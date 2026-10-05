# Developer Guide

This file is for contributors developing new skills in this marketplace.

## Skill Structure

```
plugins/<plugin-name>/
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md          # required — skill definition and trigger description
        └── references/       # optional — supporting files the skill reads at runtime
            └── *.md
```

## Development Workflow

### 1. Create the skill structure

Add your plugin directory under `plugins/` following the layout above.

### 2. Iterate locally (no push required)

Symlink the skill directory straight into `~/.claude/skills/` so Claude picks it up immediately without going through the plugin system:

```bash
ln -s "$(pwd)/plugins/<plugin-name>/skills/<skill-name>" \
      ~/.claude/skills/<skill-name>
```

Edit `SKILL.md`, test by talking to Claude, repeat. Changes are reflected instantly — no reinstall needed.

### 3. Remove the local symlink when done

```bash
rm ~/.claude/skills/<skill-name>
```

### 4. Push to GitHub

```bash
git add plugins/<plugin-name>
git commit -m "add <plugin-name> plugin"
git push
```

### 5. Install or update the plugin from the marketplace

If installing for the first time:
```bash
claude plugin install <plugin-name>@skill-marketplace
```

If the plugin was already installed and you pushed an update:
```bash
claude plugin update <plugin-name>@skill-marketplace
```

## Tips

- Keep each skill focused on a single domain — overlap in trigger descriptions causes unpredictable activation.
- The `description` frontmatter field in `SKILL.md` is what Claude reads to decide when to invoke the skill. Write it with explicit trigger phrases users are likely to say.
- Put large reference content (examples, style guides, reference tables) in `references/*.md` rather than inline in `SKILL.md` — the skill reads them on demand, keeping the main file concise.
- Use the `hello-world` plugin as a sanity check after registering the marketplace for the first time.
