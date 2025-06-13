from flask import request
from models import Expense, Session
from datetime import datetime
from flask_login import current_user

def get_query_parameters():
    category = request.args.get("category")
    type_ = request.args.get("type")
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc")    #預設升冪排序

    return {
        "category" : category,
        "type_" : type_,
        "start_date" : start_date,
        "end_date" : end_date,
        "sort_by" : sort_by,
        "order" : order,
        "user_id" : current_user.id
    }


def filtered_query(category = None, type_ = None, start_date = None, end_date = None, sort_by = None, order = "asc", user_id = None):
    with Session() as session:
        query = session.query(Expense)

        if user_id is not None:
            query = query.filter(Expense.user_id == user_id)
        if category:
            query = query.filter(Expense.category == category)
        if type_:
            query = query.filter(Expense.type == type_)
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Expense.date >= start_dt)
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Expense.date <= end_dt)
        if sort_by == "amount":
            if order == "desc":
                query = query.order_by(Expense.amount.desc())
            else:
                query = query.order_by(Expense.amount.asc())
        elif sort_by == "date":
            if order == "desc":
                query = query.order_by(Expense.date.desc())
            else:
                query = query.order_by(Expense.date.asc())
        return query.all()

