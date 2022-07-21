#buff

def buff_add_attr(u, attrs):
    for k, v in attrs:
        u.info[k] = u.info.get(k, 0) + v

def buff_add_attr_percent(u, attrs):
    for k, v in attrs:
        u.info[k] = u.info.get(k, 0) * (1 + v)

buff_config = {
    'add_attr': buff_add_attr,
    'add_attr_percent': buff_add_attr_percent,
}

def buff_trigger(u, buff_info):
    buff_type = buff_info['type']
    if buff_type in buff_config:
        buff_func = buff_config[buff_type]
        buff_func(u, buff_info['value'])
        return True
    else:
        return False
