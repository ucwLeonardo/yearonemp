import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='YearoneInvest',
    appId='wxb6c1126cee0cb7a6',
    appSecret='4bcf6c3e704f7f27af33f53daab5bc66'))

menu = {
        "button":
        [
            {
                "name": "事件",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "订阅事件",
                        "key": "subscribe_event"
                    },
                    {
                        "type": "click",
                        "name": "已订阅事件",
                        "key": "subscribed_event"
                    }
                ]
            },
            {
                "type": "click",
                "name": "关于我们",
                "key":  "about_us"
            }
          ]
    }

r = itchatmp.menu.create(menu)
print(r)
