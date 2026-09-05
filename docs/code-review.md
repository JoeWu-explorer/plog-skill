# Code review

Baseline: `4dc0ebd011ce2fd8acaefe5076985aacfd8450ae`. Initial implementation reviewed: `e2c250e27af5cf2d3d3ab6b856137a28180361ef`. Two independent read-only agents reviewed Standards and Spec, followed by focused review of the fixes. No agent generated visual acceptance scores.

## Standards

1. Post-commit interruption could delete the PNG newly referenced by revision.json. Fixed by reading publication state before rollback; registered or uncertain files are preserved. A controlled interrupt immediately after OS replacement reproduces the old failure and now leaves all versions recoverable.
2. Failed update publication plus failed rollback could delete the previous installation inside TemporaryDirectory. Fixed by keeping the backup outside automatic cleanup, reporting its recovery path, and rechecking local changes after staging/moving. A controlled dual rename failure now preserves the old install.

Focused re-review confirmed both resolved; no new concrete defect or actionable Fowler-smell finding in these changes.

## Spec

1. A low-scoring retry could bypass the release score gate. Fixed by validating every attempt, while counting only the 18 fixed first attempts. Delivered results without complete passing human review also block release.
2. First acceptance could bind an earlier candidate to a source changed during generation. Fixed by requiring the SHA-256 retained from pre-generation inspect, rejecting changes before saving, and passing that value through the CLI and Skill instructions.

Focused re-review confirmed both resolved and no new concrete defect in these changes. Known missing release evidence remains: successful clean-host generation/modification/recovery, full environment and human visual evaluation, reviewed formal examples and complete publication review.

Initial findings: Standards 2, Spec 2 concrete defects plus known acceptance gaps. Remaining concrete findings after focused re-review: 0 on each axis. Release remains not passed.
