from flask import Blueprint, Response, send_file
from utils.helpers import get_query_parameters, filtered_query
import csv
from io import StringIO, BytesIO
from datetime import datetime
from openpyxl import Workbook
from flask_login import login_required

export_bp = Blueprint("export", __name__)

@export_bp.route("/export_csv")
@login_required
def export_csv():
    params = get_query_parameters()
    records = filtered_query(**params)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["分類", "金額", "類型", "日期", "備註"])
    for record in records:
        writer.writerow([
            record.category,
            record.amount,
            record.type,
            record.date.strftime("%Y-%m-%d") if record.date else "",
            record.note ])

    response = Response(output.getvalue(), content_type="text/csv")
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@export_bp.route("/export_excel")
@login_required
def export_excel():
    params = get_query_parameters()
    records = filtered_query(**params)
    wb = Workbook()
    ws = wb.active
    ws.title = "收支紀錄表"
    ws.append(["分類", "金額", "類型", "日期", "備註"])
    for record in records:
        ws.append([
            record.category,
            record.amount,
            record.type,
            record.date.strftime("%Y-%m-%d") if record.date else "",
            record.note])
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=filename,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")