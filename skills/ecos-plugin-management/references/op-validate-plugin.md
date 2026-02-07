---
operation: validate-plugin
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Validate Plugin Installation

## When to Use

- Before publishing a plugin
- When plugins fail to load
- When hooks do not fire as expected
- After modifying plugin files
- When verifying plugin structure
- Before installing plugin on agents

## Prerequisites

- Plugin directory exists
- Claude Code CLI available
- Python with validation scripts (optional but recommended)

## Procedure

### Step 1: Run Claude Code Plugin Validate

```bash
claude plugin validate /path/to/my-plugin
```

This checks:
- JSON syntax in plugin.json
- Required fields present
- Directory structure valid
- Path references accessible

### Step 2: Validate plugin.json Manually

```bash
# Check JSON syntax
jq . /path/to/my-plugin/.claude-plugin/plugin.json

# Required fields check
jq -e '.name and .version' /path/to/my-plugin/.claude-plugin/plugin.json
```

### Step 3: Check Directory Structure

```bash
# Verify components at root
ls -la /path/to/my-plugin/
# Should see: .claude-plugin/, commands/, agents/, hooks/, scripts/

# NOT inside .claude-plugin/
ls /path/to/my-plugin/.claude-plugin/
# Should ONLY see: plugin.json (not commands/, agents/, etc.)
```

### Step 4: Validate Hook Scripts

```bash
# Check scripts are executable
ls -la /path/to/my-plugin/scripts/
# Should show x permission

# Validate hooks.json
jq . /path/to/my-plugin/hooks/hooks.json

# Check hook script paths exist
jq -r '.hooks | .[] | .[].hooks[].command' /path/to/my-plugin/hooks/hooks.json | while read cmd; do
  SCRIPT=$(echo "$cmd" | sed 's/\${CLAUDE_PLUGIN_ROOT}/\/path\/to\/my-plugin/')
  if [ -f "$SCRIPT" ]; then
    echo "OK: $SCRIPT exists"
  else
    echo "ERROR: $SCRIPT not found"
  fi
done
```

### Step 5: Validate Agents (If Present)

```bash
# Check agents field format in plugin.json
jq '.agents' /path/to/my-plugin/.claude-plugin/plugin.json
# Must be array of strings, each ending in .md

# Verify each agent file exists
jq -r '.agents[]' /path/to/my-plugin/.claude-plugin/plugin.json | while read agent; do
  if [ -f "/path/to/my-plugin/$agent" ]; then
    echo "OK: $agent exists"
  else
    echo "ERROR: $agent not found"
  fi
done
```

### Step 6: Validate Skills (If Present)

```bash
# Install skills-ref if not present
pip install skills-ref

# Validate each skill
for skill in /path/to/my-plugin/skills/*/; do
  skills-ref validate "$skill"
done
```

### Step 7: Test Load

```bash
# Launch with debug to see loading issues
claude --debug --plugin-dir /path/to/my-plugin 2>&1 | grep -i plugin

# Check hooks registered
/hooks
```

## Checklist

Copy this checklist and track your progress:

- [ ] Run claude plugin validate
- [ ] Validate plugin.json JSON syntax
- [ ] Verify required fields (name, version)
- [ ] Check components at ROOT (not in .claude-plugin/)
- [ ] Verify hooks.json syntax
- [ ] Check all hook script paths exist
- [ ] Verify scripts are executable
- [ ] Check agents array format (array of .md paths)
- [ ] Verify each agent file exists
- [ ] Validate skills with skills-ref
- [ ] Test load with --debug flag
- [ ] Verify hooks register correctly

## Examples

### Example: Complete Plugin Validation

```bash
PLUGIN_PATH="/path/to/my-plugin"

# Step 1: CLI validation
claude plugin validate $PLUGIN_PATH

# Step 2: JSON syntax
jq . $PLUGIN_PATH/.claude-plugin/plugin.json > /dev/null && echo "JSON OK" || echo "JSON ERROR"

# Step 3: Structure check
echo "=== Structure Check ==="
[ -d "$PLUGIN_PATH/.claude-plugin" ] && echo "OK: .claude-plugin/" || echo "MISSING: .claude-plugin/"
[ -f "$PLUGIN_PATH/.claude-plugin/plugin.json" ] && echo "OK: plugin.json" || echo "MISSING: plugin.json"
[ -d "$PLUGIN_PATH/commands" ] && echo "OK: commands/" || echo "INFO: no commands/"
[ -d "$PLUGIN_PATH/agents" ] && echo "OK: agents/" || echo "INFO: no agents/"
[ -d "$PLUGIN_PATH/hooks" ] && echo "OK: hooks/" || echo "INFO: no hooks/"

# Step 4: Scripts executable
echo "=== Scripts Check ==="
for script in $PLUGIN_PATH/scripts/*; do
  if [ -x "$script" ]; then
    echo "OK: $script is executable"
  else
    echo "FIX NEEDED: chmod +x $script"
  fi
done

# Step 5: Skills validation
echo "=== Skills Validation ==="
for skill in $PLUGIN_PATH/skills/*/; do
  skills-ref validate "$skill" 2>&1 | head -5
done

# Step 6: Test load
echo "=== Test Load ==="
echo "Run: claude --debug --plugin-dir $PLUGIN_PATH"
```

### Example: Common Validation Fix Commands

```bash
# Fix script permissions
chmod +x /path/to/my-plugin/scripts/*.sh
chmod +x /path/to/my-plugin/scripts/*.py

# Fix agents array (edit plugin.json)
# Change from:  "agents": "./agents/"
# Change to:    "agents": ["./agents/my-agent.md"]

# Fix JSON syntax (find error)
python -m json.tool /path/to/my-plugin/.claude-plugin/plugin.json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Invalid JSON | Syntax error in plugin.json | Use `jq .` to find error location |
| Missing required field | name or version absent | Add missing field to plugin.json |
| Path not found | Broken reference in manifest | Fix path or create missing file |
| Permission denied | Script not executable | `chmod +x` on the script |
| Components not loading | In wrong directory | Move to ROOT, not .claude-plugin/ |
| agents invalid | Not array of strings | Change to array: `["./agents/x.md"]` |
| Skill validation fails | SKILL.md format issue | Fix frontmatter or structure per skills-ref output |
| Hooks not firing | hooks.json syntax error | Validate with `jq .` |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Install after validation
- [op-configure-local-plugin.md](op-configure-local-plugin.md) - Local plugin setup
- [op-restart-agent-plugin.md](op-restart-agent-plugin.md) - Restart after fixes
