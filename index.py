from flask import Flask, render_template, request
from flask_fontawesome import FontAwesome

from chatbot import *

app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/chat', methods = ['POST'])
def chat():
   if request.method == 'POST':
      n1 = request.form["n1"]
      n1 = request.form["n2"]
      chat_text = request.form["chat_text"]
      outs = predict(chat_text, top_n = 10, normalize = option.normalize)
      return clean_answer(outs)

if __name__ == '__main__':
   app.run(debug = True)