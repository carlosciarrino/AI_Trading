import backtrader as bt

class ThreeCandlesIntraday(bt.Strategy):
    params = (
        ('risk_per_trade', 0.02),
        ('atr_period', 14),
        ('tp_ratio', 1.5),
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
        ('volume_threshold', 1.2),  # volume > media * 1.2
        ('trend_filter', True),     # usa SMA 200 come filtro trend
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.sma_trend = bt.indicators.SMA(self.data.close, period=200)
        self.volume_avg = bt.indicators.SMA(self.data.volume, period=20)
        self.trade_count = 0

    def log(self, txt):
        dt = self.datas[0].datetime.datetime(0)
        print(f'{dt} {txt}')

    def notify_trade(self, trade):
        if trade.isclosed:
            pnl = trade.pnlcomm
            self.trade_count += 1
            self.log(f'TRADE #{self.trade_count} PNL: {pnl:.2f} | CAPITAL: {self.broker.getvalue():.2f}')

    def next(self):
        if len(self.data) < 3:
            return

        # Pattern 3 candele consecutive
        c1, c2, c3 = self.data.close[-3], self.data.close[-2], self.data.close[-1]
        o1, o2, o3 = self.data.open[-3], self.data.open[-2], self.data.open[-1]

        if c1 > o1 and c2 > o2 and c3 > o3:
            bias = 1
        elif c1 < o1 and c2 < o2 and c3 < o3:
            bias = -1
        else:
            bias = 0

        # Filtri
        if bias != 0:
            # 1. Volume > media 20 * threshold
            if self.data.volume[0] < self.volume_avg[0] * self.params.volume_threshold:
                self.log(f'Volume troppo basso: {self.data.volume[0]:.0f} < {self.volume_avg[0]*self.params.volume_threshold:.0f}')
                return

            # 2. RSI (non ipercomprato/venduto)
            if bias == 1 and self.rsi[0] > self.params.rsi_overbought:
                self.log(f'RSI ipercomprato: {self.rsi[0]:.2f}')
                return
            if bias == -1 and self.rsi[0] < self.params.rsi_oversold:
                self.log(f'RSI ipervenduto: {self.rsi[0]:.2f}')
                return

            # 3. Trend filter (prezzo sopra SMA 200 per BUY, sotto per SELL)
            if self.params.trend_filter:
                if bias == 1 and self.data.close[0] < self.sma_trend[0]:
                    self.log(f'Prezzo sotto SMA200: {self.data.close[0]:.5f} < {self.sma_trend[0]:.5f}')
                    return
                if bias == -1 and self.data.close[0] > self.sma_trend[0]:
                    self.log(f'Prezzo sopra SMA200: {self.data.close[0]:.5f} > {self.sma_trend[0]:.5f}')
                    return

        # Entry
        if not self.position and bias != 0:
            price = self.data.close[0]
            sl = price - self.params.tp_ratio * self.atr[0] if bias == 1 else price + self.params.tp_ratio * self.atr[0]
            tp = price + self.params.tp_ratio * abs(price - sl) if bias == 1 else price - self.params.tp_ratio * abs(price - sl)
            size = int(self.broker.get_cash() * self.params.risk_per_trade / (abs(price - sl) + 0.0001))

            if bias == 1:
                self.buy(size=size)
                self.log(f'LONG @ {price:.5f} SL {sl:.5f} TP {tp:.5f}')
            else:
                self.sell(size=size)
                self.log(f'SHORT @ {price:.5f} SL {sl:.5f} TP {tp:.5f}')

        # Exit
        if self.position:
            if self.position.size > 0:
                if self.data.close[0] <= self.position.price - self.atr[0]:
                    self.close()
                    self.log(f'CLOSE LONG @ {self.data.close[0]:.5f}')
            else:
                if self.data.close[0] >= self.position.price + self.atr[0]:
                    self.close()
                    self.log(f'CLOSE SHORT @ {self.data.close[0]:.5f}')
