from googletrans import Translator
translator = Translator()

# bạn, mình, xin chào
detect_high_frequent_phrase = "bạn bè, bè bạn, bạn hàng, người bạn, bạn gái, bạn trai, bạn xã giao,\
bạn học, bạn đọc, đám bạn, cô bạn, anh bạn, nhỏ bạn, ông bạn,\
bạn trẻ, bạn già, bạn tù, tụi bạn, trở thành bạn, bạn thân, bạn tôi,\
bạn mình, nhóm bạn, kết bạn, tìm bạn, tình bạn,\
nhiều bạn, ít bạn, vài bạn, nhà bạn, bạn ấy, bạn nhóc, bạn đó, bạn nhỏ,\
bạn cùng, bạn chí cốt, bạn của, thằng bạn, đứa bạn,\
bực mình, đầy mình, rùng mình, giữ mình, chuyển mình, trở mình, của mình, giật mình,\
biết mình, bầm mình, hoà mình, dân mình, người mình, dân tộc mình, người việt mình,\
hoàn thiện mình, đời mình, giấu mình, một mình, uốn mình, xuôi mình, buông mình, tự mình,\
mình mẩy, hết mình, nghiêng mình, liều mình, về mình, con mình, chồng mình, vợ mình,\
con gái, con trai, con chó, con mèo, con dâu, con rể,\
xin chào, ba mẹ, cha mẹ, anh chị, anh chị em, ông bà, vợ chồng, chồng vợ, cô chú, chú bác, thầy cô, mẹ cha, cô thầy"
detect_high_frequent_phrase = detect_high_frequent_phrase.replace(", ", ",").split(",")


# N là list đại từ phân cấp bậc
N = 'bác, cháu, anh, chị, em, con, ba, mẹ, bố, cha,\
tía, u, thầy, bé, chú, cô, ông, bà, dì,\
dượng, thím, vợ, chồng'
N = N.replace(", ", ",").split(",")
N = list(set(N))

eng_pronoun = [
    "you've","i've","you'll", "i'll", "we've", "we'll" ,'you','i', "i'm", "me", "your", "mine", "yours", "my", 'we', "us", 'our', 'ours',
    'mom','uncle','man','parents','honey','baby', 'mother', "husband", "kid", "u"
    'children', "aunt", "brother", "sister", "mommy", "mother", "father", "dad", "daddy",
    "grandchildren", "grandmother", "stepfather", "he" , "she", "her", "his", "him", "hers", "mr",
    "miss", "aunt", "teacher", "sister", "wife", "Father","Boss"
]

cap_daitu_nganghang = [
    ["tôi", "bạn"],
    ["tôi", "cậu"],
    ["tao", "mày"],
    ["tao", "mầy"],
    ["tao", "bồ"],
    ["tao", "mi"],
    ["tớ", "cậu"],
    ["tớ", "bạn"],
    ["tớ", "bồ"],
    ["tui", "bạn"],
    ["tui", "mi"],
    ["tui", "mầy"],
    ["tui", "bồ"],
    ["t", "m"],
    ["t", "bồ"],
    ["t", "mày"],
    ["t", "cậu"],
    ["t", "mầy"],
    ["t", "mi"],
    ["t", "bạn"],
    ["mình", "bạn"],
    ["mình", "cậu"],
    ["mình", "bồ"],
    ["tau", "mi"],
    ["tau", "m"],
    ["tau", "mầy"],
    ["tau", "mày"],
]
cap_daitu_phancap = [
    ["vợ", "chồng"],
    ["cô", "cháu"],
    ["thầy", "cháu"],
    ["ông", "cháu"],
    ["anh", "em"],
    ["chị", "em"],
    ["thím", "cháu"],
    ["tía", "con"],
    ["dượng", "cháu"],
    ["bà", "cháu"],
    ["chú", "cháu"],
    ["bác", "cháu"],
    ["dì", "cháu"],
    ["thím", "con"],
    ["bác", "con"],
    ["ba", "con"],
    ["bà", "con"],
    ["bố", "con"],
    ["mẹ", "con"],
    ["u", "con"],
    ["dượng", "con"],
    ["cha", "con"],
    ["chú", "con"],
    ["cô", "con"],
    ["thầy", "em"],
    ["thầy", "con"],
    ["ông", "con"],
    ["dì", "con"],
    ["u", "cháu"],
]


# list đại từ không phân cấp bậc
list_n1 = ["tôi", "tao", "tớ", "tui", "t", "mình", "tau"]
list_n2 = ["mày", "cậu", "m", "bạn", "mi", "mầy", "bồ"] 

N.extend(list_n1)
N.extend(list_n2)

def preprocess(text, split_sep = " "):
    return (
        text.replace(".", " . ")
        .replace("_comma_", " , ")
        .replace(".  .  .", " ... ")
        .replace(",", " , ")
        .replace(";", " ; ")
        .replace(":", " : ")
        .replace("'", " ' ")
        .replace("''", " \" ")
        .replace("!", " ! ")
        .replace("?", " ? ")
        .replace('-', ' - ')
        .replace("  ", " ")
        .replace("  ", " ")
        .strip()
        .lower()
    )
    
