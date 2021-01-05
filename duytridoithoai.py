import random

excited = [
    "Bạn đâu rồi , vui quá nên quên tôi rồi chăng ?",
    "Người ơi người đâu rồi ?",
    "Hay chia sẻ niềm vui cùng nhau nào đừng im lặng mà vui một mình như thế chứ ?",
    "Bạn đang tận hưởng niềm vui à ?",
    "Có chuyện gì hay kể tôi nghe nữa đi , đừng im lặng thế chứ ?",
    "Thật vui nếu như bạn tiếp tục trò chuyện cùng tôi đấy ",
]


scared = [
    "đừng quá lo lắng , bạn hãy suy nghĩ tích cực lên",
    "lo lắng không giúp được gì đâu , sao bạn không thử kể cho tôi về những câu chuyện vui mà cậu có",
]


angry = [
    "đừng giận nữa mà , bạn đang tự tổn hại sức khoẻ đó .",
    "đăm đắm về cơn giận không phải là ý hay đâu , bạn thử xem bộ phim hoạt hình Larva xem !",
    "Cơn giận khiến chúng ta mất đi sự minh mẫn thường có , hãy chia sẻ với tôi nếu bạn còn phiền não !",
]

sad = [
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
    "Tôi sẽ rất vui nếu bạn tiếp tục trò chuyện cùng tôi đấy ",
]

first_hello = [
    "Chào bạn , mình họ chát tên bót , hân hạnh gặp bạn!",
    "Mình là chatbot , bạn hãy chia sẻ câu chuyện hôm nay của bạn với mình đi."
]


def first_greet():
    return first_hello[random.randint(0, len(first_hello) - 1)]


user_hello = [
    "chào bạn",
    "tôi xin chào bạn"
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
    "chào chát bót",
    "chào chatbot",
    "chào bé bót",
    "chào bạn bót",
    "tôi chào bạn"
]

reply_hello = [
    "Tôi có thể giúp gì được bạn không ?",
    "Tôi đây , bạn có vấn đề gì cần trao đổi không ?",
    "Thật hân hạnh khi bạn nhớ đến tôi , bạn có muốn nói gì với tôi à ?",
    "Rất vui khi bạn nhắn cho tôi , có tin gì mới không ?",
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
    "Cảm ơn bạn đã nói chuyện cùng tôi , hẹn gặp lại bạn trong một ngày không xa",
    "Cảm ơn bạn nhiều đã dành thời gian của mình , hãy nhớ đến tôi thường xuyên nhé",
    "Cảm ơn bạn vì đã trò chuyện cùng tôi , chúc bạn có một ngày vui vẻ",
    "Thật hạnh phúc khi bạn trò chuyện với tôi như thế này , tạm biệt và hẹn gặp lại bạn",
]


def bye_user():
    return bye_to_user[random.randint(0, len(bye_to_user) - 1)]


# excited, scared, angry, sad, neutral
all_emotions_cls = [
    [
        "confident",
        "impressed",
        "joyful",
        "faithful",
        "excited",
        "grateful",
        "prepared",
        "hopeful",
        "proud",
        "content",
        "surprised",
        "caring",
        "trusting",
        "anticipating",
    ],
    [
        "afraid",
        "ashamed",
        "anxious",
        "guilty",
        "apprehensive",
        "embarrassed",
    ],
    [
        "jealous",
        "disgusted",
        "angry",
        "annoyed",
        "furious",
    ],
    [
        "disappointed",
        "sad",
        "lonely",
        "devastated",
        "terrified",
    ],
    [
        "sentimental",
        "nostalgic"
    ]
]


# excited, scared, angry, sad, neutral
def keep_conversation(emo):
    if emo in all_emotions_cls[0]:
        return excited[random.randint(0, len(excited) - 1)]

    if emo in all_emotions_cls[1]:
        return scared[random.randint(0, len(scared) - 1)]

    if emo in all_emotions_cls[2]:
        return angry[random.randint(0, len(angry) - 1)]
    if emo in all_emotions_cls[3]:
        return sad[random.randint(0, len(sad) - 1)]
    if emo in all_emotions_cls[4]:
        return neutral[random.randint(0, len(neutral) - 1)]


# emo = "sentimental"
# while 1:
    # emo = input()
    # input()
    # print(keep_conversation(emo))
    # print(hello_user())
