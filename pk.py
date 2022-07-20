import random
from util import att_map

def fight(me, other):
    msg = []
    msg.append('【%s】【%s]与【%s】【%s】之间的战斗开始了' % (me.realm_info['name'], me.nick_name, other.realm_info['name'], other.nick_name))
    me_info, other_info = {'name': me.nick_name, 'player': me}, {'name': other.nick_name, 'player': other}
    for k in att_map:
        me_info[k] = me.info.get(k, 0)
        other_info[k] = other.info.get(k, 0)

    if me_info['hp'] <= 0 or other_info['hp'] <= 0:
        return '未正确设置加点, 无法开始战斗', False, other_info['hp']

    is_me_round = True
    is_on_attack = True
    while me_info['hp'] > 0 and other_info['hp'] > 0:
        fighter = me_info if is_me_round else other_info
        defender = other_info if is_me_round else me_info

        if is_on_attack:
            is_on_attack = False
            info = defender['player'].on_attack('on_attack')
            if info['trigger']:
                msg.append(info['msg'])
                is_me_round = not is_me_round
                continue

        is_hit = random.randint(0, 99) < (100 + fighter['hit'] - defender['dodge'])
        if not is_hit:
            msg.append('【%s】发动了攻击, 却被【%s】闪避了' % (fighter['name'], defender['name']))
        else:
            is_cri = random.randint(0, 99) < (fighter['critical'] - defender['tough'])
            blood = max(0, fighter['attack'] * (2 if is_cri else 1) - defender['defend'])
            if blood == 0:
                msg.append('【%s】发动%s, 但是未能破防, 【%s】还剩%d的生命' % (fighter['name'], '致命一击' if is_cri else '攻击', defender['name'], defender['hp']))
            else:
                defender['hp'] -= blood
                msg.append('【%s】发动%s, 造成了%d的伤害, 【%s】还剩%d的生命' % (fighter['name'], '致命一击' if is_cri else '攻击', blood, defender['name'], defender['hp']))
                if defender['hp'] <= 0:
                    info = defender['player'].on_attack('on_death')
                    if info['trigger']:
                        fighter['hp'] -= info['damage']
                        info['msg'] += ', 【%s】还剩%d的生命' % (fighter['name'], fighter['hp'])
                        msg.append(info['msg'])

        is_me_round = not is_me_round
        if len(msg) >= 1000:
            msg = msg[:9] + ['......', '双方打生打死, 不分胜负, 握手言和了']
            return '\n'.join(msg), False, other_info['hp']

    if len(msg) > 10:
        msg = msg[0:3] + ['战斗过程太长, 省略'] + msg[-4:]

    if me_info['hp'] <= 0 and other_info['hp'] <= 0:
        msg.append('【%s】与【%s】两败俱伤, 不分胜负！' % (me.nick_name, other.nick_name))
        is_win = False
    else:
        is_win = me_info['hp'] > 0
        msg.append('【%s】获得了胜利！' % (me_info['name'] if is_win else other_info['name']))
    return '\n'.join(msg), is_win, other_info['hp']