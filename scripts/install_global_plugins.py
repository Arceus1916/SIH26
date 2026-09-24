"""
Install and Activate Global Antigravity Plugins:
1. CodeRabbit (AI Code Review & Quality Gating)
2. GSD Core (Git. Ship. Done. — Spec-Driven Task Planning & Context-Rot Mitigation)
3. Roo Code (Adaptive Multi-Mode Agent Framework)
4. Ralph Loop (Autonomous Iterative Task Completion Engine)
"""
import os
import sys
import json
from pathlib import Path

GLOBAL_PLUGINS_DIR = Path(r"C:\Users\jadeu\.gemini\config\plugins")

PLUGINS = {
    "coderabbit": {
        "manifest": {
            "name": "coderabbit",
            "version": "1.0.0",
            "description": "AI-powered automated code review, PR quality auditing, security vulnerability scanning, and architectural linting for Antigravity.",
            "author": {
                "name": "CodeRabbit Community"
            },
            "keywords": [
                "coderabbit",
                "code-review",
                "pull-request",
                "security-audit",
                "ast-analysis",
                "quality-gate"
            ]
        },
        "skill": {
            "name": "coderabbit",
            "content": """---
name: coderabbit
description: >
  Performs comprehensive, automated AI code review on git diffs, staged changes,
  individual files, or entire pull requests. Detects logic bugs, security
  vulnerabilities (OWASP), resource leaks, performance bottlenecks, and style
  inconsistencies, providing actionable diff comments and summary reports.
---

# CodeRabbit: AI Code Review & Quality Gating

Use this skill when:
- The user asks to "review my code", "check for bugs", "run a code review", or "audit this PR/diff".
- Staged or uncommitted changes need a thorough security, performance, and logic check before merging or deploying.
- You need structured review feedback categorized by severity (Critical, Warning, Optimization, Note).

## Core Capabilities

### 1. Multi-Dimensional Code Inspection
- **Logic & Correctness**: Off-by-one errors, nil/null dereferences, race conditions, edge-case regressions.
- **Security & OWASP**: SQL/NoSQL injection, Command injection, Path traversal, hardcoded credentials/tokens, insecure deserialization, SSRF.
- **Resource & Performance**: Unclosed DB connections/sockets/files, memory spikes, quadratic/cubic algorithmic loops in request handlers.
- **Architectural & Design Consistency**: Boundary violations between modules, leaky abstractions, missing type hints/contracts.
- **Test Coverage & Gaps**: Identifying untested code branches, missing assertions, and mutation gaps.

### 2. Standard CodeRabbit Review Format
When presenting a review:
1. **Summary Table**:
   - Total Files Inspected
   - High-Severity Issues (Critical)
   - Medium-Severity Issues (Warnings)
   - Performance & Readability Optimizations
2. **Actionable Findings by File**:
   - **Location**: `path/to/file.ext:L123-L135`
   - **Severity**: 🔴 Critical | 🟡 Warning | 🔵 Optimization
   - **Issue Summary**: Clear explanation of the flaw and impact.
   - **Suggested Fix**: Drop-in replacement diff snippet.
3. **Verification Checklist**:
   - Commands to verify the fix (`pytest`, `npm test`, `linter`).
"""
        },
        "rules": {
            "coderabbit-review.md": """# CodeRabbit Quality & Review Rules

When performing code reviews or evaluating pull requests:
1. **Severity Hierarchy**: Categorize all findings into:
   - 🔴 **Critical**: Logic bugs, security exploits, memory/resource leaks, data loss hazards, breaking API contract changes.
   - 🟡 **Warning**: Missing error handling, unhandled edge cases, performance bottlenecks (O(N^2) in hot paths), type inconsistencies.
   - 🔵 **Optimization**: Readability, idiomatic refactoring, code deduplication, documentation clarity.
   - ⚪ **Positive**: Commend well-structured code, solid unit tests, or elegant abstractions.
2. **Actionable Suggestions**: Every criticism must include an exact suggested code fix or diff snippet.
3. **Verification Focus**: Check that new features have corresponding unit or integration tests.
4. **Preserve Comments & Rationale**: Do not strip existing architectural comments during refactoring suggestions.
"""
        }
    },

    "gsd-core": {
        "manifest": {
            "name": "gsd-core",
            "version": "1.0.0",
            "description": "Git. Ship. Done. (GSD) Core — Spec-driven autonomous task planning, 5-phase execution loop, and context-rot mitigation framework for Antigravity.",
            "author": {
                "name": "Open GSD Team"
            },
            "keywords": [
                "gsd",
                "gsd-core",
                "task-planning",
                "milestones",
                "spec-driven",
                "autonomous-execution",
                "ship"
            ]
        },
        "skill": {
            "name": "gsd-core",
            "content": """---
name: gsd-core
description: >
  Drives spec-driven autonomous development using the GSD (Git. Ship. Done.)
  5-phase lifecycle: Discuss, Plan, Execute, Verify, and Ship. Breaks down epics
  into atomic milestones, maintains persistent planning state (.planning/STATE.md),
  and eliminates context rot across long sessions.
---

# GSD Core (Git. Ship. Done.)

Use this skill when:
- The user asks to "plan a feature", "use GSD", "break this down into milestones", or "execute this spec".
- Working on complex multi-step epics that need structured state management across sessions.
- Enforcing verifiable completion criteria for each development phase.

## The 5-Phase GSD Lifecycle

```text
[1. Discuss] ──> [2. Plan] ──> [3. Execute] ──> [4. Verify] ──> [5. Ship]
      ▲                                                │
      └────────────── Fix / Rework Loop ───────────────┘
```

1. **Phase 1: Discuss**
   - Clarify intent, scope boundaries, non-goals, and architectural constraints.
   - Generate or update `.planning/SPEC.md`.

2. **Phase 2: Plan**
   - Decompose specifications into bite-sized, atomic milestones.
   - Each milestone must have explicit, testable acceptance criteria.
   - Document in `.planning/ROADMAP.md`.

3. **Phase 3: Execute**
   - Implement code changes milestone by milestone.
   - Keep context windows clean by delegating discrete subtasks.

4. **Phase 4: Verify**
   - Run automated test suites, linting, and contract validation.
   - Zero-tolerance for unverified milestone advancement.

5. **Phase 5: Ship**
   - Create clean, descriptive git commits for the milestone.
   - Update `.planning/STATE.md` with completed items and current progress.
"""
        },
        "rules": {
            "gsd-workflow.md": """# GSD Workflow Protocol Rules

1. **State Persistence**: Always inspect `.planning/STATE.md` at the start of work and update it at phase boundaries.
2. **Atomic Verification**: Never advance a phase from 'Execute' to 'Ship' without passing all verification tests.
3. **No Unplanned Scope**: Reject spontaneous scope expansion during execution; log new ideas in `.planning/BACKLOG.md`.
4. **Context Cleanliness**: Avoid hoarding unnecessary terminal logs or large search outputs in context; summarize findings immediately.
"""
        }
    },

    "roo-code": {
        "manifest": {
            "name": "roo-code",
            "version": "1.0.0",
            "description": "Adaptive multi-mode agent system providing specialized Architect, Code, Ask, and Debug roles with tailored constraints.",
            "author": {
                "name": "Roo Code Community"
            },
            "keywords": [
                "roo-code",
                "multi-mode",
                "architect",
                "code",
                "ask",
                "debug",
                "modes"
            ]
        },
        "skill": {
            "name": "roo-code",
            "content": """---
name: roo-code
description: >
  Provides adaptive multi-mode operation for coding agents. Switches between
  specialized modes: Architect (system design & schemas), Code (high-velocity
  implementation), Ask (read-only codebase exploration), and Debug (root-cause
  investigation) with role-specific tool restrictions.
---

# Roo Code: Multi-Mode Agent Framework

Use this skill when:
- The user requests switching modes (e.g. "switch to architect mode", "code mode", "ask mode", "debug mode").
- The user needs an architectural review before writing code.
- Read-only exploration is required without accidental file changes.

## Available Operating Modes

### 1. Architect Mode
- **Focus**: High-level system design, data schemas, API contracts, architectural decision records (ADRs), module boundaries.
- **Constraints**: Focuses on design and planning; does not prematurely edit production code.

### 2. Code Mode
- **Focus**: Surgical, high-velocity code implementation, idiomatic refactoring, test-driven implementation.
- **Constraints**: Strictly follows architecture specifications; writes production-ready code with no shortcuts.

### 3. Ask Mode
- **Focus**: Read-only codebase interrogation, answering technical questions, mapping dependencies.
- **Constraints**: Strictly forbidden from creating or modifying files or running destructive commands.

### 4. Debug Mode
- **Focus**: Root-cause analysis, reproduction scripts, stack trace dissection, minimal regression tests.
- **Constraints**: Must isolate the exact defect with evidence before proposing fixes.
"""
        },
        "rules": {
            "roo-modes.md": """# Roo Code Mode Operational Rules

1. **Architect Mode**: Focus on architecture, data models, API boundaries, and ADRs. Do not implement production code until the architecture is approved.
2. **Code Mode**: Surgical, high-quality implementation adhering to design specifications.
3. **Ask Mode**: Strictly read-only. Search, inspect, and explain code without modifying any files.
4. **Debug Mode**: Isolate root causes using reproductions, minimal test cases, and log analysis before modifying code.
"""
        }
    },

    "ralph-loop": {
        "manifest": {
            "name": "ralph-loop",
            "version": "1.0.0",
            "description": "Autonomous iterative task completion engine and fresh-context execution loop for continuous development until verifiable goal completion.",
            "author": {
                "name": "Ralph Loop Community"
            },
            "keywords": [
                "ralph-loop",
                "autonomous-loop",
                "iterative-development",
                "fresh-context",
                "goal-completion"
            ]
        },
        "skill": {
            "name": "ralph-loop",
            "content": """---
name: ralph-loop
description: >
  Executes an autonomous, iterative task completion loop. Reads goals from
  tasks.json or PRD.md, executes incremental steps with fresh context memory,
  evaluates objective verification criteria, and loops until the entire goal
  is 100% finished without premature termination.
---

# Ralph Loop: Autonomous Iterative Execution Engine

Use this skill when:
- The user asks to "run in a loop", "use ralph loop", "don't stop until it's done", or "run autonomous iterations".
- A multi-phase task needs continuous progress tracking against a checklist or PRD until all verification tests pass.
- Managing context limits by persisting state to files and driving incremental progress.

## The Ralph Loop Cycle

```text
┌────────────────────────────────────────────────────────┐
│                   RALPH LOOP CYCLE                     │
│                                                        │
│  [Read PRD / tasks.json] ──> [Pick Next Task]          │
│            ▲                        │                  │
│            │                        ▼                  │
│   [Resume Fresh Context]   [Implement & Test]          │
│            ▲                        │                  │
│            │                        ▼                  │
│    [Commit Checkpoint] <─── [Verify All Criteria]      │
└────────────────────────────────────────────────────────┘
```

### Key Principles
1. **File System as Memory**: Progress is tracked in `tasks.json` or `PRD.md` on disk, allowing state to survive restarts.
2. **Fresh Context Iterations**: Each iteration focuses strictly on the active task without dragging historical context rot.
3. **Objective Completion Check**: Never declare completion based on assumptions; always run tests, linters, or verification scripts.
"""
        },
        "rules": {
            "ralph-loop-protocol.md": """# Ralph Loop Autonomous Protocol Rules

1. **Checklist Grounding**: Ground every iteration in `tasks.json` or `PRD.md`.
2. **Objective Verification Gate**: An item is only marked complete when an automated check (tests, build, lint) passes.
3. **Incremental Commits**: Commit working progress after each passing verification milestone.
4. **Circuit Breakers**: If the same test fails 3 consecutive iterations, halt the loop and seek clarification.
5. **No Premature Exit**: Do not terminate execution while unfinished checklist items remain.
"""
        }
    }
}

