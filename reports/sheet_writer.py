from datetime import datetime

from config.config import SHEET_ID
from utils.sheets_auth import get_sheets_client


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def _pick_first(x) -> dict:
    """Return the first element if *x* is a list, or *x* itself if it's a dict."""
    if isinstance(x, list) and x:
        return x[0]
    if isinstance(x, dict):
        return x
    return {}


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------------
# TRADE SIGNALS
# ------------------------------------------------------------------
def log_trade_signals(symbol: str, signals: list | dict, monte: list | dict) -> None:

    gc = get_sheets_client()
    ws = gc.open_by_key(SHEET_ID).worksheet("TradeSignals")

    s = _pick_first(signals)
    m = _pick_first(monte)

    row = [
        _now(),
        symbol,
        s.get("regime", ""),
        s.get("position", s.get("direction", "")),
        s.get("entry", ""),
        s.get("sl", s.get("stop", "")),
        s.get("tp1", ""),
        s.get("tp2", ""),
        m.get("bull", ""),
        m.get("bear", ""),
        m.get("sideway", ""),
    ]

    ws.append_row(row, value_input_option="USER_ENTERED")


# ------------------------------------------------------------------
# OPTIONS
# ------------------------------------------------------------------
def log_options_signals(symbol: str, options: list | dict, monte: list | dict) -> None:

    gc = get_sheets_client()
    ws = gc.open_by_key(SHEET_ID).worksheet("Options")

    o = _pick_first(options)
    m = _pick_first(monte)

    row = [
        o.get("timestamp", _now()),
        symbol,
        o.get("strategy", ""),
        o.get("entry", ""),
        o.get("target", ""),
        o.get("buy_call", ""),
        o.get("sell_call", ""),
        o.get("buy_put", ""),
        o.get("sell_put", ""),
        o.get("dte", ""),
        o.get("pop", ""),
        m.get("bull", ""),
        m.get("bear", ""),
        m.get("sideway", ""),
    ]

    ws.append_row(row, value_input_option="USER_ENTERED")


# ------------------------------------------------------------------
# MARKET DATA  (used by pipeline)
# ------------------------------------------------------------------
def write_market_data(rows: list[list]) -> None:
    """Append raw market-data rows to the MarketData worksheet."""

    gc = get_sheets_client()
    ws = gc.open_by_key(SHEET_ID).worksheet("MarketData")
    ws.append_rows(rows, value_input_option="USER_ENTERED")
