#龙门
import random
import datetime

need_realm = 1
cooldown = 600
cave_config = {
    2: { 'create': 100, 'use': 5, 'gongli': 10 },
    3: { 'create': 1000, 'use': 50, 'gongli': 100 },
    4: { 'create': 10000, 'use': 500, 'gongli': 1000 },
    5: { 'create': 100000, 'use': 5000, 'gongli': 10000 },
    6: { 'create': 1000000, 'use': 50000, 'gongli': 100000 },
    7: { 'create': 10000000, 'use': 500000, 'gongli': 1000000 },
    8: { 'create': 100000000, 'use': 5000000, 'gongli': 10000000 },
}

def cave_desc(u):
    msg = []
    msg.append('【龙门】玩法介绍')
    msg.append('\t金丹以后可以开辟充满灵气的龙门, 消耗自身灵气吸收龙门中的灵气')
    msg.append('\t灵气在后期有额外用途, 且积攒到一定量的灵气可以自动转换为功力')
    msg.append('\t龙门内的灵气全部吸收后可提高渡劫成功率')
    msg.append('\t可用命令:  龙门 新建, 龙门 修炼')
    cave = u.info.get('cave')
    if cave:
        msg.append('当前龙门: 剩余灵气%d(%d)' % (cave.get('left'), cave.get('max')))
    return '\n'.join(msg)

def cave_create(u):
    realm_level = u.realm_info['level']
    if realm_level < need_realm:
        return '龙门过于危险, 请【%s】努力修炼, 早日破境后再来' % (u.nick_name)

    if u.info.get('cave_create') == 1:
        return '【%s】今天的龙门之旅已经结束, 请明日签到后再来' % (u.nick_name)

    cave_info = cave_config[realm_level]
    lingqi = u.info.get('lingqi', 0) + cave_info['create']
    ran_min = u.info.get('gongli', 0) * 10
    ran_max = int(ran_min * 1.5)
    cave_max = random.randint(ran_min, ran_max)
    cave = {'max': cave_max, 'left': cave_max, 'last': 0}
    u.info['cave_create'] = 1
    u.info['cave'] = cave
    u.info['lingqi'] = lingqi
    u.save_db()

    return '【%s】披荆斩棘, 开辟了充满灵气的龙门%d(%d), 获得了%d(%d)的灵气' % (u.nick_name, cave['left'], cave['max'], cave_info['create'], lingqi)

def cave_xiuxian(u):
    realm_level = u.realm_info['level']
    if realm_level < need_realm:
        return '龙门过于危险, 请【%s】努力修炼, 早日破境后再来' % (u.nick_name)

    cave_info = cave_config[realm_level]
    cave = u.info.get('cave')
    if not cave:
        return '【%s】还没有开辟龙门' % (u.nick_name)

    if cave['left'] == 0:
        return '【%s】龙门内的灵气已经被全部吸收, 请开辟新的龙门' % (u.nick_name)

    lingqi = u.info.get('lingqi', 0)
    use_lingqi = cave_info['use']
    if lingqi < use_lingqi:
        return '【%s】灵气不足以在龙门中修炼' % (u.nick_name)

    now = int(datetime.datetime.now().timestamp())
    delta = cave['last'] + cooldown - now
    if delta > 0:
        return '【%s】还在平复之前修炼获得的灵气, 请在%d分钟后再次修炼' % (u.nick_name, int(delta / 60))

    gongli = u.info.get('gongli', 0)
    ran_min = int(gongli * 3)
    ran_max = int(gongli * 4)
    ran = random.randint(ran_min, ran_max)
    ran = min(ran, cave['left'])

    cave['last'] = now
    cave['left'] -= ran
    lingqi = lingqi - use_lingqi + ran
    if lingqi >= cave_info['gongli']:
        lingqi -= cave_info['gongli']
        gongli += 1
        msg = '【%s】在龙门内潜心修炼, 消耗%d自身灵气吸收了%d龙门灵气, 功力+1(%d)' % (u.nick_name, use_lingqi, ran, gongli)
    else:
        msg = '【%s】在龙门内潜心修炼, 消耗%d自身灵气吸收了%d龙门灵气' % (u.nick_name, use_lingqi, ran)

    if cave['left'] == 0:
        u.info['realm_rate'] = u.info.get('realm_rate', 0) + 0.01
        msg = msg + '\n龙门内的灵气被席卷而空, 破境成功率增加了!'

    u.info['lingqi'] = lingqi
    u.info['gongli'] = gongli
    u.info['cave'] = cave
    u.save_db()
    return msg

def funcs(u, message):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return cave_desc(u)

    if attrs[1] == '新建':
        return cave_create(u)
    elif attrs[1] == '修炼':
        return cave_xiuxian(u)