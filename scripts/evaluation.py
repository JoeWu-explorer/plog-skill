"""Prepare private release evidence and emit only aggregate, non-private results."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from typing import Any

SAMPLES = tuple(f'synthetic-{i:02d}' for i in range(1, 7)) + tuple(f'real-{i:02d}' for i in range(1, 4))
BEHAVIORS = ('photo_only', 'quote_attribution', 'quotes_traditional_creative', 'input_limits', 'style_aspect', 'minors_privacy_care', 'authorization', 'service_failures', 'invalid_candidate', 'one_retry', 'save_interruption', 'recovery_data_only', 'source_missing_changed', 'invalid_record_version', 'minimal_record_exports')
REVISIONS = ('text_only', 'atmosphere_only', 'old_version_move_text')
DIMENSIONS = ('composition', 'chinese_typography', 'atmosphere', 'narrative', 'save_share_value')
STATUSES = ('untested', 'unsupported', 'fail', 'pass')


def new_evaluation(commit: str, package_sha256: str) -> dict[str, Any]:
    return {'schema_version': 1, 'candidate_commit': commit, 'package_sha256': package_sha256, 'environment': {},
            'attempts': [{'sample': sample, 'round': round_id, 'attempt': 1, 'status': 'untested', 'real_service': False, 'clean_session': False, 'delivery': 'untested', 'misdelivered': False, 'human_reviewer': None, 'scores': {}, 'elapsed_seconds': None, 'cost': None, 'reason': ''} for sample in SAMPLES for round_id in (1, 2)],
            'behaviors': dict.fromkeys(BEHAVIORS, 'untested'), 'revisions': dict.fromkeys(REVISIONS, 'untested')}


def summarize(evidence: dict[str, Any]) -> dict[str, Any]:
    if evidence.get('schema_version') != 1 or not re.fullmatch('[0-9a-f]{40}', evidence.get('candidate_commit', '')) or not re.fullmatch('[0-9a-f]{64}', evidence.get('package_sha256', '')):
        raise ValueError('A fixed commit, package SHA-256 and schema 1 are required.')
    first: dict[tuple[str, int], dict[str, Any]] = {}
    identities: set[tuple[str, int, int]] = set()
    misdelivered = False
    all_deliveries_reviewed = True
    for row in evidence['attempts']:
        if row['sample'] not in SAMPLES or type(row['round']) is not int or row['round'] not in (1, 2) or type(row['attempt']) is not int or row['attempt'] < 1 or row['status'] not in STATUSES or row['delivery'] not in STATUSES or type(row['misdelivered']) is not bool:
            raise ValueError('Invalid attempt identity, status or delivery flag.')
        identity = (row['sample'], row['round'], row['attempt'])
        if identity in identities:
            raise ValueError('Duplicate attempt; retain each attempt exactly once.')
        identities.add(identity)
        misdelivered |= row['misdelivered']
        scores = row['scores']
        human_pass = isinstance(row['human_reviewer'], str) and bool(row['human_reviewer'].strip()) and isinstance(scores, dict) and set(scores) == set(DIMENSIONS) and all(type(v) is int and 4 <= v <= 5 for v in scores.values())
        if row['status'] == 'pass' and not (row['delivery'] == 'pass' and row['real_service'] is True and row['clean_session'] is True and human_pass):
            raise ValueError('Every pass, including retries, requires actual service, clean session, Delivery Verification and all five human scores >=4.')
        if row['delivery'] == 'pass' and not human_pass:
            all_deliveries_reviewed = False
        if row['attempt'] == 1:
            first[(row['sample'], row['round'])] = row
    expected = {(sample, round_id) for sample in SAMPLES for round_id in (1, 2)}
    if set(first) != expected:
        raise ValueError('Keep all 18 fixed first attempts, including untested inputs.')
    passed = [key for key, row in first.items() if row['status'] == 'pass']
    counts = {status: sum(row['status'] == status for row in first.values()) for status in STATUSES}
    for name, keys in [('behaviors', BEHAVIORS), ('revisions', REVISIONS)]:
        if set(evidence[name]) != set(keys) or any(value not in STATUSES for value in evidence[name].values()):
            raise ValueError('Keep the full behavior and revision matrix.')
    matrix_pass = all(value == 'pass' for key in ('behaviors', 'revisions') for value in evidence[key].values())
    all_inputs = {key[0] for key in passed} == set(SAMPLES)
    environment_recorded = all(evidence['environment'].get(key) for key in ('codex', 'platform', 'python', 'image_service', 'service_version_or_unavailable'))
    release_pass = len(passed) >= 16 and all_inputs and matrix_pass and not misdelivered and environment_recorded and all_deliveries_reviewed
    return {'candidate_commit': evidence['candidate_commit'], 'package_sha256': evidence['package_sha256'],
            'status': 'pass' if release_pass else 'not_passed', 'first_generation_total': 18, 'passed': len(passed),
            'untested': counts['untested'], 'unsupported': counts['unsupported'], 'failed': counts['fail'],
            'all_inputs_succeeded': all_inputs, 'misdelivery_blocks_release': misdelivered,
            'behavior_passed': sum(v == 'pass' for v in evidence['behaviors'].values()), 'behavior_total': 15,
            'revision_passed': sum(v == 'pass' for v in evidence['revisions'].values()), 'revision_total': 3,
            'environment_recorded': environment_recorded, 'all_deliveries_reviewed': all_deliveries_reviewed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    initialize = commands.add_parser('init')
    initialize.add_argument('destination', type=Path)
    initialize.add_argument('--commit', required=True)
    initialize.add_argument('--package-sha256', required=True)
    summary = commands.add_parser('summary')
    summary.add_argument('evidence', type=Path)
    args = parser.parse_args()
    try:
        if args.operation == 'init':
            repository = Path(__file__).resolve().parents[1]
            if args.destination.resolve().is_relative_to(repository):
                raise ValueError('Keep private release evidence outside the repository.')
            evidence = new_evaluation(args.commit, args.package_sha256)
            summarize(evidence)
            fd = os.open(args.destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as stream:
                json.dump(evidence, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
            print('Private evidence initialized: 18 untested first attempts; no result has passed.')
        else:
            result = summarize(json.loads(args.evidence.read_text()))
            print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
