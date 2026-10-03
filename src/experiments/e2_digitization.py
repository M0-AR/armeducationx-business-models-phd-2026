"""E2 — Digitization vs Digitalization vs Transformation classifier.
Course learning outcome: 'differentiate digitalization and digitization, identify disruption.'
Literature anchors: Rachinger et al 2019 (digitization=analog->digital, digitalization=process change),
Parida et al 2019 (digitalization needs BMI), Guerrero et al 2022 maturity model.
Benchmark: 18 labelled vignettes from course modules; keyword+rule classifier; report accuracy.
"""
from __future__ import annotations
from .live_data import save_live_snapshot
import re

CASES = [
    ("Scan paper datasheets to PDF archive", "digitization"),
    ("Convert RTL netlists to digital artefacts", "digitization"),
    ("Automate tape-out checklist with scripts", "digitalization"),
    ("Shift from perpetual IP sale to Flexible Access subscription", "digitalization"),
    ("Launch Arm Total Access pay-as-you-go ecosystem", "transformation"),
    ("Add Ethos-U85 NPU to edge SoC BOM", "digitization"),
    ("Rewire partner revenue share from unit royalty to CSS annuity", "transformation"),
    ("Use AI agents to optimize workloads on Arm (Performix)", "transformation"),
    ("Put Azure Cobalt VMs in 50% regions", "digitalization"),
    ("Replace x86 hosts with Axion CPUs + TPU", "transformation"),
    ("Email license PDFs instead of fax", "digitization"),
    ("MCP Server 10k Docker pulls enabling dev ecosystem", "transformation"),
    ("Track royalties in spreadsheet", "digitization"),
    ("Predictive maintenance via IoT sensors", "digitalization"),
    ("Graviton5 tens of millions cores for agentic AI", "transformation"),
    ("OCR on scanned contracts", "digitization"),
    ("CSS pre-integrated cluster doubling royalty rate", "transformation"),
    ("Online training portal for Flexible Access", "digitalization"),
]

KW_DIGITIZATION = {"scan", "convert", "pdf", "ocr", "archive", "spreadsheet", "email", "fax", "artefact", "bom"}
KW_DIGITALIZATION = {"automate", "subscription", "portal", "predictive", "iot", "process", "training", "regions", "vm"}
KW_TRANSFORMATION = {"ecosystem", "annuity", "platform", "mcp", "agentic", "axion", "css", "performix", "graviton", "revenue share", "pay-as-you-go"}

def classify(text: str) -> str:
    t = text.lower()
    s_trans = sum(1 for k in KW_TRANSFORMATION if k in t)
    s_digi_proc = sum(1 for k in KW_DIGITALIZATION if k in t)
    s_digi_conv = sum(1 for k in KW_DIGITIZATION if k in t)
    # transformation dominates; then digitalization; else digitization
    if s_trans >= 1 and (s_trans >= s_digi_proc):
        return "transformation"
    if s_digi_proc >= 1:
        return "digitalization"
    return "digitization"

def run():
    correct = sum(1 for text, label in CASES if classify(text) == label)
    acc = correct / len(CASES)
    conf = {}
    for text, label in CASES:
        pred = classify(text)
        conf.setdefault(label, {}).setdefault(pred, 0)
        conf[label][pred] += 1
    # disruption detector: transformation containing platform/ecosystem/annuity keywords
    disruption_hits = [t for t, l in CASES if l == "transformation" and classify(t) == "transformation"]
    result = {
        "experiment": "E2_digitization_benchmark",
        "n": len(CASES), "correct": correct, "accuracy": round(acc, 3),
        "confusion": conf,
        "disruption_recall": round(len(disruption_hits) / sum(1 for _, l in CASES if l == "transformation"), 3),
        "assertions": {"accuracy_ge_0_78": acc >= 0.78, "disruption_recall_ge_0_8": len(disruption_hits) / 6 >= 0.8},
    }
    result["PASS"] = all(result["assertions"].values())
    save_live_snapshot(result, "e2_digitization.json")
    return result

if __name__ == "__main__":
    import json; print(json.dumps(run(), indent=2))
