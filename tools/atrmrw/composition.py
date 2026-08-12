#!/usr/bin/env python3
"""ATRMRWの史実基準variantから固定船体基礎値を校正する。"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any


FORMULA_ID = "atrmrw.module_composition.add_then_multiply.v1"


def _number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def module_digest(modules: list[dict[str, Any]]) -> str:
    slot_ids = [module.get("slot_id") for module in modules]
    if any(not isinstance(slot_id, str) or not slot_id for slot_id in slot_ids):
        raise ValueError("every contribution requires slot_id")
    if len(slot_ids) != len(set(slot_ids)):
        raise ValueError("duplicate slot_id in module composition")
    payload = json.dumps(modules, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def contribution_totals(stat: str, modules: list[dict[str, Any]]) -> tuple[float, float]:
    additive = 0.0
    multiplicative = 0.0
    for module in modules:
        additive += _number(module.get("add_stats", {}).get(stat, 0.0), f"{stat} add")
        multiplicative += _number(
            module.get("multiply_stats", {}).get(stat, 0.0), f"{stat} multiply",
        )
    return additive, multiplicative


def compose_stat(base: float, stat: str, modules: list[dict[str, Any]]) -> float:
    additive, multiplicative = contribution_totals(stat, modules)
    if 1.0 + multiplicative <= 0.0:
        raise ValueError(f"{stat}: combined multiplier must be greater than -1")
    return (_number(base, f"{stat} base") + additive) * (1.0 + multiplicative)


def calibrate_reference(
    targets: dict[str, float],
    reference_modules: list[dict[str, Any]],
    tolerances: dict[str, float] | None = None,
) -> dict[str, Any]:
    """史実基準module構成から基礎値を一度だけ解き、digestと共に凍結する。"""
    digest = module_digest(reference_modules)
    tolerances = tolerances or {}
    stats: dict[str, Any] = {}
    for stat, raw_target in targets.items():
        target = _number(raw_target, f"{stat} target")
        additive, multiplicative = contribution_totals(stat, reference_modules)
        denominator = 1.0 + multiplicative
        if denominator <= 0.0:
            raise ValueError(f"{stat}: reference multiplier must be greater than -1")
        base = target / denominator - additive
        if base < 0.0:
            raise ValueError(f"{stat}: solved reference base must be non-negative")
        forward = compose_stat(base, stat, reference_modules)
        tolerance = _number(tolerances.get(stat, 1e-9), f"{stat} tolerance")
        residual = abs(forward - target)
        if residual > tolerance:
            raise ValueError(f"{stat}: forward residual {residual} exceeds {tolerance}")
        stats[stat] = {
            "target": target,
            "reference_add": additive,
            "reference_multiply": multiplicative,
            "frozen_base": base,
            "forward_value": forward,
            "residual": residual,
            "tolerance": tolerance,
        }
    return {
        "formula_id": FORMULA_ID,
        "reference_module_digest": digest,
        "base_policy": "freeze_after_reference_calibration",
        "runtime_calibration_status": "pending_HOI4_1.19.2_controlled_experiment",
        "stats": stats,
    }


def evaluate_design(calibration: dict[str, Any], modules: list[dict[str, Any]]) -> dict[str, float]:
    """交換後moduleへ固定基礎値を順方向適用する。基礎値は再逆算しない。"""
    module_digest(modules)
    return {
        stat: compose_stat(record["frozen_base"], stat, modules)
        for stat, record in calibration["stats"].items()
    }
