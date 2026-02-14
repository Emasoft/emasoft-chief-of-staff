# Plugin Validation Reference

## Table of Contents

- 3.1 What is plugin validation - Checking plugin correctness
- 3.2 Validation levels - What gets checked
  - 3.2.1 Manifest validation - plugin.json structure
  - 3.2.2 Component validation - commands, agents, skills
  - 3.2.3 Hook validation - hooks.json and scripts
  - 3.2.4 Path validation - File references
- 3.3 Validation procedure - Running validation
  - 3.3.1 CLI validation - claude plugin validate
  - 3.3.2 Script validation - Using validation scripts
  - 3.3.3 Manual inspection - Checking files directly
- 3.4 Common validation errors - Frequent issues
  - 3.4.1 Manifest errors - Missing fields, wrong types
  - 3.4.2 Path errors - Broken references
  - 3.4.3 Hook errors - Invalid hook configuration
  - 3.4.4 Permission errors - Script not executable
- 3.5 Fixing validation errors - Resolution procedures
- 3.6 Examples - Validation scenarios
- 3.7 Troubleshooting - Validation issues

---

## 3.1 What is plugin validation

Plugin validation is the process of checking that a plugin conforms to the required structure and specifications. Validation catches:

- Missing required files
- Invalid JSON/YAML syntax
- Broken file references
- Incorrect configurations

---

## 3.2 Validation levels

### 3.2.1 Manifest validation

Checks `.claude-plugin/plugin.json`:

| Check | Description |
|-------|-------------|
| File exists | plugin.json must exist |
| Valid JSON | Must parse without errors |
| Required fields | `name` must be present |
| Field types | Each field has correct type |
| Name format | Kebab-case, no spaces |

### 3.2.2 Component validation

Checks commands, agents, skills:

| Component | Checks |
|-----------|--------|
| Commands | YAML frontmatter valid, required fields |
| Agents | YAML frontmatter valid, required fields |
| Skills | SKILL.md exists, frontmatter valid |

### 3.2.3 Hook validation

Checks hooks/hooks.json:

| Check | Description |
|-------|-------------|
| Valid JSON | Must parse without errors |
| Hook structure | Correct nesting and fields |
| Matcher format | Valid regex patterns |
| Command paths | Scripts exist |

### 3.2.4 Path validation

Checks all file references:

| Check | Description |
|-------|-------------|
| Script paths | All referenced scripts exist |
| Relative paths | Correctly resolved |
| Permissions | Scripts are executable |

---

## 3.3 Validation procedure

### 3.3.1 CLI validation

```bash
# Validate installed plugin
claude plugin validate perfect-skill-suggester@emasoft-plugins

# Validate local plugin directory
claude plugin validate /path/to/my-plugin
```

### 3.3.2 Script validation

Many plugins include validation scripts:

```bash
# Using plugin's internal validator
cd /path/to/my-plugin
uv run python scripts/validate_plugin.py . --verbose

# With verbose output
uv run python scripts/validate_plugin.py . --verbose

# Output as JSON
uv run python scripts/validate_plugin.py . --json
```

### 3.3.3 Manual inspection

Check files directly:

```bash
# Verify plugin.json
cat .claude-plugin/plugin.json | jq .

# Verify hooks.json
cat hooks/hooks.json | jq .

# Check command frontmatter
head -20 commands/my-command.md

# Verify scripts executable
ls -la scripts/
```

---

## 3.4 Common validation errors

### 3.4.1 Manifest errors

**Missing name field:**
```
Error: plugin.json missing required field: name
```

**Fix:** Add name to plugin.json:
```json
{
  "name": "my-plugin"
}
```

**Invalid name format:**
```
Error: plugin name must be kebab-case: "My Plugin" -> "my-plugin"
```

**Fix:** Use kebab-case:
```json
{
  "name": "my-plugin"
}
```

### 3.4.2 Path errors

