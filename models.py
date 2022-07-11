import os
import json
import datetime
import sqlite3

from config import func_nums
from treasure import get_one_event
import attribute
import pk
import battle
import skill
import realm

db_name = "烦人修仙bt.db"
db_conn = None
db_cursor = None

gs_list = {}
user_list = {}

def init_db():
    global db_conn, db_cursor
    if not os.path.exists(db_name):
        db_conn = sqlite3.connect(db_name)
        db_cursor = db_conn.cursor()

        db_cursor.execute("create table gs (id int, name varchar(20), info varchar(2000));")
        db_cursor.execute("create table user (id int, gs_id int, name varchar(20), nickname varchar(100), info varchar(2000));")

        db_conn.commit()
        print("init db done")
    else:
        db_conn = sqlite3.connect(db_name)
        db_cursor = db_conn.cursor()

        db_cursor.execute("select id, name, info from gs;")
        for row in db_cursor.fetchall():
            gs = game_server(row)
            gs_list[gs.name] = gs

        db_cursor.execute("select id, gs_id, name, nickname, info from user;")
        for row in db_cursor.fetchall():
            u = user(row)
            if u.gs_id not in user_list:
                user_list[u.gs_id] = {}
            user_list[u.gs_id][u.name] = u

        print("load db done")

def get_other(gs_id, message):
    other = message.strip().split(' ')[-1].split('@')[-1]
    if other in user_list[gs_id]:
        return user_list[gs_id][other]
    else:
        return None

class game_server():
    id = 0
    name = ""
    info = {}
    rank_gongli = []
    rank_jingli = []
    rank_juedou = []
    rank_jingjie = []

    def __init__(self, db_row):
        self.id = db_row[0]
        self.name = db_row[1]
        self.info = json.loads(db_row[2])

    def save_db(self):
        global db_conn, db_cursor
        db_cursor.execute("update gs set info='%s' where id=%d;" % (json.dumps(self.info), self.id))
        db_conn.commit()

    def get_rank_gongli(self):
        self.rank_gongli.clear()
        for user_name, u in user_list.get(self.id, {}).items():
            gongli = u.info.get('gongli', 0)
            if gongli == 0:
                continue
            self.rank_gongli.append({ 'name': u.nick_name or user_name, 'gongli': gongli })

        self.rank_gongli.sort(key=lambda x: x['gongli'], reverse=True)
        msg = []
        msg.append('《烦人修仙bt服》功力榜')
        rank = 1
        for item in self.rank_gongli:
            msg.append('【%d】%s 功力:%d' % (rank, item['name'], item['gongli']))
            rank += 1
            if rank > 10:
                break

        return '\n'.join(msg)

    def get_rank_jingli(self):
        self.rank_jingli.clear()
        for user_name, u in user_list.get(self.id, {}).items():
            jingli = u.info.get('jingli', 0)
            if jingli == 0:
                continue
            self.rank_jingli.append({ 'name': u.nick_name or user_name, 'jingli': jingli })

        self.rank_jingli.sort(key=lambda x: x['jingli'], reverse=True)
        msg = []
        msg.append('《烦人修仙bt服》精力榜')
        rank = 1
        for item in self.rank_jingli:
            msg.append('【%d】%s 精力:%d' % (rank, item['name'], item['jingli']))
            rank += 1
            if rank > 10:
                break

        return '\n'.join(msg)

    def reset_all_attr(self):
        pass

    def get_user(self, name):
        return user_list[self.id].get(name)

