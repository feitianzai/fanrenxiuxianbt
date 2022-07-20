import pk

def battle_desc():
    msg = []
    msg.append('【竞技场说明】')
    msg.append('挑战命令:  竞技 挑战 名次')
    msg.append('如果当前没有名次, 则自动归位到最后一名')
    msg.append('如果当前挑战的名次高于自己, 则获胜后交换名次')
    msg.append('查看命令:  竞技 查看')
    msg.append('返回当前竞技场前十的道友')
    return '\n'.join(msg)

def battle_view(gs):
    msg = []
    msg.append('【烦人修仙bt服】竞技场')

    idx = 1
    for ins in gs.info.get('battle', []):
        player = gs.get_user(ins)
        msg.append('% 2d: %s' % (idx, player and player.nick_name))
        idx += 1

    return '\n'.join(msg)

def battle_fight(u, rank):
    gs = u.get_gs()

    now_rank_list = gs.info.get('battle', [])
    if len(now_rank_list) > 0 and rank > (len(now_rank_list) + 1):
        return '【%s】名次错误' % (u.nick_name)

    if len(now_rank_list) == 0:
        now_rank_list.append(u.name)
        gs.info['battle'] = now_rank_list
        gs.save_db()
        return '恭喜【%s】成为本服第一个挑战竞技场的道友, 自动夺得榜首' % (u.nick_name)

    if rank == len(now_rank_list) + 1:
        if u.name not in now_rank_list:
            now_rank_list.append(u.name)
            gs.info['battle'] = now_rank_list
            gs.save_db()
            return '【%s】荣登竞技场第%d名' % (u.nick_name, rank)
        else:
            return '【%s】当前排名不易, 不要自甘堕落' % (u.nick_name)

    cur_rank, idx, other = -1, 0, gs.get_user(now_rank_list[rank - 1])
    for ins in now_rank_list:
        idx += 1
        if ins == u.name:
            cur_rank = idx
            break

    if cur_rank == -1:
        now_rank_list.append(u.name)
        cur_rank = len(now_rank_list)
    elif cur_rank == rank:
        return '【%s】挑战自己作甚？' % (u.nick_name)

    _, is_win, _ = pk.fight(u, other)
    if not is_win:
        return '【%s】挑战第%d名【%s】失败, 名次不变' % (u.nick_name, rank, other.nick_name)

    if rank > cur_rank:
        return '【%s】挑战第%d名【%s】成功' % (u.nick_name, rank, other.nick_name)

    now_rank_list[rank - 1] = u.name
    now_rank_list[cur_rank - 1] = other.name
    gs.info['battle'] = now_rank_list
    gs.save_db()
    return '【%s】挑战【%s】成功, 成为晋升为第%d名' % (u.nick_name, other.nick_name, rank)

def funcs(u, message):
    infos = message.strip().split(' ')
    if len(infos) == 1:
        return battle_desc()

    if infos[1] == '查看':
        return battle_view(u.get_gs())

    if infos[1] == '挑战':
        if len(infos) < 3:
            return '【%s】请输入挑战的名次' % (u.nick_name)
        return battle_fight(u, int(infos[2]))