**Script not found:**
```
Error: Hook script not found: ${CLAUDE_PLUGIN_ROOT}/scripts/hook.py
```

**Fix:** Create the script or fix the path.

**Wrong path format:**
```
Error: Relative path not allowed in hooks: ./scripts/hook.py
```

**Fix:** Use ${CLAUDE_PLUGIN_ROOT}:
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook.py"
}
```

### 3.4.3 Hook errors

**Invalid JSON:**
```
Error: hooks.json parse error at line 15: Unexpected token
```

**Fix:** Correct JSON syntax.

**Invalid matcher:**
```
Error: Invalid matcher regex: [unclosed
```

**Fix:** Correct regex pattern.

### 3.4.4 Permission errors

**Script not executable:**
```
Error: Script not executable: scripts/hook.py
```

**Fix:**
```bash
chmod +x scripts/hook.py
```

---

## 3.5 Fixing validation errors

### General fix procedure

1. Run validation to see all errors
2. Fix errors in order (manifest first)
3. Re-run validation
4. Repeat until clean

### Manifest fixes

```bash
# Validate JSON syntax
cat .claude-plugin/plugin.json | jq .

# If parse error, use JSON linter
# Or recreate file carefully
```

### Hook fixes

```bash
# Validate hooks.json syntax
cat hooks/hooks.json | jq .

# Check all referenced scripts exist
jq -r '.. | .command? // empty' hooks/hooks.json | while read cmd; do
  script=$(echo "$cmd" | sed 's/\${CLAUDE_PLUGIN_ROOT}/./g')
  if [ ! -f "$script" ]; then
    echo "Missing: $script"
  fi
done
```

### Permission fixes

```bash
# Make all scripts executable
chmod +x scripts/*.py scripts/*.sh
```

---

## 3.6 Examples

### Example 1: Full Validation Run

```bash
$ claude plugin validate ./my-plugin

Validating plugin: my-plugin
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Manifest: OK
  ✓ plugin.json exists
  ✓ Valid JSON
  ✓ Name: my-plugin
  ✓ Version: 1.0.0

Commands: OK
  ✓ commands/hello.md - valid frontmatter
  ✓ commands/status.md - valid frontmatter

Agents: OK
  ✓ agents/helper.md - valid frontmatter

Hooks: OK
  ✓ hooks/hooks.json - valid structure
  ✓ All scripts exist and executable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Result: VALID (0 errors, 0 warnings)
```

### Example 2: Validation with Errors

```bash
$ claude plugin validate ./broken-plugin

Validating plugin: broken-plugin
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Manifest: ERROR
  ✗ Missing required field: name

Commands: WARNING
  ⚠ commands/test.md - missing description in frontmatter

Hooks: ERROR
  ✗ Script not found: scripts/missing.py
  ✗ Script not executable: scripts/hook.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Result: INVALID (3 errors, 1 warning)
```

### Example 3: Skill Validation

```bash
# Validate skills with skills-ref
pip install skills-ref

# Validate each skill
for skill in skills/*/; do
  echo "Validating $skill"
  skills-ref validate "$skill"
done
```

---

## 3.7 Troubleshooting

### Issue: Validation command not found

**Symptoms:** `claude plugin validate` returns error.

**Resolution:**
1. Ensure Claude Code CLI is installed
2. Check CLI version supports validation
3. Use internal validation script instead

### Issue: False positive errors

**Symptoms:** Validation reports error but plugin works.

**Resolution:**
1. Check if error is for optional component
2. Verify Claude Code version matches validator
3. Report as bug if genuinely false positive

### Issue: Validation hangs

**Symptoms:** Validation does not complete.

**Resolution:**
1. Check for very large files
2. Look for infinite loops in scripts
3. Try validating components individually
4. Check system resources

### Issue: Different results between validators

**Symptoms:** CLI says valid, script says invalid.

**Resolution:**
1. Check validator versions
2. One may have stricter checks
3. Fix all errors from both
4. Prefer more recent validator
