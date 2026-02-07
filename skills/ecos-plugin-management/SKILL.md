---
name: ecos-plugin-management
description: Use when installing, configuring, or validating Claude Code plugins. Trigger with plugin install, update, or validation requests.
license: Apache-2.0
compatibility: Requires access to Claude Code CLI, plugin directories, and understanding of plugin manifest format and hooks configuration. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "Step 4"
procedure: "proc-create-team"
---

# Emasoft Chief of Staff - Plugin Management Skill

## Overview

Plugin management enables the Chief of Staff to install, configure, and maintain Claude Code plugins across projects. This skill teaches you how to install plugins from marketplaces, configure local plugin directories, manage plugin settings, and validate plugin installations.

## Prerequisites

Before using this skill, ensure:
1. Plugin validation scripts are available
2. Plugin directories are accessible
3. Agent restart capability is available

## Instructions

1. Identify plugin operation needed (install, update, validate)
2. Execute the operation
3. Verify plugin integrity
4. Restart affected agents if needed

## Output

| Operation | Output |
|-----------|--------|
| Install | Plugin installed, agents restarted |
| Update | Plugin updated, version logged |
| Validate | Validation report generated |

## What Is Plugin Management?

Plugin management is the administration of Claude Code extensions that add commands, agents, skills, hooks, and MCP servers. It includes:

- **Installation**: Adding plugins from marketplaces or local directories
- **Configuration**: Setting plugin options and scope
- **Local management**: Working with development plugins
- **Validation**: Ensuring plugins are correctly structured

## Plugin Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  AVAILABLE  │───►│  INSTALLED  │───►│   ENABLED   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       │                  ▼                  ▼
       │           ┌─────────────┐    ┌─────────────┐
       └──────────►│   CACHED    │    │  DISABLED   │
                   └─────────────┘    └─────────────┘
```

## Core Procedures

### PROCEDURE 1: Install Plugin from Marketplace

**When to use:** When adding a new plugin that is available from a registered marketplace.

**Steps:** Check marketplace registration, verify plugin exists, run install command, restart Claude Code, verify installation.

**Related documentation:**

#### Plugin Installation ([references/plugin-installation.md](references/plugin-installation.md))
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

### PROCEDURE 2: Configure Local Plugin Directory

**When to use:** When developing plugins locally, testing plugin changes, or using plugins not in marketplaces.

**Steps:** Create plugin directory structure, add plugin.json manifest, configure components, launch with --plugin-dir flag.

**Related documentation:**

#### Local Configuration ([references/local-configuration.md](references/local-configuration.md))
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

### PROCEDURE 3: Validate Plugin Installation

**When to use:** When plugins fail to load, when hooks do not fire, or when verifying plugin structure.

**Steps:** Run plugin validate command, check for errors, verify component loading, test hook execution.

**Related documentation:**

#### Plugin Validation ([references/plugin-validation.md](references/plugin-validation.md))
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

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand plugin lifecycle states
- [ ] Learn PROCEDURE 1: Install plugin from marketplace
- [ ] Learn PROCEDURE 2: Configure local plugin directory
- [ ] Learn PROCEDURE 3: Validate plugin installation
- [ ] Learn PROCEDURE 4: Manage plugins on remote agents
- [ ] Practice adding a marketplace
- [ ] Practice installing a plugin
- [ ] Practice setting up a local plugin
- [ ] Practice validating a plugin
- [ ] Practice installing plugin on remote agent
- [ ] Practice restarting agent after plugin install

## Examples

### Example 1: Installing from Marketplace

```bash
# Step 1: Add marketplace (first time only)
claude plugin marketplace add https://github.com/Emasoft/emasoft-plugins

# Step 2: Install plugin
claude plugin install perfect-skill-suggester@emasoft-plugins

# Step 3: Verify installation
claude plugin list | grep perfect-skill-suggester

# Step 4: RESTART Claude Code (required!)
# Exit and relaunch claude
```

### Example 2: Local Plugin Development

```bash
# Launch Claude Code with local plugin
claude --plugin-dir {baseDir}/OUTPUT_SKILLS/my-plugin

# Launch with multiple local plugins
claude --plugin-dir /path/to/plugin-a --plugin-dir /path/to/plugin-b
```

### Example 3: Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED: plugin manifest
├── commands/                 # Slash commands
│   └── my-command.md
├── agents/                   # Agent definitions
│   └── my-agent.md
├── skills/                   # Agent skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Hook configurations
│   └── hooks.json
├── scripts/                  # Hook and utility scripts
│   └── my-hook.py
└── README.md
```

### Example 4: Plugin Validation

```bash
# Validate plugin structure
claude plugin validate /path/to/my-plugin

# Check hooks registration
/hooks

# Debug plugin loading
claude --debug
```

## Error Handling

### Issue: Plugin installation fails

**Symptoms:** Install command errors, plugin not in list, marketplace issues.

See [references/plugin-installation.md](references/plugin-installation.md) Section 1.8 Troubleshooting for resolution.

### Issue: Local plugin not loading

**Symptoms:** Commands not available, hooks not firing, agents not found.

See [references/local-configuration.md](references/local-configuration.md) Section 2.7 Troubleshooting for resolution.

### Issue: Plugin validation errors

**Symptoms:** Validate command reports errors, plugin partially loads.

See [references/plugin-validation.md](references/plugin-validation.md) Section 3.7 Troubleshooting for resolution.

## PROCEDURE 4: Manage Plugins on Remote Agents

**When to use:** When installing, removing, or managing plugins for agents running in other tmux sessions.

**Steps:** Use aimaestro-agent.sh plugin commands to manage plugins remotely.

**Related documentation:**

#### Remote Plugin Management ([references/remote-plugin-management.md](references/remote-plugin-management.md))
- 4.1 What is remote plugin management - Managing other agents' plugins
- 4.2 Remote installation procedure - Installing plugins on other agents
  - 4.2.1 Marketplace addition - Adding marketplaces remotely
  - 4.2.2 Plugin installation - Installing plugins remotely
  - 4.2.3 Automatic restart - Agent auto-restarts after install
- 4.3 Remote plugin operations - Other management tasks
  - 4.3.1 List plugins - View agent's installed plugins
  - 4.3.2 Enable/disable - Toggle plugins remotely
  - 4.3.3 Uninstall - Remove plugins remotely
  - 4.3.4 Clean cache - Fix corrupt installations
- 4.4 Examples - Remote management scenarios
- 4.5 Troubleshooting - Remote management issues

### Example 5: Install Plugin on Remote Agent

```bash
# Add marketplace to remote agent (auto-restarts agent)
aimaestro-agent.sh plugin marketplace add backend-api github:Emasoft/emasoft-plugins

# Install plugin from that marketplace (auto-restarts agent)
aimaestro-agent.sh plugin install backend-api perfect-skill-suggester

# List plugins on remote agent
aimaestro-agent.sh plugin list backend-api

# Uninstall plugin from remote agent
aimaestro-agent.sh plugin uninstall backend-api my-old-plugin

# Clean plugin cache on remote agent
aimaestro-agent.sh plugin clean backend-api --dry-run
```

### Example 6: Restart Agent After Plugin Changes

```bash
# After installing on current agent (self), manual restart required
# For remote agents, restart is automatic. But if needed:
aimaestro-agent.sh restart backend-api

# With longer wait time for slow systems
aimaestro-agent.sh restart backend-api --wait 5
```

## Key Takeaways

1. **Always restart after install** - Claude Code caches plugin state
2. **Use --plugin-dir for development** - Fastest local testing method
3. **Validate before publishing** - Catch errors early
4. **Components at root, not in .claude-plugin** - Common structure mistake
5. **Scripts must be executable** - chmod +x for hook scripts
6. **Remote agents auto-restart** - aimaestro-agent.sh handles restart for remote installs
7. **Current agent needs manual restart** - Exit and relaunch claude for self-install

## Remote Plugin Management CLI Reference

| Operation | Command |
|-----------|---------|
| List marketplaces | `aimaestro-agent.sh plugin marketplace list <agent>` |
| Add marketplace | `aimaestro-agent.sh plugin marketplace add <agent> <url>` |
| Update marketplace | `aimaestro-agent.sh plugin marketplace update <agent>` |
| Remove marketplace | `aimaestro-agent.sh plugin marketplace remove <agent> <name>` |
| Install plugin | `aimaestro-agent.sh plugin install <agent> <plugin>` |
| Uninstall plugin | `aimaestro-agent.sh plugin uninstall <agent> <plugin>` |
| List plugins | `aimaestro-agent.sh plugin list <agent>` |
| Enable plugin | `aimaestro-agent.sh plugin enable <agent> <plugin>` |
| Disable plugin | `aimaestro-agent.sh plugin disable <agent> <plugin>` |
| Validate plugin | `aimaestro-agent.sh plugin validate <agent> <path>` |
| Clean cache | `aimaestro-agent.sh plugin clean <agent>` |
| Reinstall plugin | `aimaestro-agent.sh plugin reinstall <agent> <plugin>` |

## Next Steps

### 1. Read Plugin Installation
See [references/plugin-installation.md](references/plugin-installation.md) for marketplace installation.

### 2. Read Local Configuration
See [references/local-configuration.md](references/local-configuration.md) for development setup.

### 3. Read Plugin Validation
See [references/plugin-validation.md](references/plugin-validation.md) for validation procedures.

---

## Resources

- [Plugin Installation](references/plugin-installation.md)
- [Local Configuration](references/local-configuration.md)
- [Plugin Validation](references/plugin-validation.md)
- [Installation Procedures](references/installation-procedures.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
