---
operation: install-plugin-marketplace
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Install Plugin from Marketplace


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Check Marketplace Registration](#step-1-check-marketplace-registration)
  - [Step 2: Check Plugin Availability](#step-2-check-plugin-availability)
  - [Step 3: Install Plugin](#step-3-install-plugin)
  - [Step 4: Verify Installation](#step-4-verify-installation)
  - [Step 5: RESTART Claude Code](#step-5-restart-claude-code)
  - [Step 6: Verify Plugin Loaded](#step-6-verify-plugin-loaded)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Installing Perfect Skill Suggester](#example-installing-perfect-skill-suggester)
  - [Example: Installing Orchestrator Agent Plugin](#example-installing-orchestrator-agent-plugin)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Setting up a new agent that requires a plugin
- Adding new capabilities to an existing agent
- Installing required plugins before team creation
- Updating to a new plugin version

## Prerequisites

- Claude Code CLI is available
- Marketplace is registered (or will be added)
- Network access to marketplace repository
- Write permissions to plugin cache directory

## Procedure

### Step 1: Check Marketplace Registration

```bash
# List registered marketplaces
claude plugin marketplace list

# If marketplace not registered, add it
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins
```

### Step 2: Check Plugin Availability

```bash
# Update marketplace cache
claude plugin marketplace update emasoft-plugins

# List available plugins
claude plugin search <plugin-name>
```

### Step 3: Install Plugin

```bash
# Install from marketplace
claude plugin install <plugin-name>@<marketplace-name>

# Example
claude plugin install emasoft-orchestrator-agent@emasoft-plugins
```

### Step 4: Verify Installation

```bash
# List installed plugins
claude plugin list | grep <plugin-name>

# Check plugin details
claude plugin info <plugin-name>
```

### Step 5: RESTART Claude Code

**CRITICAL**: Plugin changes require Claude Code restart to take effect.

```bash
# Exit current session
exit

# Relaunch Claude Code
claude
```

### Step 6: Verify Plugin Loaded

After restart:

```bash
# Check hooks are registered
/hooks

# Check commands are available
/<plugin-command>
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify marketplace is registered
- [ ] Update marketplace cache
- [ ] Confirm plugin exists in marketplace
- [ ] Run install command
- [ ] Verify installation completed without errors
- [ ] Exit Claude Code session
- [ ] Relaunch Claude Code
- [ ] Verify hooks are registered
- [ ] Verify commands are available
- [ ] Test basic plugin functionality

## Examples

### Example: Installing Perfect Skill Suggester

```bash
# Step 1: Add marketplace (first time only)
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins

# Step 2: Update cache
claude plugin marketplace update emasoft-plugins

# Step 3: Install
claude plugin install perfect-skill-suggester@emasoft-plugins

# Step 4: Verify
claude plugin list | grep perfect-skill-suggester
# Output: perfect-skill-suggester@emasoft-plugins 1.2.3 enabled

# Step 5: RESTART Claude Code
exit

# Step 6: After restart, verify
/hooks
# Should show pss-related hooks

/pss-suggest
# Should work
```

### Example: Installing Orchestrator Agent Plugin

```bash
# Install
claude plugin install emasoft-orchestrator-agent@emasoft-plugins

# Verify
claude plugin list | grep emasoft-orchestrator-agent

# RESTART required
exit

# After restart - test
/hooks
# Should show eoa-related hooks
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Marketplace not found | Not registered | Run `claude plugin marketplace add <url>` |
| Plugin not found | Wrong name or not in marketplace | Check exact plugin name in marketplace |
| Download failed | Network issue | Check internet, retry |
| Permission denied | Cache directory not writable | Check permissions on `~/.claude/plugins/cache/` |
| Version conflict | Multiple versions cached | Run `claude plugin marketplace update` to refresh |
| Hooks not firing after install | Forgot to restart | Exit and relaunch Claude Code |

## Related Operations

- [op-configure-local-plugin.md](op-configure-local-plugin.md) - Local plugin setup
- [op-validate-plugin.md](op-validate-plugin.md) - Validate plugin structure
- [op-install-plugin-remote.md](op-install-plugin-remote.md) - Install on remote agents
- [op-restart-agent-plugin.md](op-restart-agent-plugin.md) - Restart after install
