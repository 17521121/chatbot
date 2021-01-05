from flask import Flask, render_template, request
from flask_fontawesome import FontAwesome
# from flask_ngrok import run_with_ngrok
from chatbot import *

app = Flask(__name__)
fa = FontAwesome(app)
# run_with_ngrok(app)

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

list_n1 = ["tôi", "tao", "tớ", "tui", "t", "mình", "tau"]
list_n2 = ["mày", "cậu", "m", "bạn", "mi", "mầy", "bồ"] 

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/chat', methods = ['POST'])
def chat():
   if request.method == 'POST':

      n1 = request.form["n1"].lower().strip()
      n2 = request.form["n2"].lower().strip()
      chat_text = request.form["chat_text"]
      chat_text = preprocess_pronoun(chat_text) # tiền xử lí trước khi nhận diện

      # cho revert
      _n1 = None 
      _n2 = None 

      # phân tích ra n1 n2
      if n1 == "-": # chưa có đại từ
         _n1, _n2 = get_n1n2(chat_text)
         if _n1 in list_n1 or _n2 in list_n2: # ngang hàng
            n1 = _n1
            n2 = _n2
         else: # chênh thứ bậc xã hội
            n1 = _n2
            n2 = _n1
      else:
         # đã có đại từ rồi
         if n1 in list_n1 or n2 in list_n2: # ngang hàng
            _n1 = n1
            _n2 = n2
         else: # chênh thứ bậc xã hội
            _n1 = n2
            _n2 = n1

      chat_text = convert_sentence(chat_text, n1, n2)

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
      out = revert_sentence(out, _n1, _n2) 
      with open("test.txt", "a", encoding="utf-8") as myfile:
         myfile.write(chat_text + "\t" + format_output(out)+"\n")
      return {"text": format_output(out), "emo_text": emo_text, "n1": n1, "n2": n2}

@app.route("/keep_conversation_chatbot", methods = ["POST"])
def keep_conversation_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().strip()
      n2 = request.form["n2"].lower().strip()
      if n1 in list_n1 or n2 in list_n2: # ngang hàng
         _n1 = n1
         _n2 = n2
      else: # chênh thứ bậc xã hội
         _n1 = n2
         _n2 = n1
      out = revert_sentence(keep_conversation(request.form["emo_text"]), _n1, _n2)
      return format_output(out)

@app.route("/bye_chatbot", methods = ["POST"])
def bye_chatbot():
   if request.method == 'POST':
      n1 = request.form["n1"].lower().strip()
      n2 = request.form["n2"].lower().strip()
      if n1 in list_n1 or n2 in list_n2: # ngang hàng
         _n1 = n1
         _n2 = n2
      else: # chênh thứ bậc xã hội
         _n1 = n2
         _n2 = n1
      out = revert_sentence(bye_user(), _n1, _n2)
      return format_output(out)

@app.route("/hello_chatbot", methods = ["POST"])
def hello_chatbot():
   out = first_greet()
   return format_output(out)


app.run()