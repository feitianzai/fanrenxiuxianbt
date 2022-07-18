# 灵珠
import random

def item_desc(u):
    msg = []
    msg.append('使用灵珠可以获得境界相关的随机功力, 使用方法: 灵珠 x数量 或者 灵珠 数量. 带x是随机一次乘次数，不带是随机次数')
    msg.append('【%s】灵珠数量: %d' % (u.nick_name, u.info.get('land_item', 0)))
    return '\n'.join(msg)

def get_int(num):
    try:
        return int(num.replace('x', '').replace(',', '').strip())
    except:
        return 0

def item_use(u, message):
    use_num = message.split(' ')[-1]

    use = get_int(use_num)
    if use <= 0:
        return '【%s】请正确输入使用的数量' % (u.nick_name)

    have = u.info.get('land_item', 0)
    if have < use:
        return '【%s】灵珠数量不足, 当前拥有%d' % (u.nick_name, have)

    u.info['land_item'] = have - use
    realm_level = u.realm_info['level']

    total = 0
    if 'x' not in use_num:
        count = use
        while count > 0:
            total += random.randint(1, realm_level)
            count -= 1
    else:
        total = random.randint(1, realm_level) * use

    u.info['gongli'] = u.info.get('gongli', 0) + total
    u.save_db()
    return '【%s】成功使用%d颗灵珠，获得%d(%d)功力' % (u.nick_name, use, total, u.info['gongli'])

def funcs(u, message):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return item_desc(u)

    return item_use(u, message)