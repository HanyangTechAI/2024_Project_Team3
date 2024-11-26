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

@app.route('/', methods=['GET'])
def index():
    return "Flask API가 실행 중입니다. /api/upload 엔드포인트를 사용하세요."

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'files' not in request.files:
        return jsonify({'success': False, 'message': '파일이 제공되지 않았습니다.'}), 400

    files = request.files.getlist('files')  # 여러 파일 처리
    results = []

    for file in files:
        if file.filename == '':
            return jsonify({'success': False, 'message': '파일 이름이 없습니다.'}), 400

        if not file.filename.endswith('.pdf'):
            return jsonify({'success': False, 'message': f"{file.filename}은(는) 유효하지 않은 파일 형식입니다. PDF만 허용됩니다."}), 400

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # GPT로 유사 문제 찾기
            page_number, problem_number = find_similar_problem(file_path)

            # 해당 문제를 이미지로 추출
            result_image_path = extract_image_from_pdf(file_path, page_number, problem_number, app.config['OUTPUT_FOLDER'])

            if os.path.exists(result_image_path):
                results.append({
                    'file': filename,
                    'success': True,
                    'result_image': result_image_path
                })
            else:
                results.append({
                    'file': filename,
                    'success': False,
                    'message': '결과 이미지를 찾을 수 없습니다.'
                })

        except Exception as e:
            results.append({'file': filename, 'success': False, 'message': str(e)})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=DEBUG)
