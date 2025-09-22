from __future__ import annotations

def lora_config(r=16, alpha=32, dropout=0.05) -> dict:
    return {"r": r, "alpha": alpha, "dropout": dropout}

