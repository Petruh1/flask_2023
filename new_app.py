from flask import Flask, request, render_template
from celery_working import add
from database_function import DataBaseManager
import al_db
import models_db
from sqlalchemy import select

app = Flask(__name__)
from database_function import DataBaseManager, generate_data


@app.route("/", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        al_db.init_db()
        conn = al_db.engine.connect()
        res1 = select([models_db.User])
        result = conn.execute(res1)
        data_res = result.fetchall()
        print(result)
    else:
        pass
    return "<p>Login!</p>"


@app.route("/logout", methods=["GET"])
def logout_user():
    add.apply_async(args=(4, 5))
    return "<p>Logout!</p>"


@app.route("/register", methods=["GET", "POST"])
def register_user():
    return "Registration form"


@app.route("/user_page", methods=["GET"])
def user_access():
    return "More functions"


@app.route("/currency", methods=["GET", "POST"])
def currency_converter():
    if request.method == 'POST':
        user_bank = request.form["bank"]
        user_currency_1 = request.form["currency_1"]
        user_currency_2 = request.form["currency_2"]
        user_date = request.form["date"]

        with DataBaseManager() as db:
            buy_rate_1, sale_rate_1 = db.get_result(
                f'SELECT buy_rate, sale_rate FROM currency WHERE bank="{user_bank}" and date_exchange="{user_date}" and currency="{user_currency_1}"'
            )
            buy_rate_2, sale_rate_2 = db.get_result(
                f'SELECT buy_rate, sale_rate FROM currency WHERE bank="{user_bank}" and date_exchange="{user_date}" and currency="{user_currency_2}"'
            )

        cur_exchange_buy = buy_rate_2 / buy_rate_1
        cur_exchange_sale = sale_rate_2 / sale_rate_1
        return render_template("data_form.html", cur_exchange_buy=cur_exchange_buy,
                               user_currency_1=user_currency_1, user_currency_2=user_currency_2,
                               cur_exchange_sale=cur_exchange_sale)
    else:
        return render_template("data_form.html")


generate_data()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
