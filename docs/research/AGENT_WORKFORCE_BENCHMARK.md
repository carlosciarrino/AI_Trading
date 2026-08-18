# AI_BRIDGE V3 — AGENT WORKFORCE BENCHMARK

Generated automatically.
AI_BRIDGE project documents NOT supplied to candidates.

## Candidates

### openhands-sdk
- PATH: `/home/carlo/AI_Trading/research/external_agents/openhands-sdk`
- GIT: `8da8b09`
- WORKTREE: DIRTY
- CAPABILITIES:
  - multi_agent: NO
  - orchestration: YES
  - review_loop: NO
  - isolated_workspace: YES
  - autonomous_daemon: NO
  - evidence_audit: NO
  - state_persistence: NO

### mini-swe-agent
- PATH: `/home/carlo/AI_Trading/research/external_agents/mini-swe-agent`
- GIT: `8da8b09`
- WORKTREE: DIRTY
- CAPABILITIES:
  - multi_agent: NO
  - orchestration: YES
  - review_loop: NO
  - isolated_workspace: YES
  - autonomous_daemon: NO
  - evidence_audit: NO
  - state_persistence: YES

### aider
- PATH: `/home/carlo/AI_Trading/research/external_agents/aider`
- GIT: `8da8b09`
- WORKTREE: DIRTY
- CAPABILITIES:
  - multi_agent: NO
  - orchestration: YES
  - review_loop: NO
  - isolated_workspace: NO
  - autonomous_daemon: NO
  - evidence_audit: NO
  - state_persistence: NO

### liza
- PATH: `/home/carlo/AI_Trading/research/external_agents/liza`
- GIT: `dd9e2d5`
- WORKTREE: CLEAN
- CAPABILITIES:
  - multi_agent: YES
  - orchestration: YES
  - review_loop: YES
  - isolated_workspace: YES
  - autonomous_daemon: YES
  - evidence_audit: YES
  - state_persistence: YES

### looper
- PATH: `/home/carlo/AI_Trading/research/external_agents/looper`
- GIT: `608d562`
- WORKTREE: CLEAN
- CAPABILITIES:
  - multi_agent: NO
  - orchestration: YES
  - review_loop: YES
  - isolated_workspace: YES
  - autonomous_daemon: YES
  - evidence_audit: YES
  - state_persistence: YES

## Smoke tests

### openhands-sdk
- COMMAND: `python3 -m compileall -q .`
- RESULT: FAIL
- EXIT: `1`
```text
e.py'...
  File "./openhands-sdk/openhands/sdk/extensions/installation/interface.py", line 24
    class InstallationInterface[T: ExtensionProtocol](ABC):
                               ^
SyntaxError: invalid syntax

*** Error compiling './openhands-sdk/openhands/sdk/extensions/installation/manager.py'...
  File "./openhands-sdk/openhands/sdk/extensions/installation/manager.py", line 28
    class InstallationManager[T: ExtensionProtocol]:
                             ^
SyntaxError: invalid syntax

*** Error compiling './openhands-sdk/openhands/sdk/observability/laminar.py'...
  File "./openhands-sdk/openhands/sdk/observability/laminar.py", line 122
    def observe[**P, R](
               ^
SyntaxError: invalid syntax

*** Error compiling './openhands-sdk/openhands/sdk/plugin/types.py'...
  File "./openhands-sdk/openhands/sdk/plugin/types.py", line 203
    type McpServersDict = dict[str, dict[str, Any]]
         ^^^^^^^^^^^^^^
SyntaxError: invalid syntax

*** Error compiling './openhands-sdk/openhands/sdk/tool/tool.py'...
  File "./openhands-sdk/openhands/sdk/tool/tool.py", line 53
    type ResponseSchema = type[BaseModel] | dict[str, Any]
         ^^^^^^^^^^^^^^
SyntaxError: invalid syntax

*** Error compiling './openhands-sdk/openhands/sdk/utils/models.py'...
  File "./openhands-sdk/openhands/sdk/utils/models.py", line 379
    Union[*tuple(Annotated[t, Tag(n)] for n, t in subclasses.items())],
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?

*** Error compiling './openhands-sdk/openhands/sdk/utils/paging.py'...
  File "./openhands-sdk/openhands/sdk/utils/paging.py", line 7
    class PageProtocol[T](Protocol):
                      ^
SyntaxError: invalid syntax

*** Error compiling './tests/cross/test_remote_conversation_live_server.py'...
  File "./tests/cross/test_remote_conversation_live_server.py", line 644
    f"Found {len(state.events)} events: {
    ^
SyntaxError: unterminated string literal (detected at line 644)

*** Error compiling './tests/platform_utils.py'...
  File "./tests/platform_utils.py", line 41
    def maybe_mark_forked[F: Callable[..., object]](test_func: F) -> F:
                         ^
SyntaxError: invalid syntax

*** Error compiling './tests/sdk/security/test_shell_parser_node_shapes.py'...
  File "./tests/sdk/security/test_shell_parser_node_shapes.py", line 14
    type ExpectedChild = tuple[str, str]
         ^^^^^^^^^^^^^
SyntaxError: invalid syntax
```

### mini-swe-agent
- COMMAND: `python3 -m compileall -q .`
- RESULT: PASS
- EXIT: `0`

### aider
- COMMAND: `python3 -m compileall -q .`
- RESULT: PASS
- EXIT: `0`

### liza
- COMMAND: `go test ./...`
- RESULT: FAIL
- EXIT: `125`
```text
FileNotFoundError: [Errno 2] No such file or directory: 'go'
```

### looper
- COMMAND: `go test ./...`
- RESULT: FAIL
- EXIT: `125`
```text
FileNotFoundError: [Errno 2] No such file or directory: 'go'
```

## Preliminary architectural ranking

1. **Liza** — highest fit: enforced supervisor/state machine + doer/reviewer + worktrees
2. **Looper** — high fit: daemon + planner/reviewer/fixer/worker loops + transition gates
3. **OpenHands SDK** — high fit: composable agent runtime + delegation + local/isolated execution
4. **mini-swe-agent** — useful worker/runtime candidate
5. **aider** — useful coding-agent backend, not full workforce control plane

## NEXT

Do NOT feed AI_BRIDGE documents to candidates yet.
Select candidate architecture from benchmark.
Then build adapter/control-plane integration.

