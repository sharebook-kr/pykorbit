import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pykorbit


class OrderbookWorker(QThread):
    def run(self):
        orderbook = pykorbit.get_orderbook("BTC")
        print(orderbook)

class PriceWorker(QThread):
    def run(self):
        price = pykorbit.get_current_price("BTC")
        print(price)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.price_worker = PriceWorker()
        self.orderbook_workder = OrderbookWorker()

        price_timer = QTimer(self)
        price_timer.start(1000)
        price_timer.timeout.connect(self.price_timer_timeout)

        orderbook_timer = QTimer(self)
        orderbook_timer.start(85)
        orderbook_timer.timeout.connect(self.orderbook_timer_timeout)

    def price_timer_timeout(self):
        self.price_worker.start()

    def orderbook_timer_timeout(self):
        self.orderbook_workder.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow ()
    win.show()
    app.exec_()
