from models import get_gs, get_user
from config import master_id

def gm_ctl(group, member, message):
    u = get_user(group, member)
    if u.name != str(master_id):
        return '还不是gm，建议py'

    ctls = message.split(' ')
    if ctls[1] == '精力':
        jingli_add = int(ctls[2])
        u.info['jingli'] = u.info.get('jingli', 0) + jingli_add
        return 'gm【%s】开启了耍赖模式，精力增加%d(%d)' % (u.nick_name, jingli_add, u.info['jingli'])
    elif ctls[1] == '重置全服加点':
    	gs = get_gs(group)
    	gs.reset_all_attr()
    else:
        return '这是什么？'