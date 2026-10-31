#!/usr/bin/env python3
"""risk_manager.py - Calcola size e verifica limiti (P044)."""
import json, os
from datetime import datetime, timezone

CONFIG_PATH = "/home/carlo/AI_Trading/config/risk_budget.json"
ACCOUNT_PATH = "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json"


def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return {
            "max_lots": 0.1, "max_risk_pct": 2.0,
            "max_drawdown_pct": 10.0, "daily_loss_limit_pct": 5.0,
            "atr_multiplier": 2.0, "initial_balance": 100000
        }


def load_account():
    try:
        with open(ACCOUNT_PATH) as f:
            return json.load(f)
    except:
        return {"balance": 0, "equity": 0}


def calculate_position_size(equity, balance, atr_value, config):
    risk_pct = config.get("max_risk_pct", 2.0) / 100.0
    atr_mult = config.get("atr_multiplier", 2.0)
    max_lots = config.get("max_lots", 0.1)

    if atr_value <= 0 or equity <= 0:
        return 0.01

    risk_amount = equity * risk_pct
    sl_distance = atr_value * atr_mult
    if sl_distance <= 0:
        return 0.01

    contract_size = 100000
    lots = risk_amount / (sl_distance * contract_size)
    lots = round(lots, 2)
    if lots < 0.01:
        lots = 0.01
    if lots > max_lots:
        lots = max_lots
    return lots


def check_drawdown(account, config):
    balance = account.get("balance", 0)
    equity = account.get("equity", 0)
    initial = config.get("initial_balance", balance)
    if initial <= 0:
        return (True, "")

    current_drawdown_pct = ((initial - equity) / initial) * 100.0
    max_dd = config.get("max_drawdown_pct", 10.0)
    if current_drawdown_pct >= max_dd:
        return (False, f"drawdown {current_drawdown_pct:.2f}% >= {max_dd}%")

    return (True, "")


def check_margin(account, config):
    """Blocca se il margine libero scende sotto il 20% del balance."""
    balance = account.get("balance", 0)
    free_margin = account.get("free_margin", balance)  # fallback: se manca, assumi = balance
    if balance <= 0:
        return (True, "")
    
    margin_pct = (free_margin / balance) * 100.0
    if margin_pct < 20.0:
        return (False, f"margine libero {margin_pct:.1f}% < 20%")
    return (True, "")


def check_daily_loss(account, config):
    """Blocca se il PNL giornaliero supera il limite (daily_loss_limit_pct)."""
    balance = account.get("balance", 0)
    equity = account.get("equity", 0)
    if balance <= 0:
        return (True, "")

    daily_loss_pct = ((balance - equity) / balance) * 100.0
    max_loss = config.get("daily_loss_limit_pct", 5.0)
    if daily_loss_pct >= max_loss:
        return (False, f"perdita giornaliera {daily_loss_pct:.2f}% >= {max_loss}%")
    return (True, "")


def check_side_limit(action):
    """Blocca se ci sono gia' 2 ordini aperti nella stessa direzione (buy o sell)."""
    orders_path = "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json"
    try:
        with open(orders_path) as f:
            orders = json.load(f)
        open_orders = [o for o in orders if o.get("status") == "open"]
        same_side = [o for o in open_orders if o.get("action") == action]
        if len(same_side) >= 2:
            return False, f"limite 2 ordini {action} raggiunto ({len(same_side)})"
    except Exception as e:
        pass
    return True, ""


def get_risk_decision(atr_value):
    config = load_config()
    account = load_account()

    # 1. Drawdown halt (P044)
    ok, reason = check_drawdown(account, config)
    if not ok:
        return {"lots": 0, "halt": True, "reason": f"halt: {reason}"}

    # 2. Limite per lato (max 2 per direzione)
    ok, reason = check_side_limit(getattr(risk_manager, '_current_action', 'buy'))  # fallback
    if not ok:
        return {"lots": 0, "halt": True, "reason": f"halt: {reason}"}

    # 3. Margin halt (nuovo)
    ok, reason = check_margin(account, config)
    if not ok:
        return {"lots": 0, "halt": True, "reason": f"halt: {reason}"}

    # 3. Daily loss halt (nuovo)
    ok, reason = check_daily_loss(account, config)
    if not ok:
        return {"lots": 0, "halt": True, "reason": f"halt: {reason}"}

    lots = calculate_position_size(
        account.get("equity", 0),
        account.get("balance", 0),
        atr_value,
        config
    )
    return {"lots": lots, "halt": False, "reason": "ok"}
