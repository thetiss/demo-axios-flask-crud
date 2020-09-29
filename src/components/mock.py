# -*- coding: utf-8 -*-
# @Author: DJ
# @Date:   2020-09-24 17:59:00
# @Last Modified by:   DJ
# @Last Modified time: 2020-09-24 18:02:30
#!/usr/bin/python3
# -*-coding: utf-8-*-

from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["DEBUG"] = True
#logging.getLogger('flask_cors').level = logging.DEBUG

CORS(app)

tutorial_arr = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'published': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'published': False
    }
]


@app.route('/', methods=['GET', 'POST'])
def hello():
   # print("Wep api by Flask")
    return 'Hello, Wep API by Flask!'

# Tutorial
# 返回所有


@app.route('/tutorials', methods=['GET'])
def getJson():
    if request.method == 'GET':
        return jsonify({'data': tutorial_arr})

# 根据Id,查找


@app.route('/tutorials/<int:id>', methods=['GET', 'POST'])
def getTutorial(id):
    if request.method == 'GET':
        tutorial = [task for task in tutorial_arr if task['id'] == id]
        print(tutorial)
        # tutorial = filter(
        #     lambda tutorial_arr: tutorial_arr.id == id, tutorial_arr)
        # if len(tutorial) == 0:
        #     abort(404)

        return jsonify(tutorial[0])
        # return jsonify([tutorial[0]])
   # return jsonify({'data': tutorial[0]})

# 根据id删除tutorial


@app.route('/tutorials/<int:id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def deleteTutorial(id):
    if request.method == 'DELETE':
        tutorial = [task for task in tutorial_arr if task['id'] == id]
        if len(tutorial) == 0:
            abort(404)
        tutorial_arr.remove(tutorial)
    # return jsonify({'result': True})
    return jsonify({tutorial_arr}), 201


@app.route('/api/post', methods=['GET', 'POST'])
def postData():
    if request.method == 'POST':
        username = request.form['name']
        print(username)
        return {'code': 1}

# 新增


@app.route('/tutorials', methods=['POST'])
def createTutorial():
    if request.method == 'POST':
        if not request.json or not 'title' in request.json:
            abort(400)
        tutorial = {
            'id': tutorial_arr[-1]['id']+1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'published': False
        }
        tutorial_arr.append(tutorial)
        return jsonify({'newTutorial': tutorial}), 201
# 根据字段title查找


@app.route('/query', methods=['GET', 'POST'])
def FindTutorialByTitle():
    if request.args:
        # when you curl http://localhost:8008/query?title=text
        # then will display (Query) title:text
        # serialized = ",".join(f"{k}:{v}" for k, v in request.args.items())
        # return f"(Query) {serialized}", 200
        searchTitle = request.args.get("title")
        tutorial = [
            task for task in tutorial_arr if task['title'] == searchTitle]
        return jsonify({'data': tutorial})
        # return f"(Query) {searchTitle}", 200
    else:
        return "Opoos…………No query string received", 200


if __name__ == '__main__':
    app.run(port=8008)
