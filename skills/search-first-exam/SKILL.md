---
name: search-first-exam
description: Search the supplied project and permitted public references before implementing. A Codex-only adaptation for timed assessments with public-source and data-transfer restrictions.
license: MIT
metadata:
  upstream: https://github.com/affaan-m/everything-claude-code
  upstream-commit: 6f1881aeafa3c48f7b603cc4be4b2e4e70daad59
  upstream-path: skills/search-first/SKILL.md
  upstream-sha256: 76835db48dd910061d2e4271b1151793d2fddbabeb2d2866eed068b3580c55d5
  adaptation: agent-exam-kit 0.3.0
---

# Search first for a timed assessment

Find the smallest permitted solution before adding code or dependencies. Start
with the supplied project and its standard library, then inspect relevant public
documentation, open-source packages and repositories. Continue implementation
when the evidence supports a choice.

## Execution boundaries

- Work through the supplied Codex, credentials and authorized models. Use tools
  already exposed by that environment. Keep its version and authorization intact.
- Read the task's dependency, network, language and submission rules first. A
  public package still has to satisfy those rules and its own license.
- Use generic technical terms for external searches. Keep task text, workspace
  files, code, datasets, identifiers, screenshots and results inside the supplied
  environment. Public package metadata requests and incoming downloads may use
  the task's permitted network paths.
- Download public references into the supplied workspace. Keep source URLs,
  versions or commits and applicable licenses. Compare and test references before
  adopting them; the task implementation remains work performed in the workspace.
- This skill needs no external AI service, personal account, browser automation,
  private repository or new MCP service. If a channel is unavailable, record the
  gap and use the available permitted channel. Honor platform blocks.
- Use this workflow during AI-permitted work. Complete AI-prohibited follow-up
  answers yourself.

## Workflow

### 1. Search existing code

Read the task instructions and relevant project guidance. Locate the entry point,
existing implementation, tests and dependency declarations. Use an existing
CodeGraph index if one is present and usable; otherwise use targeted `rg` or
available filesystem search. No index installation is required.

### 2. Decide whether an external search is useful

Skip external research for a routine fix or an existing implementation that meets
the requirement. For an unfamiliar API or algorithm, first consult its official
public documentation using generic technical queries. Look up a package or public
repository only when it closes a specific gap.

For a small decision, one discovery search and one focused verification are
usually sufficient. Stop when one option meets the task's constraints. Avoid
cataloguing tools while a suitable implementation is already available.

### 3. Check adoption conditions

Check functionality, runtime compatibility, license, dependency footprint and
integration time. Prefer the supplied code and standard library when they meet
the requirement. Public source does not imply an open-source license; verify the
license before copying or incorporating code.

If dependencies are prohibited, use documentation to understand the algorithm and
implement within the permitted runtime. Never install a dependency merely because
a tutorial recommends it.

### 4. Choose and verify

Choose reuse, a thin adaptation, composition or a small local implementation.
Record the source, reason and one concrete verification command. Reuse may cover
a bounded component or algorithm, not wholesale replacement of the task result.
Run the relevant test and compare the observed behavior with the task requirement.

Keep short notes in the task's requested document. For example:

```text
Need:
Inspected code / public source and version:
Choice and reason:
Verification command and observed result:
Unresolved condition:
```

The user may authorize a bounded helper using the supplied Codex. This skill
does not require a researcher agent, parallel execution or a particular harness.

## Changes from the upstream workflow

This adaptation retains research before implementation and reuse/adapt/build
decisions. It adds project-first search, generic external queries, source/license
records and assessment boundaries. It removes Claude-specific agent calls,
personal-configuration inspection and external-service setup suggestions.
The original MIT license is included as `UPSTREAM-LICENSE`.
