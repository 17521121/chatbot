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
      # nếu join | thì sao mà biết hello đc 
         # không dùng lịch sử nên tạm thời chấp nhận đoạn này
      if chat_text  in user_hello:
         out = hello_user()
         emo_text = "sentimental"
      elif chat_text in user_say_bye:
         out = bye_user()
         emo_text = "sentimental"
      else:
         # chat_text đã join |
         outs = predict(chat_text, top_n = 3, normalize = option.normalize)
         out, emo_text = clean_answer(outs)
      out = revert_sentence(out, n2[0], n2[1]) 
      out = '. '.join(i.capitalize() for i in out.split(' . '))
  
      return {"text": out, "emo_text": emo_text}

@app.route("/keep_conversation_chatbot", methods = ["POST"])
def keep_conversation_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().split("-")
      n2 = request.form["n2"].lower().split("-")
   return revert_sentence(keep_conversation(request.form["emo_text"]), n2[0], n2[1])

@app.route("/bye_chatbot", methods = ["POST"])
def bye_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().split("-")
      n2 = request.form["n2"].lower().split("-")

   return revert_sentence(bye_user(), n2[0], n2[1])

@app.route("/hello_chatbot", methods = ["POST"])
def hello_chatbot():
   return first_greet()

if __name__ == '__main__':
   app.run(debug = False)