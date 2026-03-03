import re
import json


def money_to_float(s):
    return float(s.replace(" ", "").replace(",", "."))



with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()



all_prices = re.findall(r"\d{1,3}(?: \d{3})*,\d{2}", text)



dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = dt_match.group(1) if dt_match else None
time = dt_match.group(2) if dt_match else None



pay_match = re.search(r"(Банковская карта|Наличными|Kaspi|QR)[^\d]*([\d ]+,\d{2})", text)
payment_method = pay_match.group(1) if pay_match else None
payment_amount = money_to_float(pay_match.group(2)) if pay_match else None



total_match = re.search(r"ИТОГО:\s*([\d ]+,\d{2})", text)
total_amount = money_to_float(total_match.group(1)) if total_match else None



item_pattern = re.compile(
    r"(?m)^\s*(\d+)\.\s*\n"
    r"([^\n]+)\n"
    r"([\d,]+)\s*x\s*([\d ]+,\d{2})\n"
    r"([\d ]+,\d{2})\n"
    r"\s*Стоимость\s*\n"
    r"([\d ]+,\d{2})"
)

items = []
calculated_total = 0.0

for m in item_pattern.finditer(text):
    index = int(m.group(1))
    name = m.group(2).strip()
    quantity = float(m.group(3).replace(",", "."))
    unit_price = money_to_float(m.group(4))
    line_total = money_to_float(m.group(6))

    calculated_total += line_total

    items.append({
        "index": index,
        "name": name,
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": line_total
    })



result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "payment_amount": payment_amount,
    "total_amount_from_receipt": total_amount,
    "calculated_total_from_items": round(calculated_total, 2),
    "items": items,
    "all_prices_raw": all_prices
}

print(json.dumps(result, ensure_ascii=False, indent=2))