import random

positive = [
    "Bạn đâu rồi , vui quá nên quên tôi rồi chăng ?",
    "Người ơi người đâu rồi ?",
    "Hay chia sẻ niềm vui cùng nhau nào đừng im lặng mà vui một mình như thế chứ ?",
    "Bạn đang tận hưởng niềm vui à ?",
    "Có chuyện gì hay kể tôi nghe nữa , đừng im lặng thế chứ ?",
    "Thật vui nếu như bạn tiếp tục trò chuyện cùng tôi đấy ",
]

negative = [
    "Bạn vẫn còn buồn à ?",
    "Bạn đâu rồi , đừng buồn nữa người ơi ?",
    "Bạn đang khóc sao ?",
    "Bạn đừng lặng im như vậy , hãy trò chuyện với tôi đi , tôi sẵn lòng tâm sự cùng bạn",
    "Có chuyện gì hãy tâm sự cùng tôi , đừng lặng im như vậy",
    "Bạn không xem tôi là bạn hay sao mà im lặng không tâm sự với tôi nữa ?",
]

neutral = [
    "Bạn đang bận à ?",
    "Người ơi , người đâu rồi ?",
    "Bạn gì ơi , bạn bỏ quên tôi rồi nè",
    "Tôi đang đứng đợi bạn từ chiều giờ",
    "Bạn đâu rồi ?",
    "Thật vui nếu như bạn tiếp tục trò chuyện cùng tôi đấy ",
]

first_hello = [
    "Chào bạn , mình họ chát tên bót , hân hạnh gặp bạn!",
    "Mình là chatbot , bạn hãy chia sẻ câu chuyện hôm nay của bạn với mình đi."
]


def first_greet():
    return first_hello[random.randint(0, len(first_hello) - 1)]


user_hello = [
    "chào bạn",
    "xin chào bạn",
    "hello",
    "hi",
    "hi bạn",
    "hello bạn",
    "xin chào",
    "chào",
    "chào buổi sáng",
    "chào buổi trưa",
    "chào buổi chiều",
    "buổi sáng tốt lành",
    "buổi trưa tốt lành",
    "buổi tối tốt lành",
    "chào bót",
    "chào chát bót"
    "chào chatbot"
    "chào bé bót"
    "chào bạn bót"
]

reply_hello = [
    "Tôi có thể giúp gì được bạn không ?",
    "Có chuyện gì vậy ?",
    "Tôi đây , có vấn đề gì với bạn sao ?",
    "Thật hân hạnh khi bạn nhớ đến tôi , bạn có muốn nói gì với tôi à ?",
    "Rất vui khi bạn nhắn cho tôi , có chuyện gì với bạn à ?",
    "Hãy kể câu chuyện của bạn cho tôi nghe đi , tôi hứa sẽ tâm sự với bạn một cách chân thành",
    "Thật tốt khi bạn trò chuyện với tôi , thế hôm nay bạn như thế nào ?",
]

def hello_user():
    return reply_hello[random.randint(0, len(reply_hello) - 1)]

user_say_bye = [
    "bye",
    "good bye",
    "goodbye",
    "tạm biệt",
    "tạm biệt nhé",
    "tạm biệt cậu",
    "bai nhé",
    "chào nha",
    "hẹn gặp lại",
    "bai , hẹn gặp lại",
]


bye_to_user = [
    "Tạm biệt bạn , rất vui khi được trò chuyện với bạn",
    "Cảm ơn bạn đã giành thời gian trò chuyện với tôi",
    "Cảm ơn bạn , hẹn gặp lại bạn trong một ngày không xa",
    "Cảm ơn bạn nhiều , hãy nhớ đến tôi thường xuyên nhé",
    "Cảm ơn bạn vì đã trò chuyện cùng tôi , chúc bạn có một ngày vui vẻ",
    "Thật hạnh phúc khi bạn trò chuyện với tôi như thế này , tạm biệt và hẹn gặp lại bạn",
]


def bye_user():
    return bye_to_user[random.randint(0, len(bye_to_user) - 1)]


# pos, neg, neu
all_emotions_cls = [
    [
        "surprised",
        "impressed",
        "joyful",
        "proud",
        "faithful",
        "excited",
        "grateful",
        "prepared",
        "caring",
        "trusting",
        "hopeful",
        "anticipating",
        "confident",
        "content",
    ],
    [
        "disappointed",
        "jealous",
        "sad",
        "afraid",
        "ashamed",
        "lonely",
        "anxious",
        "devastated",
        "disgusted",
        "guilty",
        "terrified",
        "angry",
        "annoyed",
        "apprehensive",
        "embarrassed",
        "furious",
    ],
    [
        "sentimental",
        "nostalgic",
    ],
]


def keep_conversation(emo):
    if emo in all_emotions_cls[0]:
        return positive[random.randint(0, len(positive) - 1)]

    if emo in all_emotions_cls[1]:
        return negative[random.randint(0, len(negative) - 1)]

    if emo in all_emotions_cls[2]:
        return neutral[random.randint(0, len(neutral) - 1)]



# emo = "sentimental"
# while 1:
    # emo = input()
    # input()
    # print(keep_conversation(emo))
    # print(hello_user())
