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


def preprocess_pronoun(text, split_sep = " "):
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

N = ['mẹ','con','cha','anh','em','chú','cháu','chị','ông','bà','tớ','tao','tôi','cậu','mày','mình', 'bồ','cô','bạn','ba','bố','bác','dượng','thím']
def get_n1n2(input):
    try:
      
        sentence = translator.translate(input, dest ='en').text
        sentence = sentence.replace('.', ' . ')
        sentence = sentence.replace(',', ' , ')
        sentence = sentence.replace('!', ' ! ')
        sentence = sentence.replace("?", " ? ")
        sentence = sentence.replace('-', ' - ')
        sentence = sentence.replace('  ', ' ')
        sentence = sentence.replace('  ', ' ')
        en_tokens = sentence.lower().split()
        en_results = []


        for i in detect_high_frequent_phrase:
            input = input.replace(i, "_".join(i.split(" ")))
            
        vi_tokens = input.split()
        vi_results = []
        # print(vi_tokens)
        for i, token in enumerate(en_tokens):
            if token.lower() in ['aunt','you','i', "i'm",'mom','me','uncle','my','man','parents','honey','baby','we','mother','children','mine','us',"i've",'our'] and token not in en_results:
                en_results.append(token.lower())
        for i, token in enumerate(vi_tokens):
            if token.lower() in N and token.lower() not in vi_results :
                if i < len(vi_tokens) - 1:
                    if (vi_tokens[i].lower() in N and vi_tokens[i+1].lower() in N) or (vi_tokens[i].lower() in N and vi_tokens[i+1] == 'của'):
                        pass
                    else:
                        if token.lower() not in ['anh','con','mình','cô','bạn','ông','bà', 'ba'] :
                            vi_results.append(token.lower())
                        elif i < len(vi_tokens) - 1:
                            if vi_tokens[i].lower() == 'mình':
                                if vi_tokens[i-1].lower() != 'bực':
                                    vi_results.append(token.lower())
                            elif vi_tokens[i].lower() == 'anh':
                                if vi_tokens[i+1].lower() not in ['bạn','ấy']:
                                    vi_results.append(token.lower())
                            elif vi_tokens[i].lower() == 'con':
                                if vi_tokens[i+1].lower() not in ['gái','trai','chó','mèo','rể','dâu','bạn']:
                                    vi_results.append(token.lower())
                            elif vi_tokens[i].lower() in ['ông','cô','bà']:
                                if vi_tokens[i+1].lower() not in ['ấy', 'đơn','ta']:
                                    vi_results.append(token.lower())
                            elif vi_tokens[i].lower() == 'bạn':
                                if vi_tokens[i+1].lower() not in ['thân', 'bè']:
                                    if i > 0 and vi_tokens[i-1].lower() not in ['đứa','bọn','tụi','nhóm','hội']:
                                        vi_results.append(token.lower())
                                    else:
                                        vi_results.append(token.lower())
                            elif vi_tokens[i].lower() == 'ba':
                                if vi_tokens[i+1].lower() not in ['tháng','năm','ngày','trăm','ngàn','mươi','lần','người']:
                                    vi_results.append(token.lower())
                            else:
                                if vi_tokens[i+1].lower() != 'bạn':
                                    vi_results.append(token.lower())
                        else:
                            vi_results.append(token.lower())
                else:
                    vi_results.append(token.lower())
        # Loại các từ trùng:
        overlap = ['i','mine',"i'm",'my','me','we','us',"i've"]
        for i in overlap:
            for j in overlap:
                if i != j and i in en_results and j in en_results:
                    en_results.remove(j)
        # check 
        # print(vi_results)
        # print(en_results)
        n1 = n2 = None
        if len(vi_results) > len(en_results):
            if en_tokens[0] in ['hi','sorry','congratulations','goodbye','bye','hey','hello','honey','thank']:
                if len(vi_results) > 1:
                    if vi_tokens[0].lower() in ['chào','xin']:
                        if vi_results[0] in ['cậu','mày','bồ','bạn']:
                            if vi_results[1] in ['con','cháu']:
                                return vi_results[0], vi_results[1]
                            return vi_results[1], vi_results[0]
                        return vi_results[0], vi_results[1]
                    else:
                        if vi_results[0] in ['tôi','bạn']:
                            return 'tôi', 'bạn'
                        if vi_results[0] in ['cậu','tớ']:
                            return 'tớ','cậu'
                        return vi_results[1], vi_results[0]
                elif len(vi_results) == 1:
                    if vi_results[0] not in ['mày','cậu','bạn','bồ']:
                        n1 = vi_results[0]
                    else:
                        n2 = vi_results[0]
            else:
                if len(vi_results) == 1:
                    if vi_results[0] not in ['mày','cậu','bạn','bồ']:
                        n1 = vi_results[0]
                    else:
                        n2 = vi_results[0]

                elif len(vi_results) > 1:
                    if vi_results[0] in ['bồ','bạn','cậu','mày']:
                        return vi_results[1], vi_results[0]
                    if len(en_results)>0 and en_results[0] not in ['i', "i'm", 'me','my','we','mine','us','our',"i've"]:
                        return vi_results[0],vi_results[1]
                    else:
                        return vi_results[1], vi_results[0]
                    return vi_results[0], vi_results[1]
        elif len(vi_results) < len(en_results):
            if len(vi_results) > 1:
                if en_results[0] not in ['i', "i'm", 'me','my','we','mine','us','our',"i've"]:
                    if vi_results[0] in ['bồ','bạn','mày','cậu']:
                        return vi_results[1], vi_results[0]
                    return vi_results[0],vi_results[1]
                return vi_results[1], vi_results[0]

            elif len(vi_results) == 1:
                if vi_results[0] not in ['cậu','bạn', 'mày','bồ']:
                    if en_results[0] not in ['i', "i'm", 'me','my','we','mine','us','our',"i've"]:
                        n1 = vi_results[0]
                    else:
                        if vi_results[0] in ['tao','tớ','tôi','mình']:
                            n1 = vi_results[0]
                        else:
                            n2 = vi_results[0]
                else:
                    n2 = vi_results[0]
            else:
                return 'tôi','bạn'
            
        else:
            if len(vi_results) == 0:
                return 'tôi', 'bạn'
            else:
                if len(en_results) > 1:
                    if en_results[0] not in ['i', "i'm", 'me','my','we','mine','us','our',"i've"]:
                        if vi_results[0] in ['bồ','bạn','mày','cậu']:
                            return vi_results[1], vi_results[0]
                        return vi_results[0],vi_results[1]
                    return vi_results[1], vi_results[0]
                else:
                    if vi_results[0] not in ['cậu','bạn', 'mày','bồ']:
                        if en_results[0] not in ['i', "i'm", 'me','my','we','mine','us','our',"i've"]:
                            n1 = vi_results[0]
                        else:
                            if vi_results[0] in ['tao','tớ','tôi','mình']:
                                n1 = vi_results[0]
                            else:
                                n2 = vi_results[0]
                    else:
                        if vi_results[0] in ['tao','tớ','tôi','mình']:
                            n1 = vi_results[0]
                        else:
                            n2 = vi_results[0]
            # TH n1 = None
        if n1 == None:
            if n2 in ['mẹ','cha','chú', 'cô','ba','bố','bác','dượng','thím']:
                n1 = 'con'
            if n2 in ['ông','bà']:
                n1 = 'cháu'
            if n2 in ['bạn','cậu']:
                n1 = 'tôi'
            if n2  == 'cậu':
                n1 = 'tớ'
            if n2 == 'mày':
                n1 = 'tao'
            if n2 in ['chị','anh']:
                n1 = 'em'
            if n2 == 'con':
                n1 = 'mẹ'
            if n2 == 'cháu':
                n1 = 'chú'
            if n2 == 'em':
                n1 = 'anh'
            if n2 in ['bạn','bồ']:
                n1 = 'tôi'

        # TH n2 
        if n2 is None:
            if n1 in ['cha','mẹ','chú','ba','bố','thím','dượng','bác','cô']:
                n2 = 'con'
            if n1 in ['ông','bà']:
                n2 = 'cháu'
            if n1 in ['tớ', 'tôi', 'mình']:
                n2 = 'cậu'
            if n1 == 'tao':
                n2 = 'mày'
            if n1 in ['chị','anh']:
                n2 = 'em'
            if n1 == 'em':
                n2 = 'anh'
            if n1 == 'cháu':
                n2 = 'chú'
            if n1 == 'con':
                n2 = 'mẹ'
            if n1 == 'tôi':
                n2 = 'bạn'
        if n1 == None and n2 == None:
            return 'tôi','bạn'
        return n1,n2
    
    except:
        return None, None

# while 1:
#     print(get_n1n2(input()))