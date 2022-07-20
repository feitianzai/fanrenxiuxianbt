#境界
import random
realms = [
    {'name': '练气', 'max': 10, 'rate': 0.95, 'max_rate': 1, 'fail_lose': 1},
    {'name': '先天', 'max': 100, 'rate': 0.85, 'max_rate': 1, 'fail_lose': 5},
    {'name': '金丹', 'max': 1000, 'rate': 0.75, 'max_rate': 0.8, 'fail_lose': 10},
    {'name': '元婴', 'max': 10000, 'rate': 0.65, 'max_rate': 0.8, 'fail_lose': 50},
    {'name': '化身', 'max': 100000, 'rate': 0.55, 'max_rate': 0.6, 'fail_lose': 100},
    {'name': '返虚', 'max': 1000000, 'rate': 0.45, 'max_rate': 0.6, 'fail_lose': 500},
    {'name': '合道', 'max': 10000000, 'rate': 0.35, 'max_rate': 0.4, 'fail_lose': 1000},
    {'name': '渡劫', 'max': 100000000, 'rate': 0.25, 'max_rate': 0.4, 'fail_lose': 5000},
    {'name': '地仙', 'max': 1000000000, 'rate': 0.05, 'max_rate': 0.1, 'fail_lose': 10000},
]

def realm_desc(u):
    msg = []
    msg.append('【境界系统说明】')
    msg.append('\t部分玩法有境界等级的需求')
    msg.append('\t境界 破境, 可以突破当前境界, 破境有一定几率失败, 失败会扣除部分功力。')
    msg.append('【%s】当前境界为【%s】' % (u.nick_name, get_realm(u)['name']))
    return '\n'.join(msg)

def get_realm(u):
    realm_level = u.info.get('realm', 0)
    realm_info = realms[realm_level]
    return {'level': realm_level, 'name': realm_info['name'], 'max': realm_info['max']}

def upgrade_realm(u):
    realm_level = u.info.get('realm', 0)
    realm_info = realms[realm_level]
    gongli = u.info.get('gongli', 0)
    if gongli < realm_info['max']:
        return '【%s】还未达到破境所需的功力, 请继续修炼吧。' % (u.nick_name)
    realm_addition_rate = u.info.get('realm_rate', 0)
    realm_rate = realm_info['rate'] + realm_addition_rate / 100
    if random.random() < realm_rate:
        u.info['realm'] = realm_level + 1
        u.save_db()
        next_realm = realms[realm_level + 1]
        return '【%s】成功破境至【%s】！' % (u.nick_name, next_realm['name'])
    else:
        lost = realm_info['fail_lose']
        gongli -= lost
        gongli = max(gongli, 0)
        u.info['gongli'] = gongli
        u.save_db()
        return '【%s】破境时遭遇心魔, 破境失败, 功力大减%d(%d)' % (u.nick_name, lost, gongli)

def funcs(u, message):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return realm_desc(u)

    if attrs[1] == '破境':
        return upgrade_realm(u)

