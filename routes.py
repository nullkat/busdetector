from datetime import datetime
import os
import uuid

from flask import render_template, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
import journal
import utils
import busdetector
from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/process_image', methods=['POST'])
def process_image():
    image = request.files.get('image')
    if image is None or image.filename == '':
        return jsonify(error='Выберите изображение'), 400
    if not utils.allowed_file(image.filename):
        return jsonify(error='Недопустимый формат файла'), 400
    image_filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(image.filename)}"
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    image.save(image_path)

    result = busdetector.count_buses_on_image(image_path)
    result["image_path"] = image_path
    record = journal.save_record(result)

    return jsonify(
        buses_count=record["buses_count"],
        speed=record["speed"],
        total_time=record["total_time"],
        marked_image_url=f"/marked/{record['id']}",
    )


@app.route('/marked/<int:record_id>')
def marked(record_id):
    return send_file(journal.journal[record_id]["marked_image_path"])


@app.route('/journal')
def journal_download():
    return send_file(journal.export_journal_to_excel(), as_attachment=True, download_name=f"journal_{datetime.now()}.xlsx")