
def func_add(n1, n2):
    return n1 + n2

def func_mul(n1, n2):
    return n1 * n2

char2func = {
    '乘': func_mul,
    'multi': func_mul,
    'plus': func_add,
    '加': func_add
}

def get_int(num):
    try:
        return int(num.replace(',', '').strip())
    except:
        return 0

def auto_chuanlaoxiuxian(message):
    question = message.split('题曰：')[-1].split(' 为几何')[0]
    answer = 0
    for func_name, func in char2func.items():
        if func_name in question:
            questions = question.split(func_name)
            answer = func(get_int(questions[0]), get_int(questions[1]))
            break

    return '神兽 %d' % (answer)

__cl_group_id = 10010
__cl_robot_id = 10010
__cl_call_id = 10010
ss_state, ss_number, ss_min, ss_max, ss_wrong = False, 0, 0, 49, []
def guess_number(group, member, message):
    if group.id != __cl_group_id:
        return

    global ss_state, ss_number, ss_min, ss_max, ss_wrong
    if member.id == __cl_call_id and message == '驯服 1753363989' and not ss_state:
        ss_state = True
        return

    if not ss_state:
        return

    if member.id != __cl_robot_id:
        return

    if '紫微大帝的福地' in message:
        ss_state = False
        return

    if message.startswith('紫微大帝猜中了神兽心中所想'):
        print(ss_state, ss_number, ss_min, ss_max, ss_wrong)
        ss_state, ss_number, ss_min, ss_max, ss_wrong = False, 0, 0, 49, []
        return

    if message.startswith('神兽口吐人言'):
        ss_number = 24
        return '神兽 %d' % (ss_number)
    elif message.startswith('吾心中之数') and '多之甚' in message:
        ss_wrong.append(ss_number)
        ss_min = ss_number + 10
    elif message.startswith('吾心中之数') and '较大' in message:
        ss_wrong.append(ss_number)
        ss_min = ss_number + 1
        ss_max = min(ss_max, ss_number + 10)
    elif message.startswith('吾心中之数') and '小之甚' in message:
        ss_wrong.append(ss_number)
        ss_max = ss_number - 10
    elif message.startswith('吾心中之数') and '较小' in message:
        ss_wrong.append(ss_number)
        ss_max = ss_number - 1
        ss_min = max(ss_min, ss_number -10)
    else:
        return

    ss_number = int((ss_min + ss_max) / 2)
    if ss_number in ss_wrong:
        ss_number, ss_min, ss_max, ss_wrong = 24, 0, 49, []
    return '神兽 %d' % (ss_number)

def cl_ctl(group, member, message):
    if ' 为几何' in message:
        return auto_chuanlaoxiuxian(message)
    elif '紫微大帝的福地中的神兽厉害非凡' in message:
        return '驯服'
    else:
        answer = guess_number(group, member, message)
        if answer:
            return answer