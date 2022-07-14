# 职业
from util import att_map

jobs = {
    'pal': {
        'name': '体修',
        'desc': '拥有超多的生命, 均衡的攻防, 一般的命中韧性, 不善于闪避暴击',
        'attr': {
            'hp': 6,
            'attack': 1.9,
            'defend': 1.9,
            'hit': 0.12,
            'dodge': 0.01,
            'critical': 0.01,
            'tough': 0.06,
        },
        'need_realm': 2,
    },
    'bar': {
        'name': '剑修',
        'desc': '拥有一般的生命, 超高的攻击暴击, 一般的命中闪避, 不善于防御和韧性',
        'attr': {
            'hp': 5.9,
            'attack': 2.1,
            'defend': 1.8,
            'hit': 0.1,
            'dodge': 0.02,
            'critical': 0.06,
            'tough': 0.02,
        },
        'need_realm': 2,
    },
    'asn': {
        'name': '杀手',
        'desc': '拥有一般的生命, 超高的暴击闪避, 一般的攻击命中, 不善于防御和韧性',
        'attr': {
            'hp': 5.8,
            'attack': 2.05,
            'defend': 1.85,
            'hit': 0.1,
            'dodge': 0.05,
            'critical': 0.12,
            'tough': 0.03,
        },
        'need_realm': 2,
    },
}

def check_config():
    for job, job_item in jobs.items():
        total = 0
        for val in job_item['attr'].values():
            total += val
        assert total != 1

check_config()

def get_attrs(u, job):
    job_item = jobs[job]
    gongli = u.info.get('gongli')
    attrs = {}
    for attr_name, val in job_item['attr'].items():
        attrs[attr_name] = int(val * gongli)
    return attrs

def job_desc(u):
    msg = []
    msg.append('【职业】系统介绍')
    msg.append('拥有职业后, 一点功力可以加点多个属性, 且不同职业拥有不同侧重')
    msg.append('可发送 职业 转职 职业名称进行转职')
    for job_name, job_item in jobs.items():
        msg.append('%s: %s' % (job_item['name'], job_item['desc']))
    job = u.info.get('job')
    if job:
        attrs = get_attrs(u, job)
        msg.append('【%s】当前职业【%s】, 加点为' % (u.nick_name, jobs[job]['name']))
        for attr_name, val in attrs.items():
            msg.append('%s: %d' % (att_map[attr_name], val))

    return '\n'.join(msg)

def job_set(u, message):
    job_name = message.split(' ')[-1]
    for job, job_item in jobs.items():
        if job_item['name'] == job_name:
            if u.info.get('realm', 0) < job_item['need_realm']:
                return '【%s】当前境界不足, 请努力修炼, 早日转职' % (u.nick_name)
            u.info['job'] = job
            attrs = get_attrs(u, job)
            for attr_name, val in attrs.items():
                u.info[attr_name] = val
            u.save_db()
            return '【%s】成功转职为【%s】' % (u.nick_name, job_name)

    return '【%s】想要转职为%s, 但是仙界仍未开放该职业' % (u.nick_name, job_name)

def funcs(u, message):
    attrs = message.split(' ')
    if len(attrs) == 1:
        return job_desc(u)

    if attrs[1] == '转职':
        return job_set(u, message)