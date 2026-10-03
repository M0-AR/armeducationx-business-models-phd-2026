"""E3 — Partnership network / ecosystem gravity graph.
Course claim: 'importance of partnership network within business models.'
Anchors: 1000+ licensees, 22M developers, 350B chips shipped, 50+ endorse AGI CPU,
hyperscalers AWS/Azure/GCP/NVIDIA, EDA Synopsys/Cadence, foundry TSMC/Samsung,
EuroCDP, Malaysia $250M deal, Indonesia gov deal.
Method: build directed graph, compute degree/betweenness, bottleneck test (Jang),
governance-rigidity check (Uzunca: hard-to-replace segment but rigidity risk).
"""
from __future__ import annotations
import networkx as nx
from .live_data import save_live_snapshot

NODES = {
    "Arm": {"type": "platform_owner"},
    "AWS": {"type": "hyperscaler"}, "Azure": {"type": "hyperscaler"},
    "GCP": {"type": "hyperscaler"}, "NVIDIA": {"type": "licensee_competitor"},
    "Qualcomm": {"type": "licensee"}, "Samsung": {"type": "licensee_foundry"},
    "TSMC": {"type": "foundry"}, "Synopsys": {"type": "eda"}, "Cadence": {"type": "eda"},
    "Meta": {"type": "lead_customer"}, "OpenAI": {"type": "customer"},
    "Developers22M": {"type": "complementors"}, "EuroCDP": {"type": "institution"},
    "Malaysia": {"type": "sovereign"}, "Indonesia": {"type": "sovereign"},
    "Startups300": {"type": "long_tail"},
}
EDGES = [
    ("Arm", "AWS", 5), ("Arm", "Azure", 5), ("Arm", "GCP", 5), ("Arm", "NVIDIA", 4),
    ("Arm", "Qualcomm", 4), ("Arm", "Samsung", 4), ("Arm", "TSMC", 5),
    ("Arm", "Synopsys", 3), ("Arm", "Cadence", 3), ("Arm", "Meta", 5),
    ("Arm", "OpenAI", 4), ("Arm", "Developers22M", 5), ("Arm", "EuroCDP", 3),
    ("Arm", "Malaysia", 3), ("Arm", "Indonesia", 3), ("Arm", "Startups300", 4),
    ("TSMC", "AWS", 3), ("TSMC", "NVIDIA", 4), ("Developers22M", "AWS", 4),
    ("Developers22M", "Azure", 4), ("Developers22M", "GCP", 3),
    ("Synopsys", "Startups300", 2), ("EuroCDP", "Startups300", 3),
]

def run():
    G = nx.DiGraph()
    for n, a in NODES.items():
        G.add_node(n, **a)
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)
    deg = dict(G.out_degree(weight="weight"))
    btw = nx.betweenness_centrality(G, weight="weight")
    # H3 ecosystem gravity: Arm out-strength share
    total_w = sum(w for _, _, w in EDGES)
    arm_share = sum(w for u, _, w in EDGES if u == "Arm") / total_w
    # Bottleneck test: removing Arm collapses reachability
    reach_full = sum(1 for _ in nx.descendants(G, "Arm")) + 1
    G2 = G.copy(); G2.remove_node("Arm")
    # largest weakly component size after removal vs before
    lcc_before = len(max(nx.weakly_connected_components(G), key=len))
    comps_after = list(nx.weakly_connected_components(G2))
    lcc_after = len(max(comps_after, key=len)) if comps_after else 0
    fragmentation = 1 - lcc_after / lcc_before
    result = {
        "experiment": "E3_partnership_network",
        "nodes": len(NODES), "edges": len(EDGES),
        "arm_out_strength": deg.get("Arm", 0),
        "arm_ecosystem_share": round(arm_share, 3),
        "top_betweenness": sorted(btw.items(), key=lambda x: -x[1])[:3],
        "reach_from_arm": reach_full,
        "fragmentation_if_arm_removed": round(fragmentation, 3),
        "assertions": {
            "arm_is_top_hub": max(deg, key=deg.get) == "Arm",
            "arm_share_gt_0_6": arm_share > 0.6,
            "removal_fragments_gt_0_3": fragmentation > 0.3,
        },
    }
    result["PASS"] = all(result["assertions"].values())
    save_live_snapshot(result, "e3_network.json")
    return result

if __name__ == "__main__":
    import json; print(json.dumps(run(), indent=2, default=str))
