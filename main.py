import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='YearoneInvest',
    appId = 'wxb6c1126cee0cb7a6',
    appSecret = '4bcf6c3e704f7f27af33f53daab5bc66'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['Content']

itchatmp.run()
