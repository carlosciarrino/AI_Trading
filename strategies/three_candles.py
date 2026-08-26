import backtrader as bt

class ThreeCandles(bt.Strategy):
    params = (
        ('risk_per_trade', 0.02),
        ('atr_period', 14),
        ('tp_ratio', 1.5),
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.bias = 0

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def next(self):
        if len(self.data) < 3:
            return
        c1, c2, c3 = self.data.close[-3], self.data.close[-2], self.data.close[-1]
        o1, o2, o3 = self.data.open[-3], self.data.open[-2], self.data.open[-1]
        if c1 > o1 and c2 > o2 and c3 > o3:
            self.bias = 1
        elif c1 < o1 and c2 < o2 and c3 < o3:
            self.bias = -1
        else:
            self.bias = 0

        if not self.position and self.bias != 0:
            price = self.data.close[0]
            stop = price - (1.5 * self.atr[0]) if self.bias == 1 else price + (1.5 * self.atr[0])
            tp = price + (self.params.tp_ratio * abs(price - stop)) if self.bias == 1 else price - (self.params.tp_ratio * abs(price - stop))
            size = int(self.broker.get_cash() * self.params.risk_per_trade / (abs(price - stop) + 0.0001))
            if self.bias == 1:
                self.buy(size=size)
                self.log(f'LONG @ {price:.5f} SL {stop:.5f} TP {tp:.5f}')
            else:
                self.sell(size=size)
                self.log(f'SHORT @ {price:.5f} SL {stop:.5f} TP {tp:.5f}')

        if self.position:
            if self.position.size > 0:
                if self.data.close[0] <= self.position.price - self.atr[0] or self.data.close[0] >= self.position.price + self.params.tp_ratio * self.atr[0]:
                    self.close()
                    self.log(f'CLOSE LONG @ {self.data.close[0]:.5f}')
            else:
                if self.data.close[0] >= self.position.price + self.atr[0] or self.data.close[0] <= self.position.price - self.params.tp_ratio * self.atr[0]:
                    self.close()
                    self.log(f'CLOSE SHORT @ {self.data.close[0]:.5f}')
