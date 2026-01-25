# Using Memory Scripts: Workflows, Examples, and Troubleshooting

## Table of Contents

1. [Common Workflows](#common-workflows)
   - [Daily Startup](#workflow-1-daily-startup)
   - [Before Compaction](#workflow-2-before-compaction)
   - [Weekly Maintenance](#workflow-3-weekly-maintenance)
   - [Emergency Recovery](#workflow-4-emergency-recovery)
2. [Implementation Examples](#examples)
3. [Troubleshooting](#troubleshooting)

---

## Common Workflows

### Workflow 1: Daily Startup

```bash
# 1. Validate memory
python scripts/validate-memory.py

# 2. Load into session
python scripts/load-memory.py

# 3. Begin work...
```

---

### Workflow 2: Before Compaction

```bash
# 1. Save current state
python scripts/save-memory.py --backup

# 2. Validate saved state
python scripts/validate-memory.py

# 3. Ready for compaction
```

---

### Workflow 3: Weekly Maintenance

```bash
# 1. Archive old content
python scripts/archive-memory.py --type all --cutoff-days 30

# 2. Validate after archival
python scripts/validate-memory.py --fix

# 3. Check file sizes
du -h .atlas/memory/*.md
```

---

### Workflow 4: Emergency Recovery

```bash
# 1. Assess damage
python scripts/validate-memory.py --verbose

# 2. Attempt repair
python scripts/repair-memory.py

# 3. If repair fails, reinitialize
python scripts/initialize-memory.py --force
```

---

## Examples

### Example: Integrating into Agent Workflow

```python
# In agent main loop

def initialize_session():
    """Load session memory at startup."""
    result = subprocess.run(
        ['python', 'scripts/load-memory.py', '--format', 'json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error loading memory:", result.stderr)
        # Attempt repair
        repair_memory()
        return initialize_session()  # Retry

    state = json.loads(result.stdout)
    return state

def save_session():
    """Save session memory before shutdown."""
    state_json = json.dumps(current_state)

    with open('/tmp/state.json', 'w') as f:
        f.write(state_json)

    result = subprocess.run(
        ['python', 'scripts/save-memory.py', '--state', '/tmp/state.json', '--backup'],
        capture_output=True
    )

    if result.returncode != 0:
        print("Error saving memory:", result.stderr)
        return False

    return True
```

---

## Troubleshooting

### Issue: Script fails with "module not found"

**Cause:** Missing Python dependencies

**Solution:**
```bash
pip install -r requirements.txt
# Or for scripts specifically:
pip install markdown pyyaml
```

---

### Issue: Permission denied

**Cause:** Scripts not executable

**Solution:**
```bash
chmod +x scripts/*.py
# Or run with python explicitly:
python scripts/validate-memory.py
```

---

### Issue: Script reports errors but files look OK

**Cause:** Script validation rules may be too strict

**Solution:**
1. Review reported errors manually
2. Use `--verbose` to understand what failed
3. Fix actual issues or adjust validation rules

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
