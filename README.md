# skill-marketplace

A Claude Code plugin marketplace for testing and experimentation.

## Setup

Register this marketplace with Claude Code (one-time):

```bash
claude plugin marketplace add emayssat/skill-marketplace
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `hello-world` | Minimal dummy skill to verify marketplace installation works |
| `six-thinking-hats` | Edward de Bono's Six Thinking Hats for structured parallel thinking |
| `storyboard` | Produce and review storyboards with a full crew and audience persona system |

## Install a Plugin

```bash
claude plugin install hello-world@skill-marketplace
```

## Verify Installation

After installing, tell Claude "hello world" and it will respond using the `hello-world` skill.

## Manage Plugins

```bash
claude plugin list                          # list installed plugins
claude plugin disable hello-world           # disable without uninstalling
claude plugin enable hello-world            # re-enable
claude plugin uninstall hello-world         # remove
```

---

Want to contribute a skill? See [DEVME.md](DEVME.md).