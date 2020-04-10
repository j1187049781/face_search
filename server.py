
import traceback
from flask import Flask, request, jsonify
from Similarity import Similarity

app = Flask(__name__)
sim = Similarity()
@app.route('/find_person', methods=['POST'])
def find_person():
    result = {}
    result['status'] = 1
    try:
        fp = request.files['img']
        person_id,face_sim=sim.find_person(fp)


        data={}
        data['person_id']=person_id
        data['face_sim']=face_sim
        result['data']=data
    except BaseException as e:
        traceback.print_exc()
        result['err'] = "{}".format(e)
        type = 0  # error
        result['status'] = type
    return jsonify(result)

@app.route('/rm_person', methods=['POST'])
def rm_person():
    result = {}
    result['status'] = 1
    try:

        rm_id = request.form['person_id']
        success=sim.rm_person(rm_id)
        data={}
        data['success'] = success
        result['data']=data
    except BaseException as e:
        traceback.print_exc()
        result['err'] = "{}".format(e)
        type = 0  # error
        result['status'] = type
    return jsonify(result)

@app.route('/add_person', methods=['POST'])
def add_person():
    result = {}
    result['status'] = 1
    try:
        fp = request.files['img']
        duplicate_person=request.form['duplicate_person']

        success,person_id=sim.add_person(fp,duplicate_person=duplicate_person)
        data={}
        data['success'] = success
        data['person_id'] = person_id
        result['data']=data
    except BaseException as e:
        traceback.print_exc()
        result['err'] = "{}".format(e)
        type = 0  # error
        result['status'] = type
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)