class user():
    id = 0
    gs_id = 0
    name = ""
    nick_name = ""
    info = {}
    realm_info = {'level': 0, 'name': ''}

    def __init__(self, db_row):
        self.id = db_row[0]
        self.gs_id = db_row[1]
        self.name = db_row[2]
        self.nick_name = db_row[3]
        self.info = json.loads(db_row[4])
        self.realm_info = realm.get_realm(self)

    def set_nick(self, friend):
        self.nick_name = friend.name if hasattr(friend, 'name') else friend.nickname

    def save_db(self):
        global db_conn, db_cursor
        db_cursor.execute("update user set nickname='%s', info='%s' where gs_id=%d and name='%s';" % (self.nick_name, json.dumps(self.info), self.gs_id, self.name))
        db_conn.commit()

    def get_gs(self):
        for gs in gs_list.values():
            if gs.id == self.gs_id:
                return gs

    def qiandao(self, friend):
        self.set_nick(friend)
        last_sign = self.info.get('last_sign')
        today = datetime.datetime.now() + datetime.timedelta(hours=8)
        now = int(today.timestamp() / 86400)
        if not last_sign or last_sign < now:
            self.info['last_sign'] = now
            self.info['last_sign_date'] = today.strftime('%Y-%m-%d')
            num = func_nums['sign_jingli']
            self.info['jingli'] = self.info.get('jingli', 0) + num
            self.info['today_dazuo'] = 0
            self.save_db()
            msg = '【%s】求签成功，精力+%d(%d)' % (self.nick_name, num, self.info['jingli'])
        else:
            msg = '【%s】今天已经求签过了' % (self.nick_name)
        return msg

    def dazuo(self, friend):
        self.set_nick(friend)
        today_dazuo = self.info.get('today_dazuo', 0)
        if today_dazuo and today_dazuo >= func_nums['dazuo_daymax']:
            return '【%s】今天晨练次数已经很多了，修仙为逆天行事，不可操之过急，明日求签之后再继续吧' % (self.nick_name)

        self.info['today_dazuo'] = self.info.get('today_dazuo', 0) + func_nums['dazuo_jingli']
        self.info['jingli'] = self.info.get('jingli', 0) + func_nums['dazuo_jingli']
        self.info['gongli'] = self.info.get('gongli', 0) + func_nums['dazuo_gongli']
        self.save_db()
        msg = '【%s】晨练完成，精力+%d(%d)\n晨练后修行有感, 功力+%d(%d)' % (self.nick_name, func_nums['dazuo_jingli'], self.info['jingli'], func_nums['dazuo_gongli'], self.info['gongli'])

        return msg

    def xunbao(self, friend):
        self.set_nick(friend)
        jingli = self.info.get('jingli', 0)
        if jingli == 0:
            return '【%s】精力不足以进行奇遇事件，请求签或者晨练获得精力' % (self.nick_name)

        msg = []
        msg.append('【%s】开始了奇遇' % (self.nick_name))
        count = 0
        old_gongli = self.info.get('gongli', 0)
        while True:
            one_msg = self.xunbao_one()
            count += 1
            # msg.append(one_msg)
            if one_msg == '精力不足了，停止奇遇':
                self.save_db()
                count -= 1
                new_gongli = self.info.get('gongli', 0)
                delta = new_gongli - old_gongli
                msg.append('奇遇%d次，功力%s%d(%d)' % (count, '-' if delta < 0 else '+', delta, new_gongli))
                break
        return '\n'.join(msg)

    def xunbao_one(self):
        event = get_one_event()
        if self.info.get('gongli', 0) + event['gongli'] < 0:
            return '奇遇事件导致重伤，回档了'

        jingli = self.info.get('jingli', 0) + event['jingli']
        if jingli < 0:
            return '精力不足了，停止奇遇'
        self.info['jingli'] = jingli
        self.info['gongli'] = self.info.get('gongli', 0) + event['gongli']
        # self.save_db()
        return event['desc'] % (self.info['gongli'], event['jingli'], self.info['jingli'])

    def get_info(self, friend):
        self.set_nick(friend)

        msg = []
        msg.append('【%s】' % self.nick_name)
        msg.append('功力: %d' % (self.info.get('gongli', 0)))
        msg.append('境界: %s' % (self.realm_info['name']))
        msg.append('精力: %d' % (self.info.get('jingli', 0)))
        msg.append('晨练进度: %d/%d' % (self.info.get('today_dazuo', 0), func_nums['dazuo_daymax']))

        return '\n'.join(msg)

    def attr_funcs(self, friend, message):
        self.set_nick(friend)
        return attribute.attr_funcs(self, message, get_other(self.gs_id, message))

    def pk(self, friend, message):
        self.set_nick(friend)
        other = get_other(self.gs_id, message)
        if other is None:
            return '战斗对象还未修仙，请不要欺凌弱小！'
        msg, is_win = pk.fight(self, other)
        return msg

    def battle(self, friend, message):
        self.set_nick(friend)
        return battle.funcs(self, message)

    def skill(self, friend, message):
        self.set_nick(friend)
        return skill.funcs(self, message)

    def realm(self, friend, message):
        self.set_nick(friend)
        return realm.funcs(self, message)

    def on_attack(self, timing):
        return skill.skill_trigger(self, timing)

def get_gs(group):
    group_name = str(group.id if group else 1)
    if group_name in gs_list:
        return gs_list[group_name]

    global db_conn, db_cursor
    db_cursor.execute("select id, name, info from gs where name='%s'" % (group_name))
    db_row = db_cursor.fetchone()
    if not db_row:
        db_cursor.execute("select max(id) from gs;")
        max_id = db_cursor.fetchone()
        gs_id = max_id[0] + 1 if max_id[0] else 1
        db_cursor.execute("insert into gs(id, name, info) values(%d, '%s', '{}');" % (gs_id, group_name))
        db_conn.commit()

        db_cursor.execute("select id, name, info from gs where name='%s'" % (group_name))
        db_row = db_cursor.fetchone()
    gs = game_server(db_row)
    gs_list[gs.name] = gs
    return gs

def get_user(group, friend):
    gs = get_gs(group)
    user_name = str(friend.id)
    u = user_list.get(gs.id, {}).get(user_name)
    if u:
        return u

    global db_conn, db_cursor
    db_cursor.execute("select id, gs_id, name, nickname, info from user where gs_id=%d and name='%s'" % (gs.id, user_name))
    db_row = db_cursor.fetchone()
    if not db_row:
        db_cursor.execute("select max(id) from user;")
        max_id = db_cursor.fetchone()
        user_id = max_id[0] + 1 if max_id[0] else 1
        nick_name = friend.name if hasattr(friend, 'name') else friend.nickname
        db_cursor.execute("insert into user(id, gs_id, name, nickname, info) values(%d, %d, '%s', '%s', '{}');" % (user_id, gs.id, user_name, nick_name))
        db_conn.commit()

        db_cursor.execute("select id, gs_id, name, nickname, info from user where gs_id=%d and name='%s'" % (gs.id, user_name))
        db_row = db_cursor.fetchone()
    u = user(db_row)
    if gs.id not in user_list:
        user_list[gs.id] = {}
    user_list[gs.id][user_name] = u

    return u

init_db()