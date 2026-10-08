#!/usr/bin/env python3
"""
ART Unified Harness CLI — art_harness.py

Unified entry point for:
- Workspace & Bug Ledger Validation
- ART Test Execution Logging (Harness A)
- Draft Bug Creation & Duplicate Detection (Harness B)
- Bug Retest Recording (Harness B)
- Canonical Bug ID Promotion (Harness C — Coordinator Only)
- Summary Ledger Compilation
"""

import sys
import os
import argparse
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUGS_ROOT = os.path.join(REPO_ROOT, "services", "bugs-ledger", "ART-Product-Validation", "bugs")
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts", "validation")
COORDINATOR_USER = "chiranjeevi"

def cmd_validate(args):
    """Run validation checks across research workspace, bugs ledger, and unit tests."""
    print("=" * 60)
    print("ART INVESTIGATION LAB — UNIFIED SYSTEM VALIDATION")
    print("=" * 60)
    
    all_passed = True
    
    # 1. Procurement workspace check
    proc_script = os.path.join(REPO_ROOT, "scripts", "procurement", "validate-procurement-workspace.py")
    if os.path.exists(proc_script):
        print("\n[1/3] Validating Procurement Research Workspace...")
        res = subprocess.run([sys.executable, proc_script, "--repo-root", REPO_ROOT])
        if res.returncode != 0:
            print("❌ Procurement workspace validation FAILED")
            all_passed = False
        else:
            print("✅ Procurement workspace validation PASSED")
            
    # 2. Bug ledger schema & link check
    bugs_script = os.path.join(SCRIPTS_DIR, "validate-art-bugs.py")
    if os.path.exists(bugs_script):
        print("\n[2/3] Validating ART Bugs Ledger & Evidence Links...")
        res = subprocess.run([sys.executable, bugs_script, "--bugs-root", BUGS_ROOT])
        if res.returncode != 0:
            print("❌ Bugs ledger validation FAILED")
            all_passed = False
        else:
            print("✅ Bugs ledger validation PASSED")
            
    # 3. Unit tests check
    tests_dir = os.path.join(REPO_ROOT, "services", "bugs-ledger", "tests")
    if os.path.exists(tests_dir) and not getattr(args, "skip_unit_tests", False):
        print("\n[3/3] Running Bugs Ledger Unit Tests (pytest)...")
        res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"], cwd=os.path.join(REPO_ROOT, "services", "bugs-ledger"))
        if res.returncode != 0:
            print("❌ Unit test suite FAILED")
            all_passed = False
        else:
            print("✅ All 264 unit tests PASSED")
            
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED CLEANLY")
        return 0
    else:
        print("⚠️ VALIDATION FAILURES DETECTED")
        return 1

def cmd_record_test(args):
    """Record an ART test outcome linked to research (Harness A)."""
    script = os.path.join(SCRIPTS_DIR, "art_validation_harness.py")
    cmd = [
        sys.executable, script,
        "--process-id", args.process_id,
        "--test-id", args.test_id,
        "--capability", args.capability,
        "--status", args.status,
        "--notes", args.notes or "",
        "--repo-root", REPO_ROOT
    ]
    if args.screenshot:
        cmd.extend(["--screenshot", args.screenshot])
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode

def cmd_draft_bug(args):
    """Create a new draft bug with duplicate detection (Harness B)."""
    script = os.path.join(SCRIPTS_DIR, "bug_intake_harness.py")
    cmd = [
        sys.executable, script, "create-draft",
        "--contributor", args.contributor,
        "--module", args.module,
        "--title", args.title,
        "--desc", args.desc,
        "--severity", args.severity or "MEDIUM",
        "--repo-root", REPO_ROOT
    ]
    if args.evidence:
        cmd.append("--evidence")
        cmd.extend(args.evidence)
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode

def cmd_retest(args):
    """Record a retest verification against an existing bug (Harness B)."""
    script = os.path.join(SCRIPTS_DIR, "bug_intake_harness.py")
    cmd = [
        sys.executable, script, "retest",
        "--bug-id", args.bug_id,
        "--actor", args.actor,
        "--verdict", args.verdict,
        "--notes", args.notes or "",
        "--repo-root", REPO_ROOT
    ]
    if args.evidence:
        cmd.append("--evidence")
        cmd.extend(args.evidence)
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode

