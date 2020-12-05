from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
   yourarg = request.args.get('user')
   return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
   yourarg = flask.request.args.get('')
   if request.method == 'POST':
      result = request.form
      return render_template("result.html", result = result)

if __name__ == '__main__':
   app.run(debug = True)