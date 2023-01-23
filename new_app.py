from flask import Flask, request, render_template
from celery_working import add
import al_db
import models_db
from sqlalchemy import select
from sqlalchemy.orm import Session

app = Flask(__name__)
from database_function import DataBaseManager, generate_data


@app.route("/", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        with Session(al_db.engine) as session:
            query = select(models_db.Currency)
            result = session.execute(query).fetchall()
        return str(result)
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

        with Session(al_db.engine) as session:
            statement_1 = select(models_db.Currency).filter_by(bank=user_bank,
                                                               currency=user_currency_1,
                                                               date_exchange=user_date)
            currency_1 = session.scalars(statement_1).first()

            statement_2 = select(models_db.Currency).filter_by(bank=user_bank,
                                                               currency=user_currency_2,
                                                               date_exchange=user_date)
            currency_2 = session.scalars(statement_2).first()

        buy_rate_1, sale_rate_1 = currency_1.buy_rate, currency_1.sale_rate
        buy_rate_2, sale_rate_2 = currency_2.buy_rate, currency_2.sale_rate
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
