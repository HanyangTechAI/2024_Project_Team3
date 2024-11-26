from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pdf_utils import extract_image_from_pdf
from gpt_utils import find_similar_problem
import os
import mimetypes  # 파일 MIME 타입 확인에 사용

DEBUG = True

app = Flask(__name__)
CORS(app)

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

        # 파일 확장자 또는 MIME 타입 확인
        mime_type, _ = mimetypes.guess_type(file.filename)

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 파일 유형에 따라 처리 분기
        if mime_type == 'application/pdf':  # PDF 파일 처리
            try:
                # GPT로 유사 문제 찾기
                page_number, problem_number = find_similar_problem(file_path)

                # 해당 문제를 이미지로 추출
                result_image_path = extract_image_from_pdf(file_path, page_number, problem_number, app.config['OUTPUT_FOLDER'])

                if os.path.exists(result_image_path):
                    results.append({
                        'file': filename,
                        'type': 'pdf',
                        'success': True,
                        'result_image': result_image_path
                    })
                else:
                    results.append({
                        'file': filename,
                        'type': 'pdf',
                        'success': False,
                        'message': '결과 이미지를 찾을 수 없습니다.'
                    })

            except Exception as e:
                results.append({'file': filename, 'type': 'pdf', 'success': False, 'message': str(e)})

        elif mime_type and mime_type.startswith('image/'):  # 이미지 파일 처리
            try:
                # 이미지 파일 저장 처리 (추가 작업 가능)
                results.append({
                    'file': filename,
                    'type': 'image',
                    'success': True,
                    'message': '이미지 파일이 성공적으로 처리되었습니다.'
                })
            except Exception as e:
                results.append({'file': filename, 'type': 'image', 'success': False, 'message': str(e)})

        else:
            results.append({
                'file': filename,
                'type': 'unknown',
                'success': False,
                'message': f"지원되지 않는 파일 형식입니다: {mime_type}"
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=DEBUG)
