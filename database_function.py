import datetime
import sqlite3


class DataBaseManager:
    def __enter__(self):
        self.con = sqlite3.connect("currency.db")
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()

    def get_result(self, query):
        res1 = self.cur.execute(query)
        result = res1.fetchone()
        return result

    def write_data(self, query):
        self.cur.execute(query)
        self.con.commit()


def generate_data():
    data = [
        {"bank": "A1", "currency": "UAH", "buy_rate": 0.95, "sale_rate": 1},
        {"bank": "A1", "currency": "EUR", "buy_rate": 0.95, "sale_rate": 1},
        {"bank": "A1", "currency": "USD", "buy_rate": 0.95, "sale_rate": 1},
        {"bank": "A1", "currency": "GPB", "buy_rate": 0.95, "sale_rate": 1}
    ]

    date_exchange = datetime.datetime.now().strftime("%Y-%m-%d")

    with DataBaseManager() as db:
        for i in data:
            bank = i["bank"]
            currency = i["currency"]
            buy_rate = i["buy_rate"]
            sale_rate = i["sale_rate"]
            query = f'INSERT INTO currency (bank, currency, date_exchange, buy_rate, sale_rate) VALUES ("{bank}", "{currency}", "{date_exchange}", {buy_rate}, {sale_rate})'
            if query:
                db.write_data(query)
