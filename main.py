from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, Member, Group, MiraiSession

from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

from config import mirai_info, group_whitelist, master_id
from controls import call_ctl, frame_update

app = Ariadne(MiraiSession(host=mirai_info['host'], verify_key=mirai_info['verify_key'], account=mirai_info['account']))
scheduler = app.create(GraiaScheduler)
@scheduler.schedule(crontabify("* * * * * *"))
def main_update():
    frame_update()

@app.broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend, message: MessageChain):
    msg = call_ctl(None, friend, message)
    if msg:
        await app.sendMessage(friend, MessageChain.create([Plain(msg)]))

@app.broadcast.receiver("GroupMessage")
async def friend_message_listener(app: Ariadne, member: Member, group: Group, message: MessageChain):
    if group.id not in group_whitelist:
        return

    msg = call_ctl(group, member, message)
    if msg:
        await app.sendMessage(group, MessageChain.create([Plain(msg)]))

app.launch_blocking()