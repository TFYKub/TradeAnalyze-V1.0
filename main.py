import time
import traceback

from alerts.line_alert import send_line_message
from config.config_validator import validate
from core.orchestrator import TradeOrchestrator
from reports.formatter import format_report
from reports.sheet_writer import log_options_signals, log_trade_signals
from utils.symbol_loader import load_symbols


def run_trading_engine() -> None:

    validate()

    orchestrator = TradeOrchestrator()
    success = 0
    fail = 0

    symbols = load_symbols("LINE")

    if not symbols:
        print("❌ No symbols found in Google Sheet (SYMBOL_CONFIG)")
        return

    print("\n🚀 ===== TRADING ENGINE START =====")
    print(f"📊 Symbols loaded: {len(symbols)}")

    for symbol in symbols:

        print(f"\n📊 Processing: {symbol}")

        try:
            data = orchestrator.run(symbol)

            if not data:
                fail += 1
                continue

            signals = data.get("signals", [])
            options = data.get("options", [])
            monte = data.get("monte", [])
            runtime = data.get("runtime", 0)

            report = format_report(signals, options, monte, runtime, success, fail)

            send_line_message(report["text"])
            log_trade_signals(symbol, report["signals"], report["monte"])
            log_options_signals(symbol, report["options"], report["monte"])

            success += 1
            print(f"✅ SENT: {symbol}")

            time.sleep(1)

        except Exception:
            fail += 1
            print(f"❌ ERROR {symbol}:")
            print(traceback.format_exc())

    print("\n🏁 ===== ENGINE DONE =====")
    print(f"SUCCESS: {success} | FAIL: {fail}")


if __name__ == "__main__":
    try:
        run_trading_engine()
    except Exception:
        print("GLOBAL ERROR:")
        print(traceback.format_exc())
