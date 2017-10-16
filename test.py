import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token = 'YearoneInvest',
    appId = 'wxb6c1126cee0cb7a6',
    appSecret = '4bcf6c3e704f7f27af33f53daab5bc66'))

leoId = 'o76L3w8Qg94y3efLpwm_Caor8oxw'

def send_leo(message):
    r = itchatmp.send(message, leoId)
    print(r)



