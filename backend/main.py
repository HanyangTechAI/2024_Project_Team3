from flask import Flask, request, jsonify

# TODO 나중에 환경변수를 받아서 debug 여부를 읽어주기!
DEBUG = True

app = Flask(__name__)

# TODO erase sample POST request code
@app.route('/sample', methods=['POST'])
def example():
    if request.is_json:
        # 들어오는 json payload 를 읽는 부분
        req_data = request.get_json()
        
        # python dictionary type 에서 message 라는 key 가 있으면 반환 하는 부분. 없으면 default 값 반환.
        message = req_data.get('message', 'No message received')
        
        # response 를 JSON 형식으로 구성하는 부분
        response = {
            'message': f"Received message: {message}",
            'success': True
        }
    else:
        # Request 가 json 이 아니면 반환하는 response 구성
        response = {
            'message': 'Request body must be JSON',
            'success': False
        }
    
    # python dictionary type 을 json 으로 변환하여 반환
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=DEBUG)
