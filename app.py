from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.lovecode


# HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# post 테스트
@app.route('/test', methods=['POST'])
def save_test():
    test_receive = request.form['test_give']
    db.test.insert_one({'input': test_receive})
    msg = test_receive + " 저장 성공"
    return jsonify({'result': 'success', 'msg': msg})


# 저장하기(POST) API
@app.route('/dialog', methods=['POST'])
def save_dialog():
    name_receive = request.form['name_give']
    image_receive = request.form['image_give']
    grade_receive = request.form['grade_give']
    greeting_receive = request.form['greeting_give']
    thema_receive = request.form['thema_give']

    answer = "이풀잎 : 오 문과구나! 안녕! 나 지금은 빨리 수업가야해서 연락할게!"
    some = True

    if greeting_receive == "2":
        answer = "갑자기? ㅎㅎ"
        some = False

    if greeting_receive == "1":
        answer = "당연히 알지! 문과잖아!"

    if thema_receive == "MBTI" or thema_receive == "mbti":
        answer = "오 나는 intp야! 너는?"

    if grade_receive == "1" or grade_receive == "2":
        answer = "이풀잎 : 선배님, 아직도 학교에 계세요?"
        some = False

    doc = {
        'name': name_receive,
        'image': image_receive,
        'grade': grade_receive,
        'greeting': greeting_receive,
        'thema': thema_receive,
        'some': some
    }
    db.dialogs.insert_one(doc)

    return jsonify({'result': 'success', 'msg': answer})


# 기쟈오기(Read) API
@app.route('/dialog', methods=['GET'])
def view_dialogs():
    dialogs = list(db.dialogs.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'dialogs': dialogs})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)