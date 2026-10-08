#!/usr/bin/env python3
import os
import sys
import re
import shutil
import argparse
import getpass
import subprocess
from urllib.parse import quote

COORDINATOR_USER = "chiranjeevi"

MODULE_TO_FEATURE = {
    'AGENT': 'Agent Lab',
    'ORCHESTRATOR': 'Orchestrator',
    'ORC': 'Orchestrator',
    'TOOL': 'Tool Builder',
    'TOOLBUILDER': 'Tool Builder',
    'SFN': 'Serverless Functions',
    'GOV': 'Governance',
    'AGENTX': 'Agent X',
    'ADK': 'ART Deployment Kit (ADK)',
    'MCP': 'MCP Servers',
    'TRIGGER': 'Triggers',
    'CRED': 'Credential Manager'
}

def verify_coordinator_authorization(declared_user=None, repo_root='.'):
    """
    Verify that the execution environment genuinely possesses Project Coordinator authority.
    Does not trust self-declared coordinator identity without system and credential verification.
    Fails closed if authentication is unavailable, ambiguous, or identity mismatches.
    """
    if declared_user and declared_user.strip().lower() != COORDINATOR_USER:
        return False, f"Declared user '{declared_user}' is not authorized. Coordinator operations are restricted to '{COORDINATOR_USER}'."

    # 1. OS user verification
    try:
        current_os_user = getpass.getuser()
    except Exception:
        current_os_user = os.environ.get("USER", "")
        
    if current_os_user != COORDINATOR_USER:
        return False, (
            f"OS identity check failed: Active system user is '{current_os_user}', not '{COORDINATOR_USER}'. "
            "Self-declared coordinator privileges without verified OS identity are rejected."
        )

    # 2. Credential & Git/GitHub verification
    git_name = ""
    git_email = ""
    try:
        res_name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=repo_root)
        if res_name.returncode == 0:
            git_name = res_name.stdout.strip().lower()
        res_email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True, cwd=repo_root)
        if res_email.returncode == 0:
            git_email = res_email.stdout.strip().lower()
    except Exception:
        pass

    gh_authenticated = False
    try:
        res_gh = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, cwd=repo_root)
        if res_gh.returncode == 0 or "Logged in to github.com" in (res_gh.stdout + res_gh.stderr):
            output = res_gh.stdout + res_gh.stderr
            if "Chiranjeevi005" in output or "chiranjeevi" in output.lower():
                gh_authenticated = True
    except Exception:
        pass

    if not (gh_authenticated or "chiranjeevi" in git_name or "chiranjeevi" in git_email):
        return False, (
            "Coordinator credential verification failed: No verified Git credentials or GitHub auth session "
            f"found matching '{COORDINATOR_USER}'. Failing closed."
        )

    return True, f"Verified coordinator authority for '{COORDINATOR_USER}'."

def promote_draft(draft_id, repo_root, coordinator=None):
    authorized, reason = verify_coordinator_authorization(declared_user=coordinator, repo_root=repo_root)
    if not authorized:
        print(f"❌ PERMISSION DENIED: {reason}", file=sys.stderr)
        raise PermissionError(f"PERMISSION DENIED: {reason}")
        
    drafts_root = os.path.join(repo_root, 'services', 'bugs-ledger', 'ART-Product-Validation', 'drafts')
    bugs_root = os.path.join(repo_root, 'services', 'bugs-ledger', 'ART-Product-Validation', 'bugs')
    
    target_draft_dir = None
    if os.path.exists(drafts_root):
        for d in os.listdir(drafts_root):
            if d.startswith(draft_id + '__') or d == draft_id:
                target_draft_dir = os.path.join(drafts_root, d)
                break
            
    if not target_draft_dir or not os.path.exists(target_draft_dir):
        raise FileNotFoundError('Draft folder not found for ID: ' + draft_id)
        
    m = re.match(r'^DRAFT-(?:P[0-9]{2})-([A-Z]+)-[0-9]{3}', draft_id)
    if not m:
        raise ValueError('Invalid draft ID format: ' + draft_id)
    mod_code = m.group(1)
    feature = MODULE_TO_FEATURE.get(mod_code, 'Agent Lab')
    
    existing_seq = 0
    feature_dir = os.path.join(bugs_root, feature)
    os.makedirs(feature_dir, exist_ok=True)
    
    for f in os.listdir(feature_dir):
        m_seq = re.match(r'^ART-' + mod_code + r'-([0-9]{3})', f)
        if m_seq:
            s_val = int(m_seq.group(1))
            if s_val > existing_seq:
                existing_seq = s_val
                
    canonical_id = 'ART-' + mod_code + '-' + str(existing_seq + 1).zfill(3)
    slug = os.path.basename(target_draft_dir).split('__')[-1]
    canonical_folder = canonical_id + '__' + slug
    canonical_dir = os.path.join(feature_dir, canonical_folder)
    
    print('Promoting ' + draft_id + ' -> ' + canonical_id + ' under ' + feature + '/' + canonical_folder)
    
    shutil.move(target_draft_dir, canonical_dir)
    
    old_md = os.path.join(canonical_dir, draft_id + '.md')
    new_md = os.path.join(canonical_dir, canonical_id + '.md')
    if os.path.exists(old_md):
        shutil.move(old_md, new_md)
        
    for fname in os.listdir(canonical_dir):
        if draft_id in fname and fname != (canonical_id + '.md'):
            new_fname = fname.replace(draft_id, canonical_id)
            shutil.move(os.path.join(canonical_dir, fname), os.path.join(canonical_dir, new_fname))
            
    with open(new_md, 'r', encoding='utf-8') as fp:
        c = fp.read()
        
    c = c.replace(draft_id, canonical_id)
    with open(new_md, 'w', encoding='utf-8') as fp:
        fp.write(c)
        
    compile_script = os.path.join(repo_root, 'scripts', 'validation', 'compile_ledger.py')
    ledger_out = os.path.join(repo_root, 'services', 'bugs-ledger', 'ART-Product-Validation', 'ART_PRODUCT_VALIDATION_LEDGER.md')
    if os.path.exists(compile_script):
        subprocess.run([sys.executable, compile_script, '--bugs-root', bugs_root, '--output', ledger_out], check=True)
        
    print('Promotion complete: ' + canonical_id + ' established.')
    return canonical_id

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft-id', required=True)
    parser.add_argument('--coordinator', default=None, help="Declared coordinator username")
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()
    try:
        promote_draft(args.draft_id, args.repo_root, coordinator=args.coordinator)
    except PermissionError as pe:
        sys.exit(1)
