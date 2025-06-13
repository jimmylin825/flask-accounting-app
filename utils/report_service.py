from collections import defaultdict

def get_summary_data(records):
    total_income = 0
    total_spend = 0
    for record in records:
        if record.type == "income":
            total_income += record.amount
        elif record.type == "expense":
            total_spend += record.amount
    net_gross = total_income - total_spend
    rate = round(total_spend / total_income * 100, 2) if total_income > 0 else 0

    return {
        "total_income" : total_income,
        "total_spend" : total_spend,
        "net_gross" : net_gross,
        "rate" : rate
    }

def get_category_summary(records):
    summary = defaultdict(lambda: {"income": 0, "expense": 0})
    total_sum = 0
    for record in records:
        if record.type == "income":
            summary[record.category]["income"] += record.amount
        elif record.type == "expense":
            summary[record.category]["expense"] += record.amount
    # 加上 total 與 rate 欄位
    for cat, values in summary.items():
        total = values["income"] + values["expense"]
        summary[cat]["total"] = total
        total_sum += total  # 為了稍後算百分比

    for cat, values in summary.items():
        values["rate"] = round((values["total"] / total_sum * 100), 1) if total_sum > 0 else 0

    return dict(summary)