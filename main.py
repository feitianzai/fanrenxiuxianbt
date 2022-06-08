from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, Member, Group, MiraiSession

from config import mirai_info, group_whitelist, master_id
from controls import call_ctl

app = Ariadne(MiraiSession(host=mirai_info['host'], verify_key=mirai_info['verify_key'], account=mirai_info['account']))

@app.broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend, message: MessageChain):
    msg = call_ctl(None, friend, message)
    if msg:
        await app.sendMessage(friend, MessageChain.create([Plain(msg)]))

@app.broadcast.receiver("GroupMessage")
async def friend_message_listener(app: Ariadne, member: Member, group: Group, message: MessageChain):
    if group.id not in group_whitelist:
        return
    # if member.id != master_id:
    #     return

    msg = call_ctl(group, member, message)
    if msg:
        await app.sendMessage(group, MessageChain.create([Plain(msg)]))

app.launch_blocking()