# Local Configuration Reference

## Table of Contents

- 2.1 What is local plugin configuration - Development plugin setup
- 2.2 Directory structure - Required plugin layout
  - 2.2.1 Root directory - Plugin container
  - 2.2.2 .claude-plugin folder - Manifest location
  - 2.2.3 Component directories - commands, agents, skills, hooks
- 2.3 Configuration procedure - Setting up local plugin
  - 2.3.1 Directory creation - Making plugin folder
  - 2.3.2 Manifest creation - Writing plugin.json
  - 2.3.3 Component setup - Adding commands, agents, etc.
  - 2.3.4 Launch configuration - Using --plugin-dir flag
- 2.4 Development workflow - Edit, restart, test cycle
- 2.5 Multiple plugins - Loading several local plugins
- 2.6 Examples - Local configuration scenarios
- 2.7 Troubleshooting - Local plugin issues

---

## 2.1 What is local plugin configuration

Local plugin configuration is the setup of plugins for development without marketplace installation. Benefits:

- Immediate testing of changes
- No need to publish to test
- Easy debugging
- Quick iteration

---

## 2.2 Directory structure

### 2.2.1 Root directory

The plugin root contains all plugin files:

```
my-plugin/
├── .claude-plugin/       # Metadata directory
├── commands/             # Command definitions
├── agents/               # Agent definitions
├── skills/               # Skill directories
├── hooks/                # Hook configurations
├── scripts/              # Scripts for hooks
└── README.md             # Plugin documentation
```

### 2.2.2 .claude-plugin folder

Contains the plugin manifest:

```
.claude-plugin/
└── plugin.json           # REQUIRED: Plugin manifest
```

**plugin.json structure:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  }
}
```

### 2.2.3 Component directories

**IMPORTANT:** Components go at plugin ROOT, NOT inside .claude-plugin!

**Correct:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/          ← HERE
├── agents/            ← HERE
└── skills/            ← HERE
```

**Wrong:**
```
my-plugin/
└── .claude-plugin/
    ├── plugin.json
    ├── commands/      ← WRONG!
    └── agents/        ← WRONG!
```

---

## 2.3 Configuration procedure

### 2.3.1 Directory creation

```bash
# Create plugin directory structure
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands
mkdir -p my-plugin/agents
mkdir -p my-plugin/skills
mkdir -p my-plugin/hooks
mkdir -p my-plugin/scripts
```

### 2.3.2 Manifest creation

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Description of what this plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "Apache-2.0"
}
```

**Required fields:**
- `name`: Kebab-case, unique identifier

**Optional fields:**
- `version`: Semantic version
- `description`: Human-readable description
- `author`: Author information
- `license`: License identifier

### 2.3.3 Component setup

**Add a command (commands/my-command.md):**
```markdown
---
name: my-command
description: What this command does
arguments: []
---

# My Command

Instructions for the command...
```

**Add an agent (agents/my-agent.md):**
```markdown
---
name: my-agent
description: What this agent does
---

# My Agent

You are an agent that...
```

**Add a hook (hooks/hooks.json):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-hook.py"
          }
        ]
      }
    ]
  }
}
```

### 2.3.4 Launch configuration

**Use --plugin-dir flag to load local plugin:**

```bash
# Launch with local plugin
claude --plugin-dir /absolute/path/to/my-plugin

# Or with relative path from current directory
claude --plugin-dir ./my-plugin
```

---

## 2.4 Development workflow

### Edit-Restart-Test Cycle

1. **Edit:** Make changes to plugin files
2. **Restart:** Exit and relaunch Claude Code
3. **Test:** Verify changes work
4. **Repeat:** Continue until done

**No hot-reload:** Changes require restart to take effect.

### Quick restart tips

```bash
# In Claude Code
/exit

# Relaunch with plugin
claude --plugin-dir ./my-plugin

# Test your changes
/my-command
```

---

## 2.5 Multiple plugins

Load multiple local plugins simultaneously:

```bash
claude --plugin-dir ./plugin-a --plugin-dir ./plugin-b --plugin-dir ./plugin-c
```

**Notes:**
- Each plugin must have unique name
- Hooks from all plugins are merged
- Commands from all plugins are available
- Conflicts in names cause errors

---

## 2.6 Examples

### Example 1: Minimal Plugin

```bash
# Create minimal plugin
mkdir -p my-plugin/.claude-plugin

cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A minimal plugin"
}
EOF

# Launch
claude --plugin-dir ./my-plugin
```

### Example 2: Plugin with Command

```bash
# Create plugin with command
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands

cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin with custom command"
}
EOF

cat > my-plugin/commands/hello.md << 'EOF'
---
name: hello
description: Say hello
arguments: []
---

# Hello Command

When the user runs /hello, respond with a friendly greeting.
EOF

# Launch
claude --plugin-dir ./my-plugin

# Test
/hello
```

### Example 3: Plugin with Hook

```bash
# Create plugin with hook
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/hooks
mkdir -p my-plugin/scripts

cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin with hook"
}
EOF

cat > my-plugin/hooks/hooks.json << 'EOF'
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/log-prompt.sh"
          }
        ]
      }
    ]
  }
}
EOF

cat > my-plugin/scripts/log-prompt.sh << 'EOF'
#!/bin/bash
echo "Prompt received at $(date)" >> /tmp/prompt-log.txt
exit 0
EOF

chmod +x my-plugin/scripts/log-prompt.sh

# Launch
claude --plugin-dir ./my-plugin
```

---

## 2.7 Troubleshooting

### Issue: Plugin not loading

**Symptoms:** Commands not available, hooks not firing.

**Resolution:**
1. Verify plugin.json exists and is valid JSON
2. Check plugin name is valid (kebab-case)
3. Verify --plugin-dir path is correct
4. Check for error messages at startup

### Issue: Command not found

**Symptoms:** /my-command returns "unknown command".

**Resolution:**
1. Check command file is in commands/ directory
2. Verify YAML frontmatter is valid
3. Check command name in frontmatter matches
4. Restart Claude Code

### Issue: Hook not executing

**Symptoms:** Hook script not running.

**Resolution:**
1. Check hooks/hooks.json syntax
2. Verify script path uses ${CLAUDE_PLUGIN_ROOT}
3. Make script executable: `chmod +x script.sh`
4. Check script has proper shebang
5. Test script manually first

### Issue: Script not found

**Symptoms:** Error about script path not found.

**Resolution:**
1. Use ${CLAUDE_PLUGIN_ROOT} not relative paths
2. Verify script exists at specified location
3. Check for typos in path
4. Ensure scripts/ directory is at plugin root

### Issue: Components in wrong location

**Symptoms:** Plugin loads but components missing.

**Resolution:**
1. Move commands/, agents/, skills/ to plugin ROOT
2. NOT inside .claude-plugin/
3. Restart Claude Code