def install_plugins():
    print(f"Installing plugins to: {GLOBAL_PLUGINS_DIR}")
    GLOBAL_PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

    for plugin_id, config in PLUGINS.items():
        plugin_path = GLOBAL_PLUGINS_DIR / plugin_id
        plugin_path.mkdir(parents=True, exist_ok=True)

        # 1. Write plugin.json
        manifest_path = plugin_path / "plugin.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(config["manifest"], f, indent=2)
        print(f"  [+] Wrote {manifest_path}")

        # 2. Write skill
        if "skill" in config:
            skill_dir = plugin_path / "skills" / config["skill"]["name"]
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_path = skill_dir / "SKILL.md"
            with open(skill_path, "w", encoding="utf-8") as f:
                f.write(config["skill"]["content"].strip() + "\n")
            print(f"  [+] Wrote {skill_path}")

        # 3. Write rules
        if "rules" in config:
            rules_dir = plugin_path / "rules"
            rules_dir.mkdir(parents=True, exist_ok=True)
            for rule_filename, rule_content in config["rules"].items():
                rule_path = rules_dir / rule_filename
                with open(rule_path, "w", encoding="utf-8") as f:
                    f.write(rule_content.strip() + "\n")
                print(f"  [+] Wrote {rule_path}")

    print("\nAll 4 plugins created successfully on disk.")

if __name__ == "__main__":
    install_plugins()
