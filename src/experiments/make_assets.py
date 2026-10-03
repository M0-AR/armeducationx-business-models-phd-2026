"""Generate demo charts + animated GIF for README/preview. No ffmpeg needed (Pillow writer)."""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

DOCS = os.path.join(os.path.dirname(__file__), "../../docs")
os.makedirs(DOCS, exist_ok=True)
CH = os.path.join(DOCS, "charts")
os.makedirs(CH, exist_ok=True)

def chart_royalty():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    labels = ["License $2,307m", "Royalty $2,613m"]
    vals = [2307, 2613]
    bars = ax.bar(labels, vals, color=["#5B8DEF", "#00C49A"])
    ax.set_title("FY26 Arm revenue $4,920m — royalty annuity 53.1% → 55.5% Q1 FY27")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 40, f"${v}m", ha="center", fontsize=10, weight="bold")
    fig.tight_layout(); fig.savefig(f"{CH}/royalty.png", dpi=150); plt.close(fig)

def chart_ladder():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(["v8", "v9 (2x)", "CSS (4x)"], [1, 2, 4], color=["#B0BEC5", "#5B8DEF", "#7C4DFF"])
    ax.set_title("Architecture premium ladder — CSS pays 4x v8 per chip")
    ax.set_ylabel("Royalty multiple vs v8")
    fig.tight_layout(); fig.savefig(f"{CH}/ladder.png", dpi=150); plt.close(fig)

def chart_network():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.barh(["Arm share", "Rest"], [0.739, 0.261], color=["#7C4DFF", "#E0E0E0"])
    ax.set_title("Ecosystem gravity — Arm 73.9% of partnership weight; removal fragments 64.7%")
    ax.set_xlim(0, 1)
    fig.tight_layout(); fig.savefig(f"{CH}/network.png", dpi=150); plt.close(fig)

def chart_trends():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    years = np.array([2020, 2021, 2022, 2023])
    rd = np.array([3.41788, 3.4689, 3.48736, 3.44716])
    ax.plot(years, rd, marker="o", color="#FF6F61", linewidth=2.5)
    ax.set_title("US R&D 3.42%→3.45% GDP + Neoverse 2.22x acceleration")
    ax.set_ylabel("% of GDP")
    fig.tight_layout(); fig.savefig(f"{CH}/trends.png", dpi=150); plt.close(fig)

def demo_gif():
    # 20-frame royalty-growth animation, Pillow GIF, <1MB
    fig, ax = plt.subplots(figsize=(5, 3))
    x = np.linspace(0, 2*np.pi, 100)
    def upd(f):
        ax.clear()
        ax.set_ylim(-1.3, 3.2); ax.set_title(f"Live demo frame {f+1}/20 — royalty annuity compounding")
        ax.plot(x, np.sin(x + f*0.35), color="#5B8DEF", lw=2, label="license")
        ax.plot(x, 1.133 + 0.25*np.sin(x + f*0.35 - 0.5), color="#00C49A", lw=2, label="royalty 1.133x")
        ax.legend(fontsize=8); ax.set_xticks([]); ax.set_yticks([])
    anim = animation.FuncAnimation(fig, upd, frames=20, interval=200)
    out = os.path.join(os.path.dirname(__file__), "../../docs/demo.gif")
    anim.save(out, writer="pillow", fps=5)
    plt.close(fig)
    return out

if __name__ == "__main__":
    chart_royalty(); chart_ladder(); chart_network(); chart_trends()
    gif = demo_gif()
    print(f"charts + {gif} done, size={os.path.getsize(gif)} bytes")
