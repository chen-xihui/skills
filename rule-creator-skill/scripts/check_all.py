#!/usr/bin/env python3
"""Redis Usage Rule Detection - Combined Checker

Imports and runs all individual check scripts, outputs a summary table,
and exits with code 1 if any violations are found.
"""
import sys
import importlib.util
import os
from pathlib import Path

# All check modules in order
CHECK_MODULES = [
    "check_jedis_001",
    "check_jedis_002",
    "check_jedis_003",
    "check_jedis_004",
    "check_jedis_005",
    "check_jedis_006",
    "check_jedis_007",
    "check_jedis_008",
    "check_jedis_009",
    "check_jedis_010",
    "check_jedis_011",
    "check_jedis_012",
    "check_jedis_013",
    "check_jedis_014",
    "check_lettuce_001",
    "check_lettuce_002",
    "check_lettuce_003",
    "check_lettuce_004",
    "check_lettuce_005",
    "check_lettuce_006",
    "check_lettuce_007",
    "check_redisson_001",
    "check_redisson_002",
    "check_redisson_003",
    "check_redisson_004",
    "check_redisson_005",
    "check_sdr_001",
    "check_sdr_002",
    "check_sdr_003",
    "check_cluster_001",
    "check_cluster_002",
    "check_cluster_003",
]


def load_module(module_name, scripts_dir):
    """Dynamically load a check module from the scripts directory."""
    module_path = scripts_dir / f"{module_name}.py"
    if not module_path.exists():
        print(f"[WARN] Module not found: {module_path}")
        return None
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[WARN] Failed to load {module_name}: {e}")
        return None
    return module


def run_checks(project_root):
    """Run all check modules and collect results."""
    scripts_dir = Path(__file__).parent
    results = []

    for module_name in CHECK_MODULES:
        module = load_module(module_name, scripts_dir)
        if module is None or not hasattr(module, "check"):
            results.append({
                "rule": module_name,
                "status": "SKIP",
                "count": 0,
                "violations": [],
            })
            continue

        try:
            violations = module.check(project_root)
        except Exception as e:
            results.append({
                "rule": module_name,
                "status": "ERROR",
                "count": 0,
                "violations": [],
                "error": str(e),
            })
            continue

        status = "FAIL" if violations else "PASS"
        results.append({
            "rule": module_name,
            "status": status,
            "count": len(violations),
            "violations": violations,
        })

    return results


def print_summary(results):
    """Print a summary table of all check results."""
    # Column widths
    rule_w = 22
    status_w = 8
    count_w = 8

    print()
    print("=" * (rule_w + status_w + count_w + 8))
    print("  Redis Usage Rule Detection - Summary")
    print("=" * (rule_w + status_w + count_w + 8))
    print(f"  {'Rule':<{rule_w}} {'Status':<{status_w}} {'Count':<{count_w}}")
    print(f"  {'-' * rule_w} {'-' * status_w} {'-' * count_w}")

    total_violations = 0
    total_fail = 0
    total_pass = 0
    total_skip = 0
    total_error = 0

    for r in results:
        rule = r["rule"]
        status = r["status"]
        count = r["count"]
        total_violations += count

        if status == "PASS":
            total_pass += 1
            status_display = "\033[92mPASS\033[0m"
        elif status == "FAIL":
            total_fail += 1
            status_display = "\033[91mFAIL\033[0m"
        elif status == "SKIP":
            total_skip += 1
            status_display = "\033[93mSKIP\033[0m"
        else:
            total_error += 1
            status_display = "\033[95mERROR\033[0m"

        print(f"  {rule:<{rule_w}} {status_display:<{status_w + 7}} {count}")

    print(f"  {'-' * rule_w} {'-' * status_w} {'-' * count_w}")
    print(f"  {'TOTAL':<{rule_w}} {total_pass}P/{total_fail}F/{total_skip}S/{total_error}E  {total_violations}")
    print("=" * (rule_w + status_w + count_w + 8))


def print_violations(results):
    """Print detailed violation output."""
    for r in results:
        if r["status"] != "FAIL":
            continue
        for v in r["violations"]:
            print(f"[FAIL] {v['file']}:{v['line']} - {v['message']}")


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    # Resolve project root
    if not Path(project_root).resolve().exists():
        print(f"[ERROR] Project root does not exist: {project_root}")
        sys.exit(2)

    results = run_checks(project_root)

    # Print detailed violations first
    print_violations(results)

    # Print summary table
    print_summary(results)

    # Exit code
    total_violations = sum(r["count"] for r in results)
    if total_violations > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
