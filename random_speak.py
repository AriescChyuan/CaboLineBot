import random
x =int(random.random()*1000)

def random_talk():
    talk = ''
    if x < 10:
        talk = '嘻嘻'
    elif x >= 10 and x < 20:
        talk = '好無聊 Q_Q'
    elif x >=20 and x <30:
        talk = "想便便 >O< " 
    elif x >=30 and x <40:
        talk = '好想看電影～'
    elif x >=40 and x< 50:
        talk = '剛剛夢到 好吃的甜甜圈耶 XD'
    elif x >= 50 and x <60:
        talk = '妮妮喜歡什麼動物呢？'
    elif x >= 60 and x <70:
        talk = '剛剛振銓好像又偷吃餅乾耶...'
    elif x >= 70 and x < 75:
        talk = '聽說曾經有一隻可愛又乖巧的老鼠～ 牠叫 跑跑 @@a'
    elif x >= 75  and x <80:
        talk = '嘻嘻 我不用上班～'
    elif x >= 80  and x <85:
        talk = '冷氣是不是有點冷 >o<'
    return talk
