"""Benchmark suite — runs E1..E5, writes combined JSON + markdown table.
Usage: python -m src.experiments.benchmark_suite
"""
from __future__ import annotations
import json, os, datetime
from . import e1_arm_licensing, e2_digitization, e3_network, e4_trends, e5_selector
from .live_data import save_live_snapshot

def main():
    results = {
        "e1": e1_arm_licensing.run(),
        "e2": e2_digitization.run(),
        "e3": e3_network.run(),
        "e4": e4_trends.run(),
        "e5": e5_selector.run(),
    }
    overall = all(v.get("PASS") for v in results.values())
    payload = {
        "repo": "armeducationx-business-models-phd-2026",
        "utc": datetime.datetime.utcnow().isoformat() + "Z",
        "overall_PASS": overall,
        "results": results,
    }
    out = save_live_snapshot(payload, "benchmark_all.json")
    # markdown table
    md = ["| Exp | Name | PASS | Key metric |", "|---|---|---|---|"]
    md.append(f"| E1 | Arm licensing annuity | {results['e1']['PASS']} | annuity_ratio={results['e1']['annuity_ratio_royalty_over_license']} css=4x |")
    md.append(f"| E2 | Digitization benchmark | {results['e2']['PASS']} | acc={results['e2']['accuracy']} |")
    md.append(f"| E3 | Partnership network | {results['e3']['PASS']} | arm_share={results['e3']['arm_ecosystem_share']} frag={results['e3']['fragmentation_if_arm_removed']} |")
    md.append(f"| E4 | Market trends live | {results['e4']['PASS']} | accel={results['e4']['neoverse_acceleration_vs_lifetime_avg']}x |")
    md.append(f"| E5 | Model selector | {results['e5']['PASS']} | acc={results['e5']['accuracy']} |")
    md.append(f"\nOverall: {'PASS' if overall else 'FAIL'} — {payload['utc']}")
    md_path = os.path.join(os.path.dirname(out), "benchmark_table.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nSaved {out} + {md_path}")
    return payload

if __name__ == "__main__":
    main()
