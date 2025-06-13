from flask import Blueprint, render_template, request, abort, url_for
from werkzeug.utils import redirect
from utils.report_service import get_summary_data
from models import Expense, Session
from utils.helpers import get_query_parameters, filtered_query
from datetime import datetime
from flask_login import current_user, login_required

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/expenses", methods = ["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")
        type_ = request.form.get("type")
        date = request.form.get("date")
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        note = request.form.get("note")
    #建立資料並加入資料庫
        with Session() as session:
            new_expense = Expense(user_id = current_user.id, category = category, amount = int(amount), type = type_, date = date_obj, note = note)
            session.add(new_expense)
            session.commit()
    #資料送出後重新導向(避免重新整理又送一次)
        return redirect("/expenses")
    params = get_query_parameters()
    records = filtered_query(**params)
    summary = get_summary_data(records)

    return render_template("expenses.html", expenses = records, params = params, summary = summary)


@expense_bp.route("/expenses/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    with Session() as session:
        record = session.get(Expense, id)
        if record is None or record.user_id != current_user.id:
            abort(403)  # 資料不存在或不是你的資料

        if request.method == "POST":
            # 使用者送出修改
            record.category = request.form.get("category")
            record.amount = int(request.form.get("amount"))
            record.type = request.form.get("type")
            date = request.form.get("date")
            record.date = datetime.strptime(date, "%Y-%m-%d")
            record.note = request.form.get("note")
            session.commit()
            return redirect(url_for("expense.expense"))

        # 顯示原本的資料給使用者編輯
        return render_template("edit_expense.html", expense=record)


@expense_bp.route("/expenses/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_expense(id):
    with Session() as session:
        record = session.get(Expense, id)
        if record is None or record.user_id != current_user.id:
            abort(403)
        if request.method == "POST":
            session.delete(record)
            session.commit()
            return redirect(url_for("expense.expense"))
        return render_template("confirm_delete.html", expense=record)
