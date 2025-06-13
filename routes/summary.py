from flask import Blueprint, render_template
from utils.report_service import get_category_summary
from utils.helpers import get_query_parameters, filtered_query
from flask_login import login_required

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/summary")
@login_required
def summary():
    params = get_query_parameters()
    records = filtered_query(**params)
    summary_by_category = get_category_summary(records)
    total_income = sum(data['income'] for data in summary_by_category.values())
    total_expense = sum(data['expense'] for data in summary_by_category.values())
    return render_template("summary.html", summary=summary_by_category, params=params, total_income = total_income, total_expense = total_expense)

