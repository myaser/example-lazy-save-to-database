from flask import request, jsonify

from .utils import allowed_file
from .jobs import process_file


def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'message': 'un supported file type'}), 400

    process_file.queue(file.stream)
    return jsonify({'message': 'we are processing your file'}), 201
