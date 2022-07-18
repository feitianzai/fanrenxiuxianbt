#秘境
import datetime
import random
import math
from util import att_map
import pk

from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At
from graia.ariadne.model import Friend, Group, MemberPerm

need_realm = 2
land_level = 15
land_mon_begin = 0.5
land_mon_step = 0.1
land_cooldown = 600

lands = {}

class Monster():
    def __init__(self):
        self.realm_info = {}
        self.nick_name = ''
        self.info = {'gongli': 0}
        self.attr = {
            'hp': 5.75,
            'attack': 2,
            'defend': 2,
            'hit': 0.1,
            'dodge': 0.05,
            'critical': 0.05,
            'tough': 0.05,
        }
        self.attr_desc = []

    def create(self, realm_name, level, player_gongli):
        self.realm_info['name'] = realm_name
        self.nick_name = '第%d层守护兽' % (level)

        times = land_mon_begin + land_mon_step * level
        gongli = int(player_gongli * times)
        for attr_name, val in self.attr.items():
            attr_val = int(val * gongli)
            self.info[attr_name] = attr_val
            self.attr_desc.append('%s: %d' % (att_map[attr_name], attr_val))

    def on_attack(self, timing):
        return {'trigger': False}

    def set_hp(self, hp):
        self.info['hp'] = hp

def fairyland_init(user_list):
    global lands
    for gs_id, gs_users in user_list.items():
        for user_name, user in gs_users.items():
            land = user.info.get('land')
            if land:
                lands[(user.get_gs().id, user.id)] = {'user': user, 'land': land}

def __extra_item(level, realm_level):
    if level < random.randint(0, 100):
        return 0
    return random.randint(1, realm_level)

async def fairyland_update(app, timestamp):
    global lands
    lands_to_delete = []
    for land_key, land_info in lands.items():
        land = land_info['land']
        if land['act_time'] + land_cooldown > timestamp:
            continue

        user = land_info['user']
        realm_level = user.realm_info['level']
        land_level_cost = math.pow(10, max(realm_level - 1, 1))
        if user.info.get('lingqi', 0) < land_level_cost:
            land['act_time'] += land_cooldown
            continue

        msg = ''
        old_mon = Monster()
        old_mon.create(land['realm_name'], land['now_level'], land['gongli'])
        old_mon.set_hp(land['mon_hp'])
        land['act_time'] = timestamp
        user.info['lingqi'] = user.info.get('lingqi', 0) - land_level_cost

        _, is_win, other_hp = pk.fight(user, old_mon)
        if is_win or other_hp <= 0:
            pass_str = '【%s】经过奋战, 击败了【%s】, ' % (user.nick_name, old_mon.nick_name)
            extra_item = __extra_item(land['now_level'], realm_level)
            land_item = land['now_level'] + extra_item
            land['item_num'] += land_item
            if extra_item > 0:
                item_str = '获得了%d+%d(%d)颗灵珠, ' % (land['now_level'], extra_item, land['item_num'])
            else:
                item_str = '获得了%d(%d)颗灵珠, ' % (land_item, land['item_num'])

            land['now_level'] += 1
            if land['now_level'] > land_level:
                lands_to_delete.append(land_key)
                user.info['land_item'] = user.info.get('land_item', 0) + land['item_num']
                msg = '%s%s完成了秘境的探索' % (pass_str, item_str)
                land = None
            else:
                mon = Monster()
                mon.create(land['realm_name'], land['now_level'], land['gongli'])
                land['mon_hp'] = mon.info['hp']
                land['mon_max_hp'] = mon.info['hp']
                if is_win:
                    msg = '%s%s来到了第%d层' % (pass_str, item_str, land['now_level'])
                else:
                    land['act_time'] += land_cooldown
                    msg = '%s自身遭受重伤, 额外休息%d分钟, %s来到了第%d层' % (pass_str, int(land_cooldown / 60), item_str, land['now_level'])
                if user.info['lingqi'] < land_level_cost:
                    land['act_time'] += land_cooldown
                    msg = msg + ', 由于灵气不足停止了探索'
        elif other_hp == land['mon_max_hp'] or other_hp == land['mon_hp']:
            msg = '【%s】经过奋战, 完败于【%s】, 刮痧!!' % (user.nick_name, old_mon.nick_name)
        else:
            land['mon_hp'] = other_hp
            msg = '【%s】经过奋战, 惜败于【%s】, 守护兽剩余血量%d(%d), 请继续努力' % (user.nick_name, old_mon.nick_name, land['mon_hp'], land['mon_max_hp'])

        user.info['land'] = land
        user.save_db()

        # print(int(user.name), user.nick_name, msg)
        #send message
        group_id = int(user.get_gs().name)
        if group_id == 1:
            friend = Friend(id=int(user.name), nickname=user.nick_name, remark='')
            await app.sendMessage(friend, MessageChain.create([Plain(msg)]))
        else:
            group = Group(id=group_id, name='', permission=MemberPerm.Member)
            await app.sendMessage(group, MessageChain.create([Plain(msg)]))

    for land_key in lands_to_delete:
        del lands[land_key]

def fairyland_desc(u):
    msg = []
    msg.append('【秘境玩法说明】')
    msg.append('\t玩家在元婴后可以探索15层秘境, 每层可获得与层数相同的灵珠, 每个灵珠可以提供境界相关的随机功力')
    msg.append('\t秘境每天仅可探索一次, 需要打败每一层的守护兽方可获得灵珠, 也可以提前收获, 放弃后续的收益')
    msg.append('\t秘境为自动探索, 每一层的守护兽将逐渐增强')
    msg.append('\t可用口令 秘境 探索, 秘境 状态, 秘境 收获')
    land = u.info.get('land')
    if land:
        ts = int(datetime.datetime.now().timestamp())
        next_cooldown = land['act_time'] + land_cooldown - ts
        msg.append('【%s】当前秘境: 层数%d(%d), 守护兽血量%d(%d), 已累计灵珠%d, 下次将在%d分钟后挑战' % (u.nick_name, land['now_level'], land['max_level'], land['mon_hp'], land['mon_max_hp'], land['item_num'], int(next_cooldown / 60)))
    msg.append('灵珠数量: %d' % (u.info.get('land_item', 0)))
    return '\n'.join(msg)

def fairyland_move(u):
    realm_level = u.realm_info['level']
    if realm_level < need_realm:
        return '秘境过于危险, 请【%s】努力修炼, 早日破境后再来' % (u.nick_name)

    if u.info.get('land_create') == 1:
        if u.info.get('land'):
            return '【%s】今天的秘境之旅已经开始' % (u.nick_name)
        else:
            return '【%s】今天的秘境之旅已经完成' % (u.nick_name)

    land_level_cost = math.pow(10, max(realm_level - 1, 1))
    if u.info.get('lingqi', 0) < land_level_cost:
        return '【%s】灵气不足，无法开始秘境' % (u.nick_name)

    global lands
    u.info['land_create'] = 1
    now_level = 1
    mon = Monster()
    mon.create(u.realm_info['name'], now_level, u.info.get('gongli', 0))
    land = {
        'realm_name': u.realm_info['name'],
        'gongli': u.info.get('gongli', 0),
        'now_level': now_level,
        'max_level': land_level,
        'mon_hp': mon.info['hp'],
        'mon_max_hp': mon.info['hp'],
        'item_num': 0,
        'act_time': int(datetime.datetime.now().timestamp()) - land_cooldown + 1,
    }
    u.info['land'] = land
    u.save_db()
    lands[(u.gs_id, u.id)] = {'user': u, 'land': land}
    return '【%s】的秘境已经创建，将自动探索' % (u.nick_name)

def fairyland_info(u):
    land = u.info.get('land')
    if not land:
        return '【%s】没有正在探索的秘境' % (u.nick_name)

    ts = int(datetime.datetime.now().timestamp())
    next_cooldown = land['act_time'] + land_cooldown - ts

    return '【%s】当前秘境: 层数%d(%d), 守护兽血量%d(%d), 已累计灵珠%d, 下次将在%d分钟后挑战' % (u.nick_name, land['now_level'], land['max_level'], land['mon_hp'], land['mon_max_hp'], land['item_num'], int(next_cooldown / 60))

def fairyland_exit(u):
    land = u.info.get('land')
    if not land:
        return '【%s】没有正在探索的秘境' % (u.nick_name)

    global lands
    land_key = (u.gs_id, u.id)
    if land_key in lands:
        del lands[land_key]

    u.info['land'] = None
    u.info['land_item'] = u.info.get('land_item', 0) + land['item_num']
    u.save_db()
    return '【%s】结束了秘境探索, 到达了第%d层, 获得了%d(%d)灵珠' % (u.nick_name, land['now_level'], land['item_num'], u.info['land_item'])

def funcs(u, message):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return fairyland_desc(u)

    if attrs[1] == '探索':
        return fairyland_move(u)
    elif attrs[1] == '状态':
        return fairyland_info(u)
    elif attrs[1] == '收获':
        return fairyland_exit(u)