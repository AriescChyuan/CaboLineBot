import random


def random_talk():
    x =int(random.random()*3000)
    print('x= ',x)
    talk = ''
    if x < 5:
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
    elif x >= 85  and x <90:
        talk = '噓！ 我要睡覺了zZZ'
    elif x >= 90  and x <95:
        talk = '幹麻？'
    elif x >= 95  and x <100:
        talk = '垃圾不能亂丟呦 留著丟討厭的人 ㄒㄒ'
    elif x >= 100  and x <105:
        talk = '有沒有認真運動呀！！'
    elif x >= 105  and x <110:
        talk = '守宮餵了嗎？'
    elif x >= 110  and x <115:
        talk = '銓銓這禮拜要飛飛機嗎？ 我想跟去看！！'
    elif x >= 115  and x <120:
        talk = '哈揪～～～ >3<'
    elif x >= 120  and x <125:
        talk = '晚安囉 zZZ'
    elif x >= 125 and x <130:
        talk = '聽說明天會下雨耶！'
    elif x >= 130 and x <135:
        talk = 'Hi~'
    elif x >= 135 and x <140:
        talk = '什麼時候我也會收到禮物呀！！'

    return talk
