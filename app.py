from flask import Flask, render_template,jsonify

app = Flask(__name__)
template = 'home.html'
data = {
  'title':'My Blog',
  'year_target':[{
  'id': 0,
  'title': 'Unity 游戏开发',
  'target': 'develop a game by unity'
}, {
  'id': 1,
  'title': 'Blender 模型建模',
  'target': 'build model by blender'
}, {
  'id': 2,
  'title': 'Design Pattern 软件设计模式',
  'target': 'design a program with design pattern '
}]
}


@app.route("/")
def hello_world():
  return render_template(template, data=data)

@app.route("/api/v1/yeartargets")
def year_target():
  return jsonify(data)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