def cmd_promote(args):
    """Promote a draft bug to a canonical ART-* ID (Harness C — Coordinator Only)."""
    actor = (args.coordinator or "").strip().lower()
    if actor != COORDINATOR_USER:
        print(f"❌ PERMISSION DENIED: Actor '{args.coordinator}' is not authorized to promote bugs.")
        print(f"   Only the Project Coordinator ('{COORDINATOR_USER}') has authority to allocate canonical ART IDs.")
        return 1
        
    script = os.path.join(SCRIPTS_DIR, "promote_canonical_bug.py")
    cmd = [
        sys.executable, script,
        "--draft-id", args.draft_id,
        "--repo-root", REPO_ROOT
    ]
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode

def cmd_compile_ledger(args):
    """Compile ART_PRODUCT_VALIDATION_LEDGER.md from disk bug records."""
    script = os.path.join(SCRIPTS_DIR, "compile_ledger.py")
    return subprocess.run([sys.executable, script], cwd=REPO_ROOT).returncode

def main():
    parser = argparse.ArgumentParser(
        description="ART Unified Harness CLI — Coordinates research, testing, bug lifecycle, and validations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")
    
    # validate
    val_p = subparsers.add_parser("validate", help="Run workspace, bug ledger, and test suite validations.")
    val_p.add_argument("--skip-unit-tests", action="store_true", help="Skip running pytest unit tests.")
    val_p.set_defaults(func=cmd_validate)
    
    # record-test (Harness A)
    rt_p = subparsers.add_parser("record-test", help="Record an ART test outcome (Harness A).")
    rt_p.add_argument("--process-id", required=True, choices=["P01-RFP", "P02-SUPPLIER-DELIVERY", "P03-REPLENISHMENT", "P04-INVOICE-EXCEPTIONS"], help="Procurement process ID")
    rt_p.add_argument("--test-id", required=True, help="Test execution ID (e.g. TEST-P02-001)")
    rt_p.add_argument("--capability", required=True, help="Target ART capability evaluated")
    rt_p.add_argument("--status", required=True, choices=["PASS", "FAIL", "BLOCKED", "NOT_TESTED"], help="Execution verdict")
    rt_p.add_argument("--notes", help="Execution observation notes")
    rt_p.add_argument("--screenshot", help="Path to evidence screenshot")
    rt_p.set_defaults(func=cmd_record_test)
    
    # draft-bug (Harness B)
    db_p = subparsers.add_parser("draft-bug", help="Create a draft bug with duplicate detection (Harness B).")
    db_p.add_argument("--contributor", required=True, choices=["P01", "P02", "P03", "P04"], help="Contributor process code")
    db_p.add_argument("--module", required=True, help="Target module (Agent, Governance, Orchestrator, Serverless, Tool, AgentX)")
    db_p.add_argument("--title", required=True, help="Concise bug title")
    db_p.add_argument("--desc", required=True, help="Bug description / repro steps")
    db_p.add_argument("--severity", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="MEDIUM", help="Bug severity")
    db_p.add_argument("--evidence", nargs="*", help="Evidence screenshot paths")
    db_p.set_defaults(func=cmd_draft_bug)
    
    # retest (Harness B)
    ret_p = subparsers.add_parser("retest", help="Submit a retest verification against an existing bug (Harness B).")
    ret_p.add_argument("--bug-id", required=True, help="Canonical bug ID (e.g. ART-AGENT-001)")
    ret_p.add_argument("--actor", required=True, help="Contributor username (e.g. ashwin)")
    ret_p.add_argument("--verdict", required=True, choices=["PASSED", "FAILED", "INCONCLUSIVE", "VERIFIED"], help="Retest verdict")
    ret_p.add_argument("--notes", help="Retest observation notes")
    ret_p.add_argument("--evidence", nargs="*", help="Evidence screenshot paths")
    ret_p.set_defaults(func=cmd_retest)
    
    # promote-bug (Harness C)
    pb_p = subparsers.add_parser("promote-bug", help="Promote a draft bug to canonical ART ID (Harness C — Coordinator Only).")
    pb_p.add_argument("--draft-id", required=True, help="Draft ID (e.g. DRAFT-P03-AGENT-001)")
    pb_p.add_argument("--coordinator", required=True, help="Coordinator username (must be 'chiranjeevi')")
    pb_p.set_defaults(func=cmd_promote)
    
    # compile-ledger
    cl_p = subparsers.add_parser("compile-ledger", help="Recompile ART_PRODUCT_VALIDATION_LEDGER.md summary table.")
    cl_p.set_defaults(func=cmd_compile_ledger)
    
    args = parser.parse_args()
    sys.exit(args.func(args))

if __name__ == "__main__":
    main()
