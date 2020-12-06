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
      n1 = request.form["n1"].lower().split("-")
      n2 = request.form["n2"].lower().split("-")
      chat_text = request.form["chat_text"]
      chat_text = convert_sentence(chat_text, n1[0], n1[1])
      outs = predict(chat_text, top_n = 3, normalize = option.normalize)
      out, emo_text = clean_answer(outs)
      out = revert_sentence(out, n2[0], n2[1]) 
      out = '. '.join(i.capitalize() for i in out.split(' . '))
      return {"text": out, "emo_text": emo_text}

if __name__ == '__main__':
   app.run(debug = False)