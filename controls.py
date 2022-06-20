from models import get_gs, get_user
from gm import gm_ctl

control_list = {}

def ctl_list_functions(group, member, message):
    information = []
    for func_name, func_info in control_list.items():
        if func_name == '菜单':
            pass
        elif func_info['desc']:
            information.append('【%s】%s\n' % (func_name, func_info['desc']))
        else:
            information.append('【%s】' % (func_name))
    information.append('更多功能敬请期待\n《烦人修仙bt服》抄袭，我们是认真的！')
    msg = ''.join(information)
    return msg

def ctl_dazuo(group, member, message):
    u = get_user(group, member)
    msg = u.dazuo(member)
    return msg

def ctl_xunbao(group, member, message):
    u = get_user(group, member)
    msg = u.xunbao(member)
    return msg

def ctl_qiandao(group, member, message):
    u = get_user(group, member)
    msg = u.qiandao(member)
    return msg

def ctl_info(group, member, message):
    u = get_user(group, member)
    msg = u.get_info(member)
    return msg

def ctl_attr(group, member, message):
    u = get_user(group, member)
    msg = u.attr_funcs(member, message)
    return msg

def ctl_pk(group, member, message):
    u = get_user(group, member)
    msg = u.pk(member, message)
    return msg

def ctl_battle(group, member, message):
    u = get_user(group, member)
    msg = u.battle(member, message)
    return msg

def ctl_skill(group, member, message):
    u = get_user(group, member)
    msg = u.skill(member, message)
    return msg

def ctl_rank_gongli(group, member, message):
    gs = get_gs(group)
    msg = gs.get_rank_gongli()
    return msg

def ctl_rank_jingli(group, member, message):
    gs = get_gs(group)
    msg = gs.get_rank_jingli()
    return msg

def ctl_rank_juedou(group, member, message):
    return '开发中'

def ctl_rank_jingjie(group, member, message):
    return '开发中'

def ctl_main_info(group, member, message):
    return '开发中'

control_list['菜单'] = { 'desc': '', 'func': ctl_list_functions, }
control_list['晨练'] = { 'desc': '每日一次晨练，可以增加精力', 'func': ctl_dazuo, }
control_list['奇遇'] = { 'desc': '奇遇事件，消耗精力概率增加或者减少功力', 'func': ctl_xunbao, }
control_list['求签'] = { 'desc': '每天一次，增加精力并重置打坐进度', 'func': ctl_qiandao, }
control_list['自视'] = { 'desc': '查看自己的信息', 'func': ctl_info, }
control_list['加点'] = { 'desc': '设置自己的属性点，更多操作输入加点查看', 'func': ctl_attr, }
control_list['战斗'] = { 'desc': '@上想要战斗的人，来进行一场男♂人♂间的战斗吧！', 'func': ctl_pk, }
control_list['竞技'] = { 'desc': '谁是天下第一', 'func': ctl_battle, }
control_list['技能'] = { 'desc': '技能系统', 'func': ctl_skill, }
control_list['功榜'] = { 'desc': '', 'func': ctl_rank_gongli, }
control_list['精榜'] = { 'desc': '', 'func': ctl_rank_jingli, }
# control_list['决斗榜'] = { 'desc': '', 'func': ctl_rank_juedou, }
# control_list['境界榜'] = { 'desc': '', 'func': ctl_rank_jingjie, }

def call_ctl(group, member, message):
    msg = str(message)
    if msg in control_list:
        func = control_list[msg]['func']
        return func(group, member, msg)

    elif msg.startswith('gm'):
        return gm_ctl(group, member, msg)

    else:
        ctl_name = msg.split(' ')[0]
        if ctl_name in control_list:
            func = control_list[ctl_name]['func']
            return func(group, member, msg)

    # message = 'From [%s]:[%s], 来自QQ机器人' % (member.name if hasattr(member, 'name') else member.nickname, message)
    # return message