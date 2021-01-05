first_person = "t, tôi, tao, tui, tớ, tau, bác, cháu, anh, chị, em, mình, ta, con, ba, mẹ, bố, cha, vợ,\
                tía, u, thầy, bé, bần đạo, chú, cô, thím, dượng, đệ tử, tiểu đệ, ca, muội, ca ca, muội muội"

second_person = "m, bạn, mày, mầy, cậu, mi, ông, bà, chú, cô, dì, dượng, thím, bác, cu, bà xã, vợ,\
                chồng, ông xã, honey, anh, chị, em, tía, u, con, ba, cha, bố, mẹ, u, thầy, bé, \
                tình yêu, sếp, thí chủ, cháu, lão đại, đại ca, sư phụ, sư thúc, nhóc, ca, muội, ca ca, muội muội"

high_frequent_phrase = "bạn bè, bè bạn, bạn hàng, người bạn, bạn gái, bạn trai, bạn xã giao,\
bạn học, bạn đọc, đám bạn, cô bạn, anh bạn, nhỏ bạn, ông bạn,\
bạn trẻ, bạn già, bạn tù, tụi bạn, trở thành bạn, bạn thân, bạn tôi,\
bạn mình, nhóm bạn, kết bạn, tìm bạn, tình bạn,\
nhiều bạn, ít bạn, vài bạn, nhà bạn, bạn ấy, bạn nhóc, bạn đó, bạn nhỏ,\
bạn cùng, bạn chí cốt, bạn của, thằng bạn, đứa bạn,\
bực mình, đầy mình, rùng mình, giữ mình, chuyển mình, trở mình, của mình, giật mình,\
biết mình, bầm mình, hoà mình, dân mình, người mình, dân tộc mình, người việt mình,\
hoàn thiện mình, đời mình, giấu mình, một mình, uốn mình, xuôi mình, buông mình, tự mình,\
mình mẩy, hết mình, nghiêng mình, liều mình"

first_person = first_person.replace(", ", ",").split(",")
second_person = second_person.replace(", ", ",").split(",")
high_frequent_phrase = high_frequent_phrase.replace(", ", ",").split(",")

# Nguoi dung nhap
def convert_sentence(input, n1, n2):
    LIST = ['.',',','?','! ','...','-','~','*']
    for i in LIST:
        input = input.replace("{} ".format(i), " {} ".format(i))

    if len(n2.split())>1:
        index = input.lower().find(n2.lower())
        n2 = n2.replace(" ","_")
        while index >= 0 :
            temp_str = input[index:len(n2)+index]
            input = input.replace(temp_str,n2)
            index = input.lower().find(temp_str.lower())
    if len(n1.split())>1:
        index = input.lower().find(n1.lower())
        n1 = n1.replace(" ","_")
        while index >= 0:
            temp_str = input[index:len(n1)+index]
            input = input.replace(temp_str,n1)
            index = input.lower().find(temp_str.lower())
    sentence = input.split(" ")
    output = []
    for i, token in enumerate(sentence):
        if token == n1.lower() or token == n1.capitalize():
            if i <= len(sentence) - 2:
                if sentence[i+1] not in ['ấy', 'ta', 'nhóc', 'bé','của','nhỏ','đó','ta'] and sentence[i-1] != 'đàn':
                    token = 'tôi'
                if sentence[i-1] == 'của':
                    if (sentence[i-2] == n2.capitalize() or sentence[i-2] == n2.lower()):
                        output[i-2] = 'bạn'
                elif sentence[i-1] == n2.capitalize() or sentence[i-1] == n2.lower():
                    token = 'tôi'
            elif i == len(sentence) - 1:
                token = 'tôi'
        if token == n2.capitalize() or token == n2.lower():
            if i <= len(sentence) - 2:
                if sentence[i+1] not in ['ấy', 'ta', 'nhóc', 'bé','của','nhỏ','đó','ta'] and sentence[i-1] != 'đàn':
                    token = 'bạn'
            elif i == len(sentence) - 1:
                token = 'bạn'
        if token.upper() == n2.split("_")[0].upper():
            if i <= len(sentence) - 2 and sentence[i+1] not in ['ấy', 'ta', 'nhóc', 'bé','của','nhỏ','đó','ta']:
                token = 'bạn'
            if i == len(sentence) - 1:
                token = 'bạn'
        output.append(token)
    return " ".join(output)

# Tra ve cho nguoi dung
def revert_sentence(sentence, n1, n2):
    for i in high_frequent_phrase:
        sentence = sentence.replace(i, "_".join(i.split(" ")))

    sentence = sentence.lower()
    sentence = sentence.replace("bạn có bạn", "bạn có_bạn") # trường hợp hi hữu
    sentence = sentence.split(" ")
    index = []
    for i in range(len(sentence)):
        if ("tôi" == sentence[i]):
            index.append(i)

    for i in index:
        if i > 1 and sentence[i-1] in second_person:
            sentence[i] = "của " + n1
        else:
            sentence[i] = n1

    index = []
    for i in range(len(sentence)):
        if ("bạn" == sentence[i]):
            index.append(i)

    for i in index:
        if i > 1 and sentence[i-1] in second_person:
            sentence[i] = "của " + n2
        else:
            sentence[i] = n2

    return " ".join(sentence).replace("_", " ")

# his = []
# while(1):
    # sentence = input()
    # n1,n2,sentence = sentence.split("\t")
#     print("--> " + revert_sentence(sentence, n1, n2))
    # if(sentence == "q"):
    #     break
    # print("--> " + convert_sentence(sentence, "tớ", "tao"))
    # his.append(revert_sentence(sentence, "tao", "mày"))

# for i in his:
#     print(i)