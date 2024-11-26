from flask import Flask, request, jsonify, send_file
from pdf_utils import extract_image_from_pdf
from gpt_utils import find_similar_problem
import os

DEBUG = True

app = Flask(__name__)

# 파일 저장 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/',methods=['GET'])
def index():
    return "Flask API is running. Use /upload_pdf or /retrieve for API calls."

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file name provided'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'success': False, 'message': 'Invalid file type, only PDFs are allowed'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({'success': True, 'file_name': filename}), 200


@app.route('/retrieve', methods=['POST'])
def retrieve_similar():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file name provided'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'success': False, 'message': 'Invalid file type, only PDFs are allowed'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # GPT를 통해 유사 문제 찾기
        page_number, problem_number = find_similar_problem(file_path)

        # PDF에서 찾은 문제를 이미지로 추출
        result_image_path = extract_image_from_pdf(file_path, page_number, problem_number, app.config['OUTPUT_FOLDER'])

        if os.path.exists(result_image_path):
            return send_file(result_image_path, mimetype='image/png')

        return jsonify({'success': False, 'message': 'Result image not found'}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=DEBUG)
