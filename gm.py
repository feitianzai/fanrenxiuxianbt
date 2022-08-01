from models import get_gs, get_user
from config import master_id

def gm_ctl(group, member, message):
    u = get_user(group, member)
    if u.name not in master_id:
        return '还不是gm, 建议py'
    gs = get_gs(group)

    ctls = message.split(' ')
    if ctls[1] == '精力':
        jingli_add = int(ctls[2])
        u.info['jingli'] = u.info.get('jingli', 0) + jingli_add
        return 'gm【%s】开启了耍赖模式, 精力增加%d(%d)' % (u.nick_name, jingli_add, u.info['jingli'])
    elif ctls[1] == '补发灵珠':
        user_id = ctls[2].split('@')[-1]
        num = int(ctls[3])
        user = gs.get_user(user_id)
        if user:
            user.info['land_item'] = user.info.get('land_item', 0) + num
            user.save_db()
        return 'gm【%s】为【%s】补发了%d颗灵珠' % (u.nick_name, user.nick_name, num)
    elif ctls[1] == '重置秘境':
        user_id = ctls[2].split('@')[-1]
        user = gs.get_user(user_id)
        if user:
            user.info['land_create'] = 0
            user.save_db()
        return 'gm【%s】为【%s】重置了秘境' % (u.nick_name, user.nick_name)
    elif ctls[1] == '重置全服加点':
        gs = get_gs(group)
        gs.reset_all_attr()
    elif ctls[1] == '功能关闭':
        gs = get_gs(group)
        gs.set_model_switch(ctls[2], False)
        return 'gm【%s】已关闭【%s】功能' % (u.nick_name, ctls[2])
    elif ctls[1] == '功能打开':
        gs = get_gs(group)
        gs.set_model_switch(ctls[2], True)
        return 'gm【%s】已打开【%s】功能' % (u.nick_name, ctls[2])
    else:
        return ' '.join(ctls[1:])