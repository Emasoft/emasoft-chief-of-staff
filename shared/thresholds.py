"""
thresholds.py - Shared constants for Chief of Staff Agent.

These thresholds configure behavior for user communication,
status reporting, approval workflows, and agent lifecycle management.
"""

# =============================================================================
# AGENT LIFECYCLE MANAGEMENT
# =============================================================================

# Maximum number of concurrent agents across all projects
MAX_CONCURRENT_AGENTS = 10

# Maximum agents per individual project
MAX_AGENTS_PER_PROJECT = 5

# =============================================================================
# SYSTEM RESOURCE THRESHOLDS
# =============================================================================

# CPU usage threshold percentage - warn/block new agents above this
CPU_THRESHOLD_PERCENT = 80

# Memory usage threshold percentage - warn/block new agents above this
MEMORY_THRESHOLD_PERCENT = 85

# Disk usage threshold percentage - warn/block new agents above this
DISK_THRESHOLD_PERCENT = 90

# =============================================================================
# AGENT MONITORING TIMEOUTS
# =============================================================================

# Heartbeat timeout - agent considered unresponsive after this (seconds)
HEARTBEAT_TIMEOUT_SECONDS = 300

# Onboarding timeout - time allowed for agent to complete onboarding (seconds)
ONBOARDING_TIMEOUT_SECONDS = 60

# Termination warning - time given before force terminating unresponsive agent (seconds)
TERMINATION_WARNING_SECONDS = 30

# =============================================================================
# SESSION MEMORY CONFIGURATION
# =============================================================================

# Maximum entries in session memory
MAX_MEMORY_ENTRIES = 100

# Time-to-live for memory entries (days)
MEMORY_TTL_DAYS = 30

# =============================================================================
# STATUS REPORTING THRESHOLDS
# =============================================================================

# How often to poll for status updates (seconds)
STATUS_POLL_INTERVAL_SECONDS = 60

# Maximum retries for status requests before escalating
MAX_STATUS_RETRIES = 3

# =============================================================================
# APPROVAL WORKFLOW TIMEOUTS
# =============================================================================

# Timeout for user approval responses (seconds)
APPROVAL_TIMEOUT_SECONDS = 300

# Reminder interval while waiting for approval (seconds)
APPROVAL_REMINDER_INTERVAL_SECONDS = 60

# =============================================================================
# COMMUNICATION THRESHOLDS
# =============================================================================

# Maximum message length for AI Maestro messages
MAX_MESSAGE_LENGTH = 4000

# Maximum handoff document size (KB)
MAX_HANDOFF_SIZE_KB = 100

# =============================================================================
# ROLE ROUTING
# =============================================================================

# Valid roles that Chief of Staff can route requests to
VALID_ROLES = frozenset(["architect", "orchestrator", "integrator"])

# Role to session prefix mapping
ROLE_PREFIX_MAP = {
    "chief-of-staff": "ecos-",
    "architect": "eaa-",
    "orchestrator": "eoa-",
    "integrator": "eia-",
}
