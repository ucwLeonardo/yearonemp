import itchatmp
from yearonequant.util_quant import *
from yearonequant.event_object import *

itchatmp.update_config(itchatmp.WechatConfig(
    token='YearoneInvest',
    appId='wxb6c1126cee0cb7a6',
    appSecret='4bcf6c3e704f7f27af33f53daab5bc66'))

today = datetime.datetime.now() - datetime.timedelta(days=1)
today_str = datetime2ymd_str(today)

tag_list = itchatmp.users.get_tags()['tags']
# construct a map from tag id to tag name
tag_dict_subscription = dict()
for tag in tag_list:
    if tag['name'][:2] == '订阅':
        tag_dict_subscription[tag['id']] = tag['name'][2:]

user_list = itchatmp.users.get_users()
openId_list = user_list['data']['openid']

for openId in openId_list:  # loop over users

    content = '点击蓝色链接可打开事件详细列表\n\n'
    tagId_list = itchatmp.users.get_tags_of_user(openId)['tagid_list']

    has_subscription = False
    # construct message content, which contains hyperlinks to event list
    for tagId in tagId_list:    # loop over user's tag ids
        if tagId in tag_dict_subscription:  # put tag id if it's subscription
            has_subscription = True
            event_name_chinese = tag_dict_subscription[tagId]
            event_name = EVENT_NAME_C2E.get(event_name_chinese)
            # prepare content
            html_path = 'file/event/{}/{}.html' \
                .format(today_str, event_name)
            url = "http://139.224.234.82:8653/event/acquire?file={}" \
                .format(html_path)
            # hyper_link = "<a href=\"{}\">{}</a>"\
            #     .format(url, event_name_chinese)
            link = "{}事件链接：\n{}"\
                .format(event_name_chinese, url)
            content += '{}\n\n'.format(link)

    if has_subscription:
        itchatmp.send(content, openId)  # send to user
    else:
        itchatmp.send('您还没有订阅事件，请点击\"订阅事件\"按钮查看详情', openId)
