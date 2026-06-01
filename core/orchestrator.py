from data.market_data import get_market_data
from engines.markov_engine import classify_regime
from engines.montecarlo_engine import monte_carlo
from engines.option_engine import generate_option_trade
from engines.signal_engine import generate_signal


class TradeOrchestrator:

    def run(self, symbol: str) -> dict | None:

        df = get_market_data(symbol)
        if df is None or df.empty:
            return None

        last = df.iloc[-1]
        price = float(last["Close"])
        atr = float(last["ATR14"])
        regime = classify_regime(last)

        # ------------------------------------------------------------------
        # SIGNAL
        # ------------------------------------------------------------------
        raw_signal = generate_signal(price, atr, regime)

        signal = {
            "symbol": symbol,
            "regime": regime,
            "position": raw_signal.get("position"),
            "entry": raw_signal.get("entry"),
            "sl": raw_signal.get("sl"),
            "tp1": raw_signal.get("tp1"),
            "tp2": raw_signal.get("tp2"),
            "target": raw_signal.get("target"),
            "risk": raw_signal.get("risk"),
            "holding_days": raw_signal.get("holding_days"),
            "active": raw_signal.get("active", True),
        }

        # ------------------------------------------------------------------
        # OPTIONS
        # ------------------------------------------------------------------
        raw_option = generate_option_trade(price, regime, atr)

        option = {
            "symbol": symbol,
            "strategy": raw_option.get("strategy", ""),
            "entry": raw_option.get("entry", 0),
            "target": raw_option.get("target", 0),
            "buy_call": raw_option.get("buy_call"),
            "sell_call": raw_option.get("sell_call"),
            "buy_put": raw_option.get("buy_put"),
            "sell_put": raw_option.get("sell_put"),
            "dte": raw_option.get("dte", 0),
            "pop": raw_option.get("pop", 0),
        }

        # ------------------------------------------------------------------
        # MONTE CARLO
        # ------------------------------------------------------------------
        mc = monte_carlo(df["Close"])

        monte = {
            "symbol": symbol,
            "bull": mc.get("bull", 0),
            "bear": mc.get("bear", 0),
            "sideway": mc.get("sideway", 0),
        }

        return {
            "symbol": symbol,
            "price": price,
            "atr": atr,
            "regime": regime,
            "signals": [signal],
            "options": [option],
            "monte": [monte],
        }
