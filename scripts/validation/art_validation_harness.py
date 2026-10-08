#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime, timezone

def record_art_test(process_id, test_id, capability, status, notes, screenshot_path, repo_root):
    valid_statuses = {'PASS', 'FAIL', 'BLOCKED', 'NOT_TESTED'}
    if status.upper() not in valid_statuses:
        raise ValueError('Invalid status: ' + status + '. Allowed: ' + str(valid_statuses))
        
    proc_file = os.path.join(repo_root, 'research', 'procurement', 'processes', process_id, 'art-validation.md')
    if not os.path.exists(proc_file):
        raise FileNotFoundError('Process art-validation file not found: ' + proc_file)
        
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    nl = chr(10)
    lines = [
        '',
        '### Test Run: ' + test_id + ' (' + now_iso + ')',
        '- **Capability:** ' + capability,
        '- **Status:** **' + status.upper() + '**',
        '- **Notes:** ' + notes
    ]
    if screenshot_path and os.path.exists(screenshot_path):
        lines.append('- **Evidence:** [' + os.path.basename(screenshot_path) + '](' + screenshot_path + ')')
    lines.append('')
    
    with open(proc_file, 'a', encoding='utf-8') as fp:
        fp.write(nl.join(lines))
        
    print('Recorded ART test execution for ' + process_id + ' in ' + proc_file + ': ' + status.upper())
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--process-id', required=True, choices=['P01-RFP', 'P02-SUPPLIER-DELIVERY', 'P03-REPLENISHMENT', 'P04-INVOICE-EXCEPTIONS'])
    parser.add_argument('--test-id', required=True)
    parser.add_argument('--capability', required=True)
    parser.add_argument('--status', required=True, choices=['PASS', 'FAIL', 'BLOCKED', 'NOT_TESTED'])
    parser.add_argument('--notes', default='Automated test execution record.')
    parser.add_argument('--screenshot', default='')
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()
    record_art_test(args.process_id, args.test_id, args.capability, args.status, args.notes, args.screenshot, args.repo_root)
