import io
import json
import os
from datetime import datetime

from openpyxl import Workbook
from config import JOURNAL_FILE

if os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "r") as f:
        journal = json.load(f)
else:
    journal = []


def save_record(record: dict) -> dict:
    record = dict(record)
    time = record.get("detection_time")
    if isinstance(time, datetime):
        record["detection_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    record["id"] = len(journal)
    journal.append(record)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f)
    return record

def export_journal_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Журнал"
    ws.append([
        "№ изображения", "Дата и время", "Автобусов",
        "Предобработка, мс", "Инференс, мс", "Постобработка, мс", "Всего, мс"
    ])
    for r in journal:
        speed = r.get("speed", {})
        ws.append([
            r["id"], r.get("processed_at"), r["buses_count"],
            speed.get("preprocess"), speed.get("inference"), speed.get("postprocess"),
            r.get("total_time")
        ])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer