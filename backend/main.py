from flask import Flask, request, jsonify, send_file
import os

# TODO 나중에 환경변수를 받아서 debug 여부를 읽어주기!
DEBUG = True

app = Flask(__name__)

# 파일 저장 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message':'No file provided in request'}), 400
    
    file = request.files['file']

    # 파일명이 비어있는지 확인
    if file.filename == '':
        return jsonify({'success': False, 'message':'No file name provided'}), 400

    # 파일명이 '.pdf'로 끝나는지 확인
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'file_name': filename}), 200
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'success': False, 'message': 'Invalid file type, only PDFs are allowed'}), 400
    
    return jsonify({'success': False, 'message': 'Unknown error occurred'}), 500
    
    # TODO 파일명 중복 시 처리 로직 추가, 파일명 안전성 검사 추가, 실제로 PDF 파일인지 확인하는 로직 추가


@app.route('/retrieve', methods=['POST'])
def retrieve_similar():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']

    # 파일명이 비어있는지 확인
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    # 이미지 파일이 맞는지 확인 (예: JPG, PNG 등)
    if file and (file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endswith('.png')):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 외부 함수에서 비슷한 문제 이미지를 검색
        result_image_path = find_similar_problem_image(file_path)

        # 이미지 전송
        if os.path.exists(result_image_path):
            return send_file(result_image_path, mimetype='image/png')

        return jsonify({'success': False, 'message': 'Result image not found'}), 500
    else:
        return jsonify({'success': False, 'message': 'Uploaded file is not a supported image format'}), 400


# TODO GPT 모델을 사용하여 비슷한 문제 이미지를 찾는 함수 구현
def find_similar_problem_image():
    # 저장해둔 PDF와 문제 이미지를 GPT에게 넘겨, 유사한 문제의 페이지와 번호 받기.
    # 페이지와 번호를 바탕으로 PDF에서 문제의 이미지를 추출하거나, 번호를 반환.
    return 'result.png'

if __name__ == '__main__':
    app.run(debug=DEBUG)
