from util import att_trans, att_map

def attr_desc():
    msg = []
    msg.append('【加点系统说明】')
    msg.append('生命: 生命值, pk时降为0则失败')
    msg.append('攻击: 减去防御为扣血值')
    msg.append('防御: 减少伤害')
    msg.append('命中: 总要打中才能扣血')
    msg.append('闪避: 概率miss, 命中概率为 (100+命中-闪避)%')
    msg.append('暴击: 使得当次攻击翻倍')
    msg.append('韧性: 抵消对面的暴击, 暴击概率为(暴击-韧性)%')
    msg.append('扣血计算公式为 命中?(max(0, 攻击*(暴击?2:1) - 防御)):0')
    msg.append('设置方式为 加点 设置 xx=x xx=x 或者 加点 增加 xx=x xx=x')
    msg.append('查看自己加点为 加点 查看')
    return '\n'.join(msg)

def attr_set(u, sets):
    add_val = 0
    for att, key in att_trans.items():
        if att in sets:
            u.info[key] = sets[att]
            add_val += sets[att]
        else:
            u.info[key] = 0
    u.info['used_gongli'] = add_val
    u.save_db()

def attr_add(u, sets):
    add_val = 0
    for att, key in att_trans.items():
        if att in sets:
            u.info[key] = u.info.get(key, 0) + sets[att]
            add_val += sets[att]
    u.info['used_gongli'] = u.info.get('used_gongli', 0) + add_val
    u.save_db()

def attr_get(u):
    msg = []
    msg.append('【%s】当前加点属性' % (u.nick_name))
    for k, v in att_trans.items():
        msg.append('%s: %d' % (k, u.info.get(v, 0)))
    if not u.info.get('job'):
        msg.append('剩余加点: %d' % (u.info.get('gongli', 0) - u.info.get('used_gongli', 0)) )

    return '\n'.join(msg)

def attr_funcs(u, message, other):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return attr_desc()

    if attrs[1] == '查看':
        return attr_get(other or u)
    elif attrs[1] == '设置':
        if u.info.get('job'):
            return '【%s】当前已经转职, 不再支持设置加点' % (u.nick_name)
        sets = {}
        add_val = 0
        for k in attrs[2:]:
            tmp = k.split('=')
            one_val = int(tmp[-1])
            if tmp[0] in att_trans:
                if one_val < 0:
                    return '【%s】加点不可以设置为负值' % (u.nick_name)
                sets[tmp[0]] = one_val
                add_val += one_val
        if add_val == 0:
            return '【%s】不加点玩呢？' % (u.nick_name)

        if add_val > u.info.get('gongli', 0):
            return '【%s】设置的加点超过当前功力, 请继续晨练或者奇遇' % (u.nick_name)
        attr_set(u, sets)
        left = u.info['gongli'] - u.info['used_gongli']
        if left > 0:
            return '【%s】加点设置成功, 剩余可分配功力%d' % (u.nick_name, left)
        else:
            return '【%s】加点设置成功' % (u.nick_name)
    elif attrs[1] == '增加':
        if u.info.get('job'):
            return '【%s】当前已经转职, 不再支持设置加点' % (u.nick_name)
        sets = {}
        add_val = 0
        have_val = False
        for k in attrs[2:]:
            tmp = k.split('=')
            one_val = int(tmp[-1])
            if tmp[0] in att_trans:
                if one_val + u.info.get(att_trans[tmp[0]], 0) < 0:
                    return '【%s】加点不可以设置为负值' % (u.nick_name)
                sets[tmp[0]] = one_val
                add_val += one_val
                have_val = have_val or (one_val != 0)
        if add_val == 0 and not have_val:
            return '【%s】不加点玩呢？' % (u.nick_name)

        if add_val + u.info.get('used_gongli', 0) > u.info.get('gongli', 0):
            return '【%s】设置的加点超过当前功力, 请继续晨练或者奇遇' % (u.nick_name)
        attr_add(u, sets)
        left = u.info['gongli'] - u.info['used_gongli']
        if left > 0:
            return '【%s】加点增加成功, 剩余可分配功力%d' % (u.nick_name, left)
        else:
            return '【%s】加点增加成功' % (u.nick_name)
    elif attrs[1] == '重置':
        if u.info.get('job'):
            return '【%s】当前已经转职, 不再支持设置加点' % (u.nick_name)
        for k in att_map:
            u.info[k] = 0
        u.info['used_gongli'] = 0
        u.save_db()
        return '【%s】加点重置成功' % (u.nick_name)