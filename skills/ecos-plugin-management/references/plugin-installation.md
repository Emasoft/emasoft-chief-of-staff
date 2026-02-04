# Plugin Installation Reference

## Table of Contents

- 1.1 What is plugin installation - Understanding plugin deployment
- 1.2 Installation prerequisites - Requirements before install
  - 1.2.1 Marketplace registration - Adding marketplaces
  - 1.2.2 Plugin discovery - Finding available plugins
  - 1.2.3 Version selection - Choosing plugin version
- 1.3 Installation procedure - Step-by-step installation
  - 1.3.1 Marketplace check - Verifying marketplace active
  - 1.3.2 Plugin availability - Confirming plugin exists
  - 1.3.3 Install command - Running installation
  - 1.3.4 Restart requirement - Restarting Claude Code
  - 1.3.5 Verification - Confirming installation success
- 1.4 Installation scopes - User, project, local, managed
- 1.5 Updating plugins - Upgrading to new versions
- 1.6 Uninstalling plugins - Removing plugins
- 1.7 Examples - Installation scenarios
- 1.8 Troubleshooting - Installation issues

---

## 1.1 What is plugin installation

Plugin installation is the process of adding a Claude Code plugin from a marketplace or local directory. Installation:

1. Downloads plugin files to cache
2. Registers plugin in settings
3. Enables plugin components (commands, agents, hooks)
4. Makes plugin available for use

---

## 1.2 Installation prerequisites

### 1.2.1 Marketplace registration

Before installing from a marketplace, register it:

```bash
# Add a marketplace
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins

# List registered marketplaces
claude plugin marketplace list

# Update marketplace cache
claude plugin marketplace update emasoft-plugins
```

### 1.2.2 Plugin discovery

Find available plugins:

```bash
# List plugins in marketplace
claude plugin search @emasoft-plugins

# Search for specific plugin
claude plugin search perfect-skill-suggester
```

### 1.2.3 Version selection

Plugins may have multiple versions:

```bash
# Install latest version (default)
claude plugin install perfect-skill-suggester@emasoft-plugins

# Install specific version
claude plugin install perfect-skill-suggester@emasoft-plugins:1.2.0
```

---

## 1.3 Installation procedure

### 1.3.1 Marketplace check

**Purpose:** Verify marketplace is registered and accessible.

```bash
# Check marketplace exists
claude plugin marketplace list | grep emasoft-plugins

# If not found, add it
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins
```

### 1.3.2 Plugin availability

**Purpose:** Confirm plugin exists in marketplace.

```bash
# Search for plugin
claude plugin search perfect-skill-suggester@emasoft-plugins

# Should return plugin info
```

### 1.3.3 Install command

**Purpose:** Execute the installation.

```bash
# Install with default scope (user)
claude plugin install perfect-skill-suggester@emasoft-plugins

# Install to specific scope
claude plugin install perfect-skill-suggester@emasoft-plugins --scope project
```

### 1.3.4 Restart requirement

**CRITICAL:** Claude Code must be restarted after installation.

```bash
# Exit Claude Code
# Relaunch Claude Code

# Or from within Claude Code
/exit
# Then relaunch
```

**Why restart is required:**
- Plugin hooks are cached at startup
- Command registry is built at startup
- Settings are loaded once at startup

### 1.3.5 Verification

**Purpose:** Confirm installation succeeded.

```bash
# List installed plugins
claude plugin list

# Check for specific plugin
claude plugin list | grep perfect-skill-suggester

# Test a plugin command (if applicable)
/pss-status
```

---

## 1.4 Installation scopes

| Scope | Settings File | Persists | Shared |
|-------|---------------|----------|--------|
| `user` | `~/.claude/settings.json` | Yes | Across all projects |
| `project` | `.claude/settings.json` | Yes | With team (via git) |
| `local` | `.claude/settings.local.json` | Yes | Not shared (gitignored) |
| `managed` | `managed-settings.json` | Yes | Enterprise managed |

**Choosing a scope:**
- `user`: Personal plugins for all projects
- `project`: Team plugins shared via version control
- `local`: Project-specific plugins not shared

---

## 1.5 Updating plugins

### Update to latest version

```bash
# Step 1: Update marketplace cache
claude plugin marketplace update emasoft-plugins

# Step 2: Uninstall current version
claude plugin uninstall perfect-skill-suggester@emasoft-plugins

# Step 3: Reinstall (gets latest)
claude plugin install perfect-skill-suggester@emasoft-plugins

# Step 4: RESTART Claude Code
```

### Clean update (if issues)

```bash
# Clear plugin cache
rm -rf ~/.claude/plugins/cache/emasoft-plugins/

# Reinstall
claude plugin uninstall perfect-skill-suggester@emasoft-plugins
claude plugin install perfect-skill-suggester@emasoft-plugins

# RESTART Claude Code
```

---

## 1.6 Uninstalling plugins

```bash
# Uninstall plugin
claude plugin uninstall perfect-skill-suggester@emasoft-plugins

# Verify removed
claude plugin list | grep perfect-skill-suggester
# Should return empty

# RESTART Claude Code
```

---

## 1.7 Examples

### Example 1: First-time Installation

```bash
# Complete installation flow

# 1. Add marketplace
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins

# 2. Install plugin
claude plugin install perfect-skill-suggester@emasoft-plugins

# 3. Verify
claude plugin list

# 4. EXIT and RELAUNCH Claude Code

# 5. Test plugin
/pss-status
```

### Example 2: Install for Project Team

```bash
# Install with project scope (shared via git)

# In project directory
claude plugin install perfect-skill-suggester@emasoft-plugins --scope project

# Commit settings
git add .claude/settings.json
git commit -m "Add perfect-skill-suggester plugin"
git push

# Team members: pull and restart Claude Code
```

### Example 3: Local Development Plugin

```bash
# Use --plugin-dir for local plugins (no install needed)

claude --plugin-dir /path/to/my-local-plugin

# Multiple local plugins
claude --plugin-dir /path/to/plugin-a --plugin-dir /path/to/plugin-b
```

---

## 1.8 Troubleshooting

### Issue: Marketplace not found

**Symptoms:** Cannot find marketplace error.

**Resolution:**
1. Check URL is correct
2. Verify repository is public or you have access
3. Check network connectivity
4. Try adding marketplace again

### Issue: Plugin install fails

**Symptoms:** Installation errors, plugin not in list.

**Resolution:**
1. Check plugin name is correct (case-sensitive)
2. Verify marketplace has the plugin
3. Update marketplace cache
4. Check for version compatibility

### Issue: Plugin not working after install

**Symptoms:** Commands not found, hooks not firing.

**Resolution:**
1. **RESTART Claude Code** (most common fix)
2. Verify plugin in list: `claude plugin list`
3. Check plugin validation: `claude plugin validate`
4. Look for error messages in debug mode

### Issue: Hook path version mismatch

**Symptoms:** Error about missing file with old version number.

```
can't open file '.../perfect-skill-suggester/1.2.1/scripts/pss_hook.py': No such file
```

**Resolution:**
1. This means session has old path cached
2. **RESTART Claude Code** to load new paths
3. If persists, clear plugin cache and reinstall

### Issue: Duplicate hooks error

**Symptoms:** Error about duplicate hook IDs.

**Resolution:**
1. Check for multiple installations of same plugin
2. Verify marketplace.json uses correct source format
3. Uninstall and reinstall cleanly
4. Clear cache if needed
