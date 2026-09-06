# Code review

> 后续代码审查的三项问题已在 `b35dde2` 修复，本机安装已更新；当前包和复审结果见 [修复记录](review-fixes.md)。下文保留 `4a5972e` 的原始验收与发布材料，不能算作新包重新通过真实成图验收。

Baseline: `4dc0ebd011ce2fd8acaefe5076985aacfd8450ae`. Implementation and focused fixes through `4a5972e2c08ab9e16265cf7864efad64f0b09b23` were reviewed along Standards and Spec by two independent read-only agents. This is engineering review; no agent supplied human visual scores.

## Standards

Five concrete defects were found and fixed:

1. An interruption after publishing revision.json could delete its newly registered PNG. Rollback now preserves registered or uncertain files; an injected post-replace interrupt reproduces the former failure and passes after the fix.
2. Failed update publication and failed rollback could remove the old installation through temporary-directory cleanup. Backups now survive outside automatic cleanup; the dual-failure test preserves the old install.
3. A missing installed file at test shutdown could discard the result evidence. Changed or unreadable candidates now produce an incomplete result with evidence preserved.
4. Waiting for a host RPC response discarded interleaved notifications. An ordered pending queue now replays them; a real subprocess protocol test verifies image and turn events arriving before responses.
5. A descendant retaining stdout could hang test shutdown indefinitely. Isolated process-group termination and bounded reader joins now preserve completion evidence; the real descendant-pipe regression passes.

Focused re-review confirmed these fixes, with no remaining concrete finding in the reviewed changes.

## Spec

Three findings were reported, one shared with Standards:

1. A low-scoring retry could bypass the release gate. Every attempt now requires all five passing human scores; only the fixed 18 first attempts count toward the threshold.
2. First acceptance could bind a generated candidate to a source changed during generation. Saving now requires the SHA-256 retained before generation and rejects later changes.
3. The host harness lost notifications while waiting for responses, invalidating attempt counts and status. The same pending-queue fix above preserves the actual sequence.

Focused re-review confirmed the fixes, with no remaining concrete finding in the reviewed changes. Seven unique defects were repaired across both axes. Separately, a real no-upload product test exposed an unauthorized local-typesetting fallback; the installed entry contract was strengthened and a fresh host regression observed zero external calls and zero accepted image.

Human visual review and the final publication decision remain separate. Passing code review does not assert a passing Release Evaluation.