def get_n1n2(input, xuat_translated = False, xuat_token = False):
    try:
        input = preprocess(input)
        sentence = translator.translate(input, dest ='en').text

        for i in detect_high_frequent_phrase:
            input = input.replace(i, "_".join(i.split(" ")))
        
        vi_tokens = input.split()
        vi_results = []

        # kiểm tra các đại từ ngang hàng
        _n1 = set()
        _n2 = set()
        for i in vi_tokens:
            if i in list_n1:
                _n1.add(i)
            if i in list_n2:
                _n2.add(i)

        if len(_n1) > 1:
            _n1.discard("mình")
        if len(_n1) > 1:
            _n1.discard("ta")
        if len(_n2) > 1:
            _n1.discard("bạn")
        if len(_n2) > 1:
            _n1.discard("bồ")

        _n1 = list(_n1)
        _n2 = list(_n2)
        if (len(_n1) == 1 and len(_n2) == 1):
            return _n1[0], _n2[0]
        if (len(_n1) == 1 and len(_n2) == 0):
            return _n1[0], None
        if (len(_n1) == 0 and len(_n2) == 1):
            return None, _n2[0]
        
        # kết thúc kiểm tra đại từ ngang hàng
        
        sentence = sentence.replace('.', ' . ')
        sentence = sentence.replace(',', ' , ')
        sentence = sentence.replace('!', ' ! ')
        sentence = sentence.replace("?", " ? ")
        sentence = sentence.replace('-', ' - ')
        sentence = sentence.replace('  ', ' ')
        sentence = sentence.replace('  ', ' ')

        if xuat_translated:
            print("eng: ", sentence)
        en_tokens = sentence.lower().split()
        en_results = []

        for i, token in enumerate(en_tokens):
            if token in eng_pronoun and token not in en_results:
                en_results.append(token)
        for i, token in enumerate(vi_tokens):
            if token in N and token not in vi_results :
                vi_results.append(token)

        if xuat_token:
            print(vi_results)
            print(en_results)

        n1 = n2 = None
        if len(vi_results) > 0:

            # chào hỏi
            for it, vi_token in enumerate(vi_tokens):
                if vi_token in ["chào", "hi", "hello", "xin_chào"]:
                    if it < len(vi_tokens) - 2  and vi_tokens[it + 1] in N:
                        n2 = vi_tokens[it + 1]
                    if it > 0 and vi_tokens[it - 1] in N:
                        n1 = vi_tokens[it-1]
                    break
            if n1 != None or n2 != None:
                return n1, n2
            # end chào hỏi
            
            elif len(en_results) > 0:
                # kiểm tra đầu
                if en_results[0] in ["i've",'i', "i'm", 'me', 'mine','we','us', 'ours', "i'll", "we've", "we'll"]:
                    n1 = vi_results[0]

                elif en_results[0] in ["my", "our"] and len(en_results) > 1 and en_results[1] in eng_pronoun and len(vi_results) > 1: # sở hữu, vd: dì của tôi
                    n1 = vi_results[1]
                
                elif en_results[0] in ["you", "yours", "you've", "you'll"]:
                    n2 = vi_results[0]

                elif en_results[0] in ["your"] and len(en_results) > 1 and en_results[1] in eng_pronoun and len(vi_results) > 1: # sở hữu, vd: dì của bạn
                    n2 = vi_results[1]

                # kiểm tra đuôi
                elif en_results[-1] in ["i've",'i', "i'm", 'me', 'mine','we','us', 'ours', "i'll", "we've", "we'll"]:
                    n1 = vi_results[-1]
                
                elif en_results[-1] in ["my", "our"]: # sở hữu, vd: dì của tôi
                    n1 = vi_results[-1]
                
                elif len(en_results) > 1 and en_results[-2] in ["my", "our"]:
                    n1 = vi_results[-1]

                elif en_results[-1] in ["you", "yours", "you've", "you'll"]:
                    n2 = vi_results[-1]

                elif en_results[-1] in ["your"]:  
                    n2 = vi_results[-1]
        
                elif len(en_results) > 1 and en_results[-2] in ["your"]:  
                    n2 = vi_results[-1]

                else: 
                    # bổ sung các trường hợp còn thiếu luật
                    pass

        # check before return
        if n1 != None and n2 != None:
            if [n1,n2] in cap_daitu_nganghang:
                pass
            elif [n1,n2] in cap_daitu_phancap or [n2,n1] in cap_daitu_phancap:
                pass
            else:
                # sai cap dai tu, gắn bằng 1 cặp có sẵn
                for item in cap_daitu_phancap:
                    if n1 == item[0]:
                        n2 = item[1]
                        break
                    if n2 == item[1]:
                        n1 = item[0]
                        break

        return n1, n2
    
    except:
        return None, None

# rs = []
# with open("danhgia_bochuyendoidaitu.csv", "r", encoding="utf16") as f:
#     f.readline()
#     for i in f.readlines():
#         line = i.split("\t")
#         rs += [get_n1n2(line[5])]
        
# with open("rs.csv", "w", encoding="utf16") as f:
#     f.write("Dự đoán\n")
#     for i in rs:
#         f.write(str(i[0])+","+str(i[1])+"\n")

# while 1:
#     print(get_n1n2(input(), True, True))

 
