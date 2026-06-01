def format_report(
    signals: list,
    option_results: list,
    monte_results: list,
    runtime: float,
    success_count: int,
    fail_count: int,
) -> dict:
    """
    Build a text report and return the full data bundle used by sheet_writer.
    """

    def fmt(x) -> str:
        try:
            if x is None:
                return "N/A"
            return f"{float(x):.2f}"
        except (TypeError, ValueError):
            return str(x)

    def safe(x) -> str:
        return "N/A" if x is None else str(x)

    lines = []

    lines += ["🚀 TRADE ANALYZE REPORT", "=" * 20]

    # ------------------------------------------------------------------
    # REGIME
    # ------------------------------------------------------------------
    lines += ["📊 MARKET REGIME", "=" * 20]
    for s in signals:
        lines.append(f"{s['symbol']} : {safe(s.get('regime'))}")

    # ------------------------------------------------------------------
    # FUTURES / SIGNALS
    # ------------------------------------------------------------------
    lines += ["=" * 20, "📈 FUTURES", "=" * 20]
    for s in signals:
        lines += [
            f"\n{s['symbol']}",
            f"Position : {safe(s.get('position'))}",
            f"Entry    : {fmt(s.get('entry'))}",
            f"SL       : {fmt(s.get('sl'))}",
            f"TP1      : {fmt(s.get('tp1'))}",
            f"TP2      : {fmt(s.get('tp2'))}",
        ]

    # ------------------------------------------------------------------
    # OPTIONS
    # ------------------------------------------------------------------
    lines += ["=" * 20, "🧠 OPTIONS", "=" * 20]
    for o in option_results:
        pop = o.get("pop") or 0
        lines += [
            f"\n{o.get('symbol', 'NA')}",
            f"Strategy : {safe(o.get('strategy'))}",
            f"Entry    : {fmt(o.get('entry'))}",
            f"Target   : {fmt(o.get('target'))}",
            f"Buy Call : {fmt(o.get('buy_call'))}",
            f"Sell Call: {fmt(o.get('sell_call'))}",
            f"Buy Put  : {fmt(o.get('buy_put'))}",
            f"Sell Put : {fmt(o.get('sell_put'))}",
            f"DTE      : {safe(o.get('dte'))}",
            f"POP      : {pop}%",
        ]

    # ------------------------------------------------------------------
    # MONTE CARLO
    # ------------------------------------------------------------------
    lines += ["=" * 20, "📊 MONTE CARLO", "=" * 20]
    for m in monte_results:
        lines += [
            f"\n{m['symbol']}",
            f"BULL     : {fmt(m.get('bull'))}%",
            f"BEAR     : {fmt(m.get('bear'))}%",
            f"SIDEWAY  : {fmt(m.get('sideway'))}%",
        ]

    return {
        "text": "\n".join(lines),
        "signals": signals,
        "options": option_results,
        "monte": monte_results,
        "runtime": runtime,
        "success": success_count,
        "fail": fail_count,
    }
