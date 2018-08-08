from Linephu.linepy import *
from Linephu.akad.ttypes import *



client = LINE()
client.log("Auth Token : " + str(client.authToken))

oepoll = OEPoll(client)
mode='on'

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        client.acceptGroupInvitation(op.param1)
        JoinedGroups.append(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return

def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    try:
        if mode == 'on':
            client.sendMessage(op.param1, "這種行為 不太對吧......")
            client.kickoutFromGroup(op.param1, [op.param2])
            client.findAndAddContactsByMid(op.param3)
            client.inviteIntoGroup(op.param1, [op.param3])
        else:
            pass
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_CANCEL_INVITATION_GROUP\n\n")
        return

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 2:
                    if msg.text == "on":
                        mode = 'on'
                        client.sendMessage(msg.to, "保護程序已啟動")
                    if msg.text == "off":
                        mode = 'off'
                        client.sendMessage(msg.to, "保護程序已關閉")
                    if msg.text == "/bye":
                        client.sendMessage(msg.to, "各位再見囉!!!!!")
                        client.leaveGroup(msg.to)
                        JoinedGroups.remove(msg.to)
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as e:
        print(e)
        print("\n\nRECEIVE_MESSAGE\n\n")
        return



oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_CANCEL_INVITATION_GROUP: NOTIFIED_CANCEL_INVITATION_GROUP,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

while True:
    oepoll.trace()
