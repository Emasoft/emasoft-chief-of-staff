# Plugin Installation and Configuration Procedures

Complete procedural guide for installing, configuring, and managing Claude Code plugins locally for agents.

## Contents

- [1. Installing Plugins from Marketplaces](#1-installing-plugins-from-marketplaces)
  - [1.1 Adding a marketplace](#11-adding-a-marketplace)
  - [1.2 Installing a plugin with local scope](#12-installing-a-plugin-with-local-scope)
  - [1.3 Verifying plugin installation](#13-verifying-plugin-installation)
- [2. Installing Plugins from Local Directories](#2-installing-plugins-from-local-directories)
  - [2.1 Using the --plugin-dir flag](#21-using-the---plugin-dir-flag)
  - [2.2 When to use local directory loading](#22-when-to-use-local-directory-loading)
- [3. Understanding and Managing Plugin Scopes](#3-understanding-and-managing-plugin-scopes)
  - [3.1 The four scope types](#31-the-four-scope-types)
  - [3.2 Choosing the right scope for your use case](#32-choosing-the-right-scope-for-your-use-case)
  - [3.3 Plugin cache locations](#33-plugin-cache-locations)
- [4. Configuring Plugin Settings Files](#4-configuring-plugin-settings-files)
  - [4.1 Creating settings.local.json for project-specific configuration](#41-creating-settingslocaljson-for-project-specific-configuration)
  - [4.2 Understanding settings file hierarchy](#42-understanding-settings-file-hierarchy)
  - [4.3 Adding plugins to enabled list](#43-adding-plugins-to-enabled-list)
- [5. Enabling and Disabling Plugins](#5-enabling-and-disabling-plugins)
  - [5.1 Enabling a plugin](#51-enabling-a-plugin)
  - [5.2 Disabling a plugin](#52-disabling-a-plugin)
  - [5.3 Temporarily disabling vs uninstalling](#53-temporarily-disabling-vs-uninstalling)
- [6. Updating Plugins to Latest Versions](#6-updating-plugins-to-latest-versions)
  - [6.1 Standard update procedure](#61-standard-update-procedure)
  - [6.2 Clean reinstall when updates fail](#62-clean-reinstall-when-updates-fail)
  - [6.3 Updating marketplace cache](#63-updating-marketplace-cache)
- [7. Uninstalling Plugins](#7-uninstalling-plugins)
  - [7.1 Basic uninstallation](#71-basic-uninstallation)
  - [7.2 Removing plugin cache manually](#72-removing-plugin-cache-manually)
- [8. Validating Plugin Installations](#8-validating-plugin-installations)
  - [8.1 Running plugin validation](#81-running-plugin-validation)
  - [8.2 Verifying plugin health checklist](#82-verifying-plugin-health-checklist)
  - [8.3 Checking plugin versions](#83-checking-plugin-versions)
- [9. Troubleshooting Duplicate Hook Errors](#9-troubleshooting-duplicate-hook-errors)
  - [9.1 Identifying stale cache issues](#91-identifying-stale-cache-issues)
  - [9.2 Clearing duplicate version caches](#92-clearing-duplicate-version-caches)
- [10. Troubleshooting Version Update Issues](#10-troubleshooting-version-update-issues)
  - [10.1 Hook path contains old version number](#101-hook-path-contains-old-version-number)
  - [10.2 Plugin list shows wrong version](#102-plugin-list-shows-wrong-version)
  - [10.3 Marketplace.json source format issues](#103-marketplacejson-source-format-issues)
- [11. Notifying Agents After Configuration Changes](#11-notifying-agents-after-configuration-changes)
  - [11.1 Why restart is required](#111-why-restart-is-required)
  - [11.2 Sending restart notification via AI Maestro](#112-sending-restart-notification-via-ai-maestro)

---

## 1. Installing Plugins from Marketplaces

### 1.1 Adding a marketplace

Before installing plugins from a marketplace, you must first register the marketplace URL with Claude Code.

**Procedure:**

```bash
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins
```

**Expected Output:**
```
Marketplace added successfully: emasoft-plugins
```

**Verification:**
```bash
claude plugin marketplace list
```

Should show the newly added marketplace in the list.

**Common Issues:**
- **Invalid URL**: Ensure the URL points to a valid git repository with a `marketplace.json` file
- **Network errors**: Check internet connectivity and proxy settings

---

### 1.2 Installing a plugin with local scope

Once a marketplace is added, install plugins using the `--scope local` flag for project-specific installations.

**Procedure:**

```bash
claude plugin install <plugin-name>@<marketplace-name> --scope local
```

**Example:**

```bash
claude plugin install perfect-skill-suggester@emasoft-plugins --scope local
```

**What happens:**
1. Claude Code downloads the plugin from the marketplace repository
2. Caches it in `~/.claude/plugins/cache/<marketplace-name>/<plugin-name>/<version>/`
3. Adds the plugin to `.claude/settings.local.json` in the current project
4. Enables the plugin for the current project only

**Expected Output:**
```
Installing perfect-skill-suggester@emasoft-plugins...
Downloaded version 1.2.2
Plugin installed successfully (scope: local)
```

**Important Notes:**
- The `--scope local` flag ensures the plugin is only enabled for this project
- The `.claude/settings.local.json` file is gitignored by default
- Other scope options: `user`, `project`, `managed` (see section 3)

---

### 1.3 Verifying plugin installation

After installation, verify the plugin is properly installed and enabled.

**Procedure:**

```bash
# List all installed plugins
claude plugin list

# Filter for specific plugin
claude plugin list | grep <plugin-name>
```

**Expected Output:**

```
perfect-skill-suggester@emasoft-plugins (enabled, v1.2.2, scope: local)
```

**Verification Checklist:**
- [ ] Plugin appears in the list
- [ ] Status shows "enabled"
- [ ] Correct version is displayed
- [ ] Scope matches what was specified during installation

**If Plugin Not Listed:**
- Check that marketplace is added: `claude plugin marketplace list`
- Verify internet connectivity (if remote marketplace)
- Try running installation command again with `--verbose` flag
- Check `.claude/settings.local.json` for the plugin entry

---

## 2. Installing Plugins from Local Directories

### 2.1 Using the --plugin-dir flag

For development or when plugins are not available in a marketplace, load plugins directly from a local directory.

**Procedure:**

```bash
claude --plugin-dir /path/to/local/plugin
```

**Example:**

```bash
claude --plugin-dir /Users/dev/my-plugins/perfect-skill-suggester
```

**Multiple Plugins:**

```bash
claude --plugin-dir /path/to/plugin-one --plugin-dir /path/to/plugin-two
```

**What happens:**
1. Claude Code loads the plugin directly from the specified directory
2. No caching occurs
3. No entry is added to settings files
4. Plugin is only active for this Claude Code session

**Important Notes:**
- The plugin directory must contain a valid `.claude-plugin/plugin.json` file
- Changes to the plugin require restarting Claude Code
- This method is preferred for plugin development and testing

---

### 2.2 When to use local directory loading

**Use `--plugin-dir` when:**
- Developing a new plugin
- Testing plugin changes before publishing
- Using private/proprietary plugins not in a marketplace
- Working with unstable/experimental plugin versions
- Need rapid iteration without cache invalidation

**Use marketplace installation when:**
- Plugin is stable and published
- Need consistent versions across team members
- Want automatic updates
- Plugin is used by multiple projects

---

## 3. Understanding and Managing Plugin Scopes

### 3.1 The four scope types

Plugin scope determines where the plugin configuration is stored and who can access it.

| Scope | Settings File | Use Case | Shared? |
|-------|---------------|----------|---------|
| `user` | `~/.claude/settings.json` | Personal plugins for all projects | No (user-specific) |
| `project` | `.claude/settings.json` | Team plugins via version control | Yes (committed to repo) |
| `local` | `.claude/settings.local.json` | Project-specific, not shared | No (gitignored) |
| `managed` | `managed-settings.json` | Enterprise-managed (read-only) | Yes (IT-controlled) |

---

### 3.2 Choosing the right scope for your use case

**Use `--scope local` when:**
- Configuring plugins for a specific agent's project
- Testing plugins before team-wide adoption
- Using plugins with personal API keys or credentials
- Different agents need different plugin configurations

**Use `--scope project` when:**
- All team members should use the same plugins
- Plugin configuration should be version-controlled
- Consistent development environment is required

**Use `--scope user` when:**
- Plugin is for personal productivity (not project-specific)
- You want the plugin available in all projects
- Plugin doesn't affect team collaboration

---

### 3.3 Plugin cache locations

**Cache Directory Structure:**

```
~/.claude/plugins/cache/
├── <marketplace-name>/
│   ├── <plugin-name>/
│   │   ├── <version>/
│   │   │   ├── .claude-plugin/
│   │   │   ├── commands/
│   │   │   ├── agents/
│   │   │   ├── skills/
│   │   │   └── hooks/
```

**Example:**

```
~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.2/
```

**Important Notes:**
- Each version is cached separately
- Stale versions can cause "duplicate hooks" errors
- Cache can be manually cleared if issues occur
- Cache is automatically updated when marketplace is updated

---

## 4. Configuring Plugin Settings Files

### 4.1 Creating settings.local.json for project-specific configuration

When installing a plugin with `--scope local`, Claude Code creates or updates `.claude/settings.local.json`.

**Manual Creation Procedure:**

1. Navigate to project root directory
2. Create `.claude/` directory if it doesn't exist:
   ```bash
   mkdir -p .claude
   ```
3. Create `settings.local.json`:
   ```bash
   touch .claude/settings.local.json
   ```
4. Add JSON structure:

```json
{
  "$schema": "https://claude.ai/schemas/settings.json",
  "plugins": {
    "enabled": [
      "plugin-a@marketplace-name",
      "plugin-b@marketplace-name"
    ],
    "disabled": []
  }
}
```

**Important Notes:**
- Plugin identifiers use format: `<plugin-name>@<marketplace-name>`
- The `$schema` field enables IDE validation and autocomplete
- Empty `disabled` array can be omitted
- File should be added to `.gitignore`

---

### 4.2 Understanding settings file hierarchy

Claude Code merges settings from multiple files in priority order:

**Priority (highest to lowest):**

1. `managed-settings.json` (Enterprise-managed, read-only)
2. `.claude/settings.local.json` (Local project, gitignored)
3. `.claude/settings.json` (Shared project, version-controlled)
4. `~/.claude/settings.json` (User global)

**Merge Behavior:**
- `enabled` lists are merged (union)
- `disabled` lists are merged (union)
- Later sources can override earlier sources
- Disabled plugins take precedence over enabled

---

### 4.3 Adding plugins to enabled list

**Manual Procedure:**

1. Open `.claude/settings.local.json`
2. Locate the `plugins.enabled` array
3. Add plugin identifier:

```json
{
  "plugins": {
    "enabled": [
      "existing-plugin@marketplace",
      "new-plugin@marketplace"  // Add this line
    ]
  }
}
```

4. Save file
5. Restart Claude Code

**Important Notes:**
- Order in the array doesn't matter
- Duplicate entries are ignored
- Invalid plugin identifiers will cause errors on startup
- Always use format: `<plugin-name>@<marketplace-name>`

---

## 5. Enabling and Disabling Plugins

### 5.1 Enabling a plugin

Enable a previously disabled or newly installed plugin.

**Procedure:**

```bash
claude plugin enable <plugin-name>@<marketplace-name> --scope local
```

**Example:**

```bash
claude plugin enable perfect-skill-suggester@emasoft-plugins --scope local
```

**What happens:**
1. Plugin identifier is added to `enabled` list in settings file
2. Plugin identifier is removed from `disabled` list (if present)
3. Changes take effect on next Claude Code restart

**Expected Output:**
```
Plugin enabled: perfect-skill-suggester@emasoft-plugins (scope: local)
Restart Claude Code to apply changes.
```

---

### 5.2 Disabling a plugin

Disable a plugin without uninstalling it.

**Procedure:**

```bash
claude plugin disable <plugin-name>@<marketplace-name> --scope local
```

**Example:**

```bash
claude plugin disable perfect-skill-suggester@emasoft-plugins --scope local
```

**What happens:**
1. Plugin identifier is added to `disabled` list in settings file
2. Plugin identifier is removed from `enabled` list (if present)
3. Plugin remains cached but won't load on restart

**Expected Output:**
```
Plugin disabled: perfect-skill-suggester@emasoft-plugins (scope: local)
Restart Claude Code to apply changes.
```

---

### 5.3 Temporarily disabling vs uninstalling

**Disable When:**
- You want to test without the plugin temporarily
- Plugin causes issues but you'll need it later
- Different projects need different plugin configurations

**Uninstall When:**
- You no longer need the plugin at all
- Freeing up disk space
- Removing deprecated/obsolete plugins
- Switching to a different plugin marketplace

**Key Difference:**
- Disable: Plugin cache remains, can re-enable instantly
- Uninstall: Plugin cache deleted, requires re-download to use again

---

## 6. Updating Plugins to Latest Versions

### 6.1 Standard update procedure

**Procedure:**

```bash
# Step 1: Update marketplace cache
claude plugin marketplace update <marketplace-name>

# Step 2: Uninstall current version
claude plugin uninstall <plugin-name>@<marketplace-name>

# Step 3: Reinstall (gets latest version)
claude plugin install <plugin-name>@<marketplace-name> --scope local

# Step 4: Verify new version
claude plugin list | grep <plugin-name>

# Step 5: RESTART Claude Code (required!)
```

**Example:**

```bash
claude plugin marketplace update emasoft-plugins
claude plugin uninstall perfect-skill-suggester@emasoft-plugins
claude plugin install perfect-skill-suggester@emasoft-plugins --scope local
claude plugin list | grep perfect-skill-suggester
```

**Expected Output:**
```
Marketplace updated: emasoft-plugins
Plugin uninstalled: perfect-skill-suggester@emasoft-plugins
Installing perfect-skill-suggester@emasoft-plugins...
Downloaded version 1.2.3
Plugin installed successfully (scope: local)

perfect-skill-suggester@emasoft-plugins (enabled, v1.2.3, scope: local)
```

**Critical Notes:**
- ALWAYS restart Claude Code after updating
- Old version cache may remain (see section 6.2 for cleanup)
- Running session will have old hook paths cached in memory

---

### 6.2 Clean reinstall when updates fail

If standard update procedure doesn't work (plugin still shows old version), perform a clean reinstall.

**Procedure:**

```bash
# Step 1: Clear marketplace cache completely
rm -rf ~/.claude/plugins/cache/<marketplace-name>/

# Step 2: Uninstall plugin
claude plugin uninstall <plugin-name>@<marketplace-name>

# Step 3: Reinstall
claude plugin install <plugin-name>@<marketplace-name> --scope local

# Step 4: Verify new version
claude plugin list | grep <plugin-name>

# Step 5: RESTART Claude Code (required!)
```

**Example:**

```bash
rm -rf ~/.claude/plugins/cache/emasoft-plugins/
claude plugin uninstall perfect-skill-suggester@emasoft-plugins
claude plugin install perfect-skill-suggester@emasoft-plugins --scope local
claude plugin list | grep perfect-skill-suggester
```

**When to Use:**
- Standard update shows old version
- "Duplicate hooks" errors after update
- Hook paths reference old version numbers
- Plugin behavior doesn't match latest release

---

### 6.3 Updating marketplace cache

Marketplace cache stores metadata about available plugins and versions.

**Procedure:**

```bash
# Update specific marketplace
claude plugin marketplace update <marketplace-name>

# Update all marketplaces
claude plugin marketplace update --all
```

**Example:**

```bash
claude plugin marketplace update emasoft-plugins
```

**What happens:**
1. Claude Code fetches latest `marketplace.json` from repository
2. Updates local cache of available plugins and versions
3. Does NOT automatically update installed plugins (requires manual reinstall)

**Expected Output:**
```
Updating marketplace: emasoft-plugins
Fetched latest metadata
Marketplace updated successfully
```

**Important Notes:**
- This only updates the marketplace catalog
- Installed plugins remain at their current versions
- Run this before checking for plugin updates

---

## 7. Uninstalling Plugins

### 7.1 Basic uninstallation

Remove a plugin from the current project.

**Procedure:**

```bash
claude plugin uninstall <plugin-name>@<marketplace-name>
```

**Example:**

```bash
claude plugin uninstall perfect-skill-suggester@emasoft-plugins
```

**What happens:**
1. Plugin is removed from enabled/disabled lists in settings files
2. Plugin cache MAY be deleted (depends on scope and usage)
3. If plugin is used in other projects/scopes, cache remains

**Expected Output:**
```
Plugin uninstalled: perfect-skill-suggester@emasoft-plugins
Restart Claude Code to apply changes.
```

**Important Notes:**
- Uninstallation respects the scope where plugin was installed
- Other projects using the same plugin are unaffected
- Cache cleanup is automatic (usually)

---

### 7.2 Removing plugin cache manually

Force-remove plugin cache for troubleshooting or disk space recovery.

**Procedure:**

```bash
# Remove specific plugin version
rm -rf ~/.claude/plugins/cache/<marketplace-name>/<plugin-name>/<version>/

# Remove all versions of a plugin
rm -rf ~/.claude/plugins/cache/<marketplace-name>/<plugin-name>/

# Remove entire marketplace cache
rm -rf ~/.claude/plugins/cache/<marketplace-name>/
```

**Example:**

```bash
# Remove specific version
rm -rf ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.2/

# Remove all versions
rm -rf ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/
```

**When to Use:**
- Plugin uninstall failed
- "Duplicate hooks" errors persist
- Reclaiming disk space
- Troubleshooting corrupt cache

**Warning:**
- Manual removal doesn't update settings files
- Plugin will fail to load if still enabled in settings
- May need to reinstall if you want to use plugin again

---

## 8. Validating Plugin Installations

### 8.1 Running plugin validation

Verify plugin structure and configuration are correct.

**Procedure:**

```bash
# Validate installed plugin (from cache)
claude plugin validate ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/

# Validate local plugin directory
claude plugin validate /path/to/local/plugin
```

**Example:**

```bash
claude plugin validate ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.2/
```

**What it checks:**
- `plugin.json` structure and required fields
- Directory structure (commands/, agents/, skills/, hooks/)
- Hook configuration file exists and is valid JSON
- Agent and command file paths are correct
- Path traversal issues

**Expected Output:**
```
Validating plugin at: ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.2/
✓ plugin.json is valid
✓ Directory structure is correct
✓ Hook configuration is valid
✓ Agent files found: 2
✓ Command files found: 3
✓ No path traversal issues

Plugin validation passed.
```

---

### 8.2 Verifying plugin health checklist

**Complete Verification Procedure:**

1. **Check plugin appears in list:**
   ```bash
   claude plugin list | grep <plugin-name>
   ```
   - Status should be "enabled"
   - Version should match expected

2. **Verify correct version:**
   ```bash
   claude plugin list | grep <plugin-name>
   ```
   - Compare version with marketplace or plugin.json

3. **Test plugin commands are available:**
   ```bash
   # In Claude Code chat
   /help
   ```
   - Look for plugin-specific commands

4. **Check hooks are registered:**
   ```bash
   # In Claude Code chat
   /hooks
   ```
   - Plugin hooks should appear in list
   - No duplicate hook errors

5. **Verify no errors in logs:**
   - Check Claude Code startup logs for plugin loading errors
   - No "duplicate hooks" warnings
   - No "hook script not found" errors

---

### 8.3 Checking plugin versions

**Check Installed Version:**

```bash
claude plugin list | grep <plugin-name>
```

**Check Latest Available Version:**

```bash
# Update marketplace cache first
claude plugin marketplace update <marketplace-name>

# Check marketplace metadata
cat ~/.claude/plugins/cache/<marketplace-name>/marketplace.json | jq '.plugins."<plugin-name>".version'
```

**Check Plugin Manifest Version:**

```bash
cat ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/.claude-plugin/plugin.json | jq '.version'
```

**Example:**

```bash
# Installed version
claude plugin list | grep perfect-skill-suggester
# Output: perfect-skill-suggester@emasoft-plugins (enabled, v1.2.2, scope: local)

# Latest available
cat ~/.claude/plugins/cache/emasoft-plugins/marketplace.json | jq '.plugins."perfect-skill-suggester".version'
# Output: "1.2.3"
```

---

## 9. Troubleshooting Duplicate Hook Errors

### 9.1 Identifying stale cache issues

**Symptom:**

```
Error: Duplicate hook registered: PreToolUse:Write
Plugin: perfect-skill-suggester
```

**Root Cause:**

Multiple versions of the same plugin are cached, each registering the same hooks.

**Diagnosis Procedure:**

```bash
# List all cached versions
ls ~/.claude/plugins/cache/<marketplace-name>/<plugin-name>/
```

**Example:**

```bash
ls ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/
# Output: 1.2.1/ 1.2.2/
```

If more than one version directory exists, you have stale cache.

---

### 9.2 Clearing duplicate version caches

**Procedure:**

```bash
# Step 1: Identify current version
claude plugin list | grep <plugin-name>
# Note the version (e.g., 1.2.2)

# Step 2: List all cached versions
ls ~/.claude/plugins/cache/<marketplace>/<plugin>/

# Step 3: Remove old versions
rm -rf ~/.claude/plugins/cache/<marketplace>/<plugin>/<old-version>/

# Step 4: Verify only current version remains
ls ~/.claude/plugins/cache/<marketplace>/<plugin>/

# Step 5: RESTART Claude Code
```

**Example:**

```bash
# Current version is 1.2.2
claude plugin list | grep perfect-skill-suggester
# Output: perfect-skill-suggester@emasoft-plugins (enabled, v1.2.2, scope: local)

# Check cached versions
ls ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/
# Output: 1.2.1/ 1.2.2/

# Remove old version
rm -rf ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.1/

# Verify cleanup
ls ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/
# Output: 1.2.2/

# Restart Claude Code (required!)
```

**Important Notes:**
- Always keep the version matching `claude plugin list`
- Remove ALL other versions
- Restart is mandatory for changes to take effect

---

## 10. Troubleshooting Version Update Issues

### 10.1 Hook path contains old version number

**Symptom:**

After updating from 1.2.1 to 1.2.2:

```
PreToolUse:Write operation blocked by hook:
can't open file '~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/1.2.1/scripts/hook.py': No such file or directory
```

**Root Cause:**

The running Claude Code session has cached the hook paths with the old version number in memory. Even though the new cache directory exists at `1.2.2/`, the process still references `1.2.1/`.

**Solution:**

```bash
# RESTART Claude Code session (only solution!)
```

**Why Restart is Required:**
- Hook paths are cached in memory when Claude Code starts
- Updating a plugin creates new cache directory with new version number
- Running process doesn't dynamically update cached paths
- Memory has `1.2.1`, disk has `1.2.2`
- Restart loads fresh paths from disk

**Prevention:**
- ALWAYS restart Claude Code after plugin updates
- Document restart requirement in agent notifications
- Use AI Maestro to notify agents about required restarts

---

### 10.2 Plugin list shows wrong version

**Symptom:**

After update, `claude plugin list` still shows old version:

```bash
claude plugin list | grep perfect-skill-suggester
# Output: perfect-skill-suggester@emasoft-plugins (enabled, v1.2.1, scope: local)
```

But marketplace shows version 1.2.2 is available.

**Diagnosis:**

```bash
# Check what's actually cached
ls ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/
# Output: 1.2.1/ 1.2.2/

# Check settings file
cat .claude/settings.local.json | jq '.plugins.enabled'
# Output: ["perfect-skill-suggester@emasoft-plugins"]
```

**Solution:**

```bash
# Step 1: Clear entire plugin cache
rm -rf ~/.claude/plugins/cache/emasoft-plugins/perfect-skill-suggester/

# Step 2: Update marketplace
claude plugin marketplace update emasoft-plugins

# Step 3: Reinstall
claude plugin install perfect-skill-suggester@emasoft-plugins --scope local

# Step 4: Verify
claude plugin list | grep perfect-skill-suggester

# Step 5: RESTART Claude Code
```

---

### 10.3 Marketplace.json source format issues

**Symptom:**

```
Error: Duplicate hooks detected when merging plugin hooks
```

Or:

```
Error: Invalid plugin source format in marketplace.json
```

**Root Cause:**

The `marketplace.json` uses wrong format for the `source` field.

**Local Submodule Marketplaces (CORRECT):**

```json
{
  "plugins": {
    "perfect-skill-suggester": {
      "version": "1.2.2",
      "description": "...",
      "source": "./perfect-skill-suggester"
    }
  }
}
```

**Remote Marketplaces (CORRECT):**

```json
{
  "plugins": {
    "my-plugin": {
      "version": "1.0.0",
      "source": {
        "type": "git",
        "repository": "https://github.com/user/plugin.git"
      }
    }
  }
}
```

**WRONG (causes duplicate hooks):**

```json
{
  "plugins": {
    "perfect-skill-suggester": {
      "version": "1.2.2",
      "source": {
        "type": "local",
        "path": "./perfect-skill-suggester"
      }
    }
  }
}
```

**Solution:**

For local submodule-based marketplaces, use STRING path:
```json
"source": "./perfect-skill-suggester"
```

NOT object format.

---

## 11. Notifying Agents After Configuration Changes

### 11.1 Why restart is required

**Critical Understanding:**

Claude Code does NOT hot-reload plugins. All plugin configuration changes require a full restart.

**What gets cached in memory:**
- Hook registration and paths (with version numbers)
- Command definitions
- Agent definitions
- Skill locations
- Plugin settings

**What changes require restart:**
- Installing new plugins
- Updating plugins
- Enabling/disabling plugins
- Uninstalling plugins
- Modifying plugin settings files
- Clearing plugin cache

**Without restart:**
- Old hook paths remain active (causing "file not found" errors)
- New commands won't be available
- Disabled plugins will still run
- Updated plugin code won't load

---

### 11.2 Sending restart notification via AI Maestro

After configuring plugins for an agent, send a restart notification via AI Maestro.

**Procedure:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<agent-session-name>",
    "subject": "Plugin Configuration Changed - Restart Required",
    "priority": "high",
    "content": {
      "type": "notification",
      "message": "Plugin configuration updated. Please restart your Claude Code session to apply changes."
    }
  }'
```

**Example:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Plugin Configuration Changed - Restart Required",
    "priority": "high",
    "content": {
      "type": "notification",
      "message": "perfect-skill-suggester plugin installed (v1.2.2). Please restart Claude Code session."
    }
  }'
```

**Message Content Template:**

```json
{
  "to": "<agent-name>",
  "subject": "Plugin Configuration Changed - Restart Required",
  "priority": "high",
  "content": {
    "type": "notification",
    "message": "<plugin-name> <action> (v<version>). Restart Claude Code to apply changes. Changes: <list of changes>"
  }
}
```

**Important Notes:**
- Always use `priority: "high"` for restart notifications
- Include specific plugin name and version in message
- List what changed (installed, updated, disabled, etc.)
- Agent must manually restart - no automation possible
- Verify restart via AI Maestro follow-up message

---

## Error Reference Table

| Error | Cause | Solution | Section |
|-------|-------|----------|---------|
| Plugin not found | Marketplace not added | Run `claude plugin marketplace add <url>` | 1.1 |
| Duplicate hooks | Stale cache with multiple versions | Remove old version caches, restart | 9.2 |
| Hook path version mismatch | Session has old version cached in memory | Restart Claude Code session | 10.1 |
| Permission denied | Invalid scope or no write access | Check scope flag, verify write access | 3.1 |
| Invalid marketplace.json | Wrong source format | Use string for local submodules | 10.3 |
| Plugin shows old version | Update didn't clear old cache | Clear cache, reinstall plugin | 6.2, 10.2 |
| Commands not available | Plugin not enabled or not restarted | Enable plugin, restart session | 5.1, 11.1 |
| Hooks not firing | Plugin not registered in settings | Add to enabled list, restart | 4.3 |

---

**End of Installation Procedures Reference**
