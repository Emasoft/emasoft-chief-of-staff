# Active Context Management Examples

This document provides complete examples for active context management workflows.

**Parent document**: [03-manage-active-context.md](./03-manage-active-context.md)

---

## Table of Contents
1. [Example 1: Complete Context Update Workflow](#example-1-complete-context-update-workflow)
2. [Example 2: Context Recovery After Compaction](#example-2-context-recovery-after-compaction)
3. [Example 3: Structured Context Template](#example-3-structured-context-template)

---

## Example 1: Complete Context Update Workflow

```bash
#!/bin/bash
# Full context update example

# 1. Start new task - update focus
cat >> .session_memory/active_context.md << 'EOF'

## Current Focus
**Updated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

- **Primary**: Implement user authentication
  - OAuth2 with GitHub
  - JWT token management
- **Next Steps**:
  1. Set up OAuth app in GitHub
  2. Implement callback handler
  3. Add token refresh logic

EOF

# 2. Make decision during implementation
cat >> .session_memory/active_context.md << 'EOF'

## Recent Decisions

### Use JWT with 1-hour expiry
- **Date**: 2026-01-01 14:30 UTC
- **Rationale**: Balance security and UX
- **Implementation**: Add refresh token mechanism
- **Impact**: Requires additional endpoint for token refresh

EOF

# 3. Hit blocker - add open question
cat >> .session_memory/active_context.md << 'EOF'

## Open Questions

### Where to store refresh tokens?
- **Added**: 2026-01-01 14:45 UTC
- **Options**: Database vs Redis vs HTTP-only cookie
- **Blocked**: Token refresh implementation
- **Needs**: Architecture decision from team lead

EOF

echo "✓ Context updated with focus, decision, and question"
```

---

## Example 2: Context Recovery After Compaction

```bash
#!/bin/bash
# Recover context after compaction

recover_context_after_compaction() {
    # 1. Check for latest snapshot
    latest_snapshot=$(ls -t .session_memory/active_context/context_*.md 2>/dev/null | head -1)

    if [ -z "$latest_snapshot" ]; then
        echo "ERROR: No context snapshot found"
        return 1
    fi

    echo "Found snapshot: $latest_snapshot"

    # 2. Check snapshot age
    snapshot_date=$(echo "$latest_snapshot" | grep -oP '\d{8}_\d{6}')
    echo "Snapshot date: $snapshot_date"

    # 3. Restore from snapshot
    cp "$latest_snapshot" .session_memory/active_context.md

    # 4. Add recovery note
    cat >> .session_memory/active_context.md << EOF

---
**Context Restored**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Source**: $latest_snapshot
**Action**: Review and update focus if needed

EOF

    echo "✓ Context restored from snapshot"
}

recover_context_after_compaction
```

---

## Example 3: Structured Context Template

```markdown
# Active Context

**Last Updated:** 2026-01-01 14:30:22 UTC
**Compaction Count:** 3

---

## Current Focus

### Primary Task
Implement user authentication system

**Objectives**:
- OAuth2 integration with GitHub
- JWT-based session management
- Role-based access control

**Progress**:
- [x] GitHub OAuth app created
- [x] Callback handler implemented
- [ ] Token refresh mechanism
- [ ] Role management

**Next Steps**:
1. Complete token refresh endpoint
2. Add role checking middleware
3. Write integration tests

---

## Recent Decisions

### Decision: JWT tokens with 1-hour expiry
**Date**: 2026-01-01 13:00 UTC
**Rationale**: Security best practice while maintaining good UX
**Alternatives Considered**:
- 24-hour tokens (rejected - too long for sensitive data)
- Session cookies (rejected - doesn't support API clients)
**Impact**: Requires refresh token implementation

### Decision: Store refresh tokens in HTTP-only cookies
**Date**: 2026-01-01 14:15 UTC
**Rationale**: Prevents XSS attacks, automatic transmission
**Alternatives Considered**:
- LocalStorage (rejected - XSS vulnerable)
- Database only (rejected - performance concerns)
**Impact**: Requires CSRF protection

---

## Open Questions

### Q: Should we implement remember-me functionality?
**Added**: 2026-01-01 14:30 UTC
**Importance**: User convenience vs. security tradeoff
**Blocked**: Not blocking current work, future enhancement
**Needs**: Product decision from stakeholders

---

## Context Notes

**Key Files**:
- OAuth handler: `src/auth/oauth.ts`
- Token utils: `src/auth/tokens.ts`
- Middleware: `src/middleware/auth.ts`

**Configuration**:
- OAuth app ID: (in `.env`)
- Token secret: (in `.env`)
- Token expiry: 3600s (1 hour)

**References**:
- GitHub OAuth docs: https://docs.github.com/en/apps/oauth-apps
- JWT best practices: https://tools.ietf.org/html/rfc8725

**Test Accounts**:
- Test user 1: testuser@example.com
- Test user 2: admin@example.com (has admin role)
```
