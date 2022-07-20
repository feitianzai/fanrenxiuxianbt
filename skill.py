import random

def skill_ljyd_func(u, skill_level, skill_conf):
    info = {
        'trigger': skill_conf['level_num'][skill_level - 1] <= random.random(),
        'msg': None,
    }
    if info['trigger']:
        info['msg'] = '【%s】发动了%s, 提前发动了攻击' % (u.nick_name, skill_conf['name'])
        info['pass_turn'] = True
    return info

def skill_tdts_func(u, skill_level, skill_conf):
    damage = int(u.info.get('hp', 0) * skill_conf['level_num'][skill_level - 1])
    info = {
        'trigger': not not damage,
        'msg': None,
    }
    if info['trigger']:
        info['msg'] = '【%s】感受到了生命威胁, 发动%s造成%d的伤害' % (u.nick_name, skill_conf['name'], damage)
        info['damage'] = damage
    return info

skill_config = {
    '灵机一动': {
        'name': '灵机一动',
        'desc': '其他人发起战斗时, 有(10/20/30/40/50)%的几率先出手',
        'timing': 'on_attack',
        'level_num': [0.1, 0.2, 0.3, 0.4, 0.5],
        'view': '其他人发起战斗时, 有%d%%的几率先出手',
        'priority': 100,
        'func': skill_ljyd_func,
    },
    '天地同寿': {
        'name': '天地同寿',
        'desc': '受到致命攻击时, 对对方造成自身(10/20/30)%生命最大值的直接伤害',
        'timing': 'on_death',
        'level_num': [0.1, 0.2, 0.3],
        'view': '受到致命攻击时, 对对方造成自身%d%%生命最大值的直接伤害',
        'priority': 100,
        'func': skill_tdts_func,
    },
}

def skill_desc():
    msg = []
    msg.append('【技能系统说明】')
    msg.append('通过消耗技能点学习技能, 技能点为当前功力值除100后取整')
    msg.append('可用操作 (技能 学习 技能名称=技能等级), (技能 查看)')
    msg.append('【可学习技能列表】')
    for skill_name, skill_info in skill_config.items():
        msg.append('【%s】: %s' % (skill_name, skill_info['desc']))
    return '\n'.join(msg)

def skill_learn(u, infos):
    skills = u.info.get('skill', {})
    for item in infos[2:]:
        tmp = item.split('=')
        skill_name = tmp[0]
        skill_level = int(tmp[1])
        if skill_name not in skill_config or skill_level <= 0 or skill_level > len(skill_config[skill_name]['level_num']):
            return '【%s】技能学习指令错误' % (u.nick_name)
        skills[skill_name] = skill_level

    total_skill_level = sum(skills.values())

    gongli = u.info.get('gongli', 0)
    u_skill_level = int(gongli / 100)
    if total_skill_level > u_skill_level:
        return '【%s】功力不足以学习全部技能, 继续努力' % (u.nick_name)

    u.info['skill'] = skills
    u.save_db()
    msg = []
    msg.append('技能学习成功')
    msg.append(skill_view(u))
    return '\n'.join(msg)

def skill_view(u):
    skills = u.info.get('skill', {})
    if len(skills) == 0:
        return '【%s】还未学习任何技能' % (u.nick_name)

    msg = []
    msg.append('【%s】当前技能' % (u.nick_name))
    for skill_name, skill_level in skills.items():
        cur_skill_conf = skill_config[skill_name]
        skill_num = cur_skill_conf['level_num'][skill_level - 1] * 100
        msg.append('%s: %s' % (skill_name, cur_skill_conf['view'] % (skill_num)))

    return '\n'.join(msg)

def skill_trigger(u, timing):
    skills = u.info.get('skill', {})
    if len(skills) == 0:
        return {'trigger': False, 'msg': None}

    for skill_name, skill_level in skills.items():
        skill_conf = skill_config[skill_name]
        if timing != skill_conf['timing']:
            continue

        return skill_conf['func'](u, skill_level, skill_conf)

    return {'trigger': False}

def funcs(u, message):
    infos = message.strip().split(' ')
    if len(infos) == 1:
        return skill_desc()

    if infos[1] == '学习':
        return skill_learn(u, infos)

    if infos[1] == '查看':
        return skill_view(u)
