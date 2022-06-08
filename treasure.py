import random
import json

rates = {
    '-2': 1,
    '-1': 3,
    '0': 38,
    '1': 15,
    '2': 3
}

events = [
    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '今天阳光灿烂，正是睡觉的好日子，被鬼压床，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '今天阳光灿烂，正是睡觉的好日子，睡觉时抽筋，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '今天阳光灿烂，正是睡觉的好日子，一天匆匆而过，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '今天阳光灿烂，正是睡觉的好日子，睡到心满意足，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '今天阳光灿烂，正是睡觉的好日子，睡梦中有所得，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '今天狂风大作，躲在家中，被吹破的窗户划伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '今天狂风大作，躲在家中，心慌意乱，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '今天狂风大作，躲在家中，吃吃喝喝，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '今天狂风大作，躲在家中，勤奋读书，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '今天狂风大作，躲在家中，忽有所得，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '今天倾盆大雨，不信邪出门修炼，被雷劈伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '今天倾盆大雨，不信邪出门修炼，滑倒摔伤，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '今天倾盆大雨，不信邪出门修炼，没有收获，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '今天倾盆大雨，不信邪出门修炼，习得春雨剑法，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '今天倾盆大雨，不信邪出门修炼，遇到仙人传功，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '被人追杀至悬崖，掉落摔伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '被人追杀至悬崖，求饶后被打赏，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '被人追杀至悬崖，侥幸逃脱，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '被人追杀至悬崖，被人相救，指点了功法，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '被人追杀至悬崖，掉落山崖习得绝世武功，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '与人一起去青楼，被护院打赏，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '与人一起去青楼，被采了阳，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '与人一起去青楼，吃喝玩乐大宝剑，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '与人一起去青楼，被头牌青睐，偷偷送了你一本秘籍，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '与人一起去青楼，遇到争风吃醋的两败俱伤，偷的秘籍一本，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '遇到官府贴皇榜，查看时被歹人偷袭受伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '遇到官府贴皇榜，不小心揭榜却没抓到歹人，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '遇到官府贴皇榜，怕事匆匆路过，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '遇到官府贴皇榜，联合道友抓捕坏人，获得秘籍，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '遇到官府贴皇榜，救下莽撞准备解绑的美人，对方心生感激，承诺来生做牛做马，送你一本秘籍，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '参加武林大会，莽撞上台被打伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '参加武林大会，围观被误伤，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '参加武林大会，一轮游，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '参加武林大会，与人切磋后对功法更有心得，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '参加武林大会，被高人指点，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '听说韩老魔要收徒，被嫌弃资质差打伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '听说韩老魔要收徒，争夺资格时被人打伤，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '听说韩老魔要收徒，对自己很有13数，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '听说韩老魔要收徒，自己做了顿好吃的，吃完心满意足，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '听说韩老魔要收徒，赶紧闭关，出关后功力大涨，功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '发现大秘境，想去浑水摸鱼被人打伤，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '发现大秘境，被守门怪物打伤，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '发现大秘境，心知与自己无关，翻身继续睡觉，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '发现大秘境，门口摸了一把就跑，哪知得到天山雪莲所炼制的药丸，吃了之后功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '发现大秘境，售卖消息换得秘籍一本，学习后功力+2(%d)，精力%d(%d)' },

    { 'rate': rates['-2'], 'jingli': -10, 'gongli': -2, 'desc': '意外获得天外玄铁，被人发现后击伤抢走玄铁，功力-2(%d)，精力%d(%d)' },
    { 'rate': rates['-1'], 'jingli': -10, 'gongli': -1, 'desc': '意外获得天外玄铁，自己想炼化却被反噬受伤，功力-1(%d)，精力%d(%d)' },
    { 'rate': rates['0'], 'jingli': -10, 'gongli': 0, 'desc': '意外获得天外玄铁，藏了起来，功力不变(%d)，精力%d(%d)' },
    { 'rate': rates['1'], 'jingli': -10, 'gongli': 1, 'desc': '意外获得天外玄铁，送到铁匠铺打造了一把宝剑，送人后获得秘籍一本，功力+1(%d)，精力%d(%d)' },
    { 'rate': rates['2'], 'jingli': -10, 'gongli': 2, 'desc': '意外获得天外玄铁，不知道怎么使用就送给了高人，被高人指点，功力+2(%d)，精力%d(%d)' },

]

total_rate = 0

def generate_event():
    global total_rate
    for event in events:
        event['begin_rate'] = total_rate
        event['end_rate'] = total_rate + event['rate']
        total_rate += event['rate']

generate_event()

def get_one_event():
    global total_rate
    rnd = random.randint(0, total_rate - 1)
    for event in events:
        if rnd >= event['begin_rate'] and rnd < event['end_rate']:
            return event
