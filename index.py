from flask import Flask, render_template, request
from flask_fontawesome import FontAwesome

from chatbot import *

app = Flask(__name__)
fa = FontAwesome(app)

def split(word): 
    return [char for char in word]  

def format_output(out):
   out = out.replace(" .", ".")
   out = out.replace(" ,", ",")
   out = out.replace(" :", ":")
   out = out.replace(" !", "!")
   out = out.replace(" ?", "?")
   capitalize = [".", "!", "?"]

   rs = split(out)
   for i in range(len(out)):
      if i < len(out) - 2 and out[i] in capitalize:
         rs[i+2] = out[i+2].upper()
   
   rs[0] = rs[0].upper()
   rs = "".join(rs).strip()
   if rs[-1] not in capitalize:
      rs += "."
   return rs

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
      
      return {"text": format_output(out), "emo_text": emo_text}

@app.route("/keep_conversation_chatbot", methods = ["POST"])
def keep_conversation_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().split("-")
      n2 = request.form["n2"].lower().split("-")
      out = revert_sentence(keep_conversation(request.form["emo_text"]), n2[0], n2[1])
      return format_output(out)

@app.route("/bye_chatbot", methods = ["POST"])
def bye_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().split("-")
      n2 = request.form["n2"].lower().split("-")
      out = revert_sentence(bye_user(), n2[0], n2[1])
      return format_output(out)

@app.route("/hello_chatbot", methods = ["POST"])
def hello_chatbot():
   out = first_greet()
   return format_output(out)

if __name__ == '__main__':
   app.run(debug = False)