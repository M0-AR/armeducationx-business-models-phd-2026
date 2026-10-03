"""E5 — Business-model selector: assess, choose, pivot (course module 3).
Options: Academic / Flexible-Startup / Flexible-SME / Total-Access / CSS-royalty / AGI-Chip.
Rule engine from Arm Subscription Guide + Tchouaso 2025 (power->non-exclusive breadth)
+ Teece 2018 (complementary assets) + Filosa 2024 (pivot stages).
Benchmark: 12 scenarios; target labels from first principles; report accuracy.
"""
from __future__ import annotations
from .live_data import save_live_snapshot

SCENARIOS = [
    ({"stage": "university", "commercial": False, "funding_m": 0, "volume": 0, "need_css": False, "need_chip": False}, "Academic"),
    ({"stage": "startup", "commercial": True, "funding_m": 5, "volume": 10_000, "need_css": False, "need_chip": False}, "Flexible-Startup"),
    ({"stage": "startup", "commercial": True, "funding_m": 40, "volume": 100_000, "need_css": False, "need_chip": False}, "Flexible-Startup"),
    ({"stage": "sme", "commercial": True, "funding_m": 60, "volume": 500_000, "need_css": False, "need_chip": False}, "Flexible-SME"),
    ({"stage": "enterprise", "commercial": True, "funding_m": 500, "volume": 5_000_000, "need_css": True, "need_chip": False}, "Total-Access-CSS"),
    ({"stage": "hyperscaler", "commercial": True, "funding_m": 5000, "volume": 10_000_000, "need_css": True, "need_chip": False}, "Total-Access-CSS"),
    ({"stage": "hyperscaler", "commercial": True, "funding_m": 5000, "volume": 2_000_000, "need_css": True, "need_chip": True}, "AGI-Chip"),
    ({"stage": "oem", "commercial": True, "funding_m": 1000, "volume": 1_000_000, "need_css": False, "need_chip": True}, "AGI-Chip"),
    ({"stage": "startup", "commercial": True, "funding_m": 10, "volume": 50_000, "need_css": True, "need_chip": False}, "Flexible-SME-CSS"),
    ({"stage": "enterprise", "commercial": True, "funding_m": 200, "volume": 1_000_000, "need_css": False, "need_chip": False}, "Total-Access"),
    ({"stage": "research", "commercial": False, "funding_m": 2, "volume": 1000, "need_css": False, "need_chip": False}, "Academic"),
    ({"stage": "sme", "commercial": True, "funding_m": 20, "volume": 200_000, "need_css": True, "need_chip": False}, "Flexible-SME-CSS"),
]

def select(s: dict) -> str:
    if not s["commercial"]:
        return "Academic"
    if s.get("need_chip") and s["volume"] >= 500_000:
        return "AGI-Chip"
    if s.get("need_css"):
        if s["funding_m"] <= 50 or s["stage"] == "startup":
            return "Flexible-SME-CSS"
        return "Total-Access-CSS"
    if s["stage"] == "startup" and s["funding_m"] <= 50:
        return "Flexible-Startup"
    if s["funding_m"] <= 80 or s["stage"] == "sme":
        return "Flexible-SME"
    return "Total-Access"

def pivot_advice(current: str, growth: str) -> str:
    order = ["Academic", "Flexible-Startup", "Flexible-SME", "Flexible-SME-CSS", "Total-Access", "Total-Access-CSS", "AGI-Chip"]
    if order.index(growth) > order.index(current):
        return f"Pivot {current} -> {growth}: progressive platformization (Filosa 3-phase)."
    return f"Hold {current}."

def run():
    correct = sum(1 for s, label in SCENARIOS if select(s) == label)
    acc = correct / len(SCENARIOS)
    result = {
        "experiment": "E5_model_selector",
        "n": len(SCENARIOS), "correct": correct, "accuracy": round(acc, 3),
        "example_pivot": pivot_advice("Flexible-Startup", "Total-Access-CSS"),
        "assertions": {"accuracy_ge_0_83": acc >= 0.83},
    }
    result["PASS"] = all(result["assertions"].values())
    save_live_snapshot(result, "e5_selector.json")
    return result

if __name__ == "__main__":
    import json; print(json.dumps(run(), indent=2))
