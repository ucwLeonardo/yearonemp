import itchatmp
from yearonequant.util_quant import *
from yearonequant.event_object import *


itchatmp.update_config(itchatmp.WechatConfig(
    token='YearoneInvest',
    appId='wxb6c1126cee0cb7a6',
    appSecret='4bcf6c3e704f7f27af33f53daab5bc66'))

# get tag list
tag_list = itchatmp.users.get_tags()['tags']
# construct a map from event name to tag id
tag_dict_name2id = dict()
for tag in tag_list:
    if tag['name'][:2] == '订阅':
        tag_dict_name2id[tag['name'][2:]] = tag['id']
# construct a map from tag id to event name
# NOTICE: chinese name of this idct has no prefix '订阅'
tag_dict_id2name = dict()
for tag in tag_list:
    if tag['name'][:2] == '订阅':
        tag_dict_id2name[tag['id']] = tag['name'][2:]

# openId = 'o76L3w8Qg94y3efLpwm_Caor8oxw
# r = itchatmp.send('Hi Leo : )', openId)
# print(r)
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    text = msg['Content']
    openId = msg['FromUserName']
    nickname = ''
    try:
        nickname = itchatmp.users.get_user_info(openId)['nickname']
    except KeyError as ex:
        print('openId is {}'.format(openId))
        print(ex)

    # tag user for subscribing this event
    if text[0] == 'E':

        text = text.replace(' ', '')
        event_name_chinese = text[1:]
        print("handle subscribing of event {} for {}"
              .format(event_name_chinese, nickname))

        if event_name_chinese in tag_dict_name2id:  # can subscribe this event

            tagId = tag_dict_name2id[event_name_chinese]    # get tag id
            # tag the user
            itchatmp.users.add_users_into_tag(tagId, [openId])

            user_tagIds = itchatmp.users.get_tags_of_user(openId)['tagid_list']
            user_tags = [tag_dict_id2name[tag_id] for tag_id in user_tagIds]
            user_tags_str = '，'.join(user_tags)
            content = '您已成功订阅{}事件，将从明天开始推送。\n' \
                      '已关注事件：\n{}'.format(event_name_chinese, user_tags_str)

        else:
            content = '目前暂不支持订阅事件"{}"，请点击订阅事件按钮查看详情。'\
                .format(event_name_chinese)

    else:
        content = "请回复E+事件名,告诉我您想订阅的事件"

    return content

@itchatmp.msg_register(itchatmp.content.EVENT)
def event_reply(msg):
    openId = msg['FromUserName']
    nickname = ''
    try:
        nickname = itchatmp.users.get_user_info(openId)['nickname']
    except KeyError as ex:
        print('openId is {}'.format(openId))
        print(ex)

    if msg['Event'] == 'CLICK':

        if msg['EventKey'] == 'subscribed_event':
            print("handle subscribed_event for {} {}".format(nickname, openId))
            # get tag list
            tag_list = itchatmp.users.get_user_info(openId)['tagid_list']
            subscribed = [tag_dict_id2name[t] for t in tag_list]
            content = "您目前已订阅的事件有：\n{}".format(','.join(subscribed))
            return content

        if msg['EventKey'] == 'subscribe_event':
            print("handle subscribe_event for {} {}".format(nickname, openId))
            event_names = '，'.join(EVENT_NAME_C2E.keys())
            content = '回复 E+事件名 可订阅该事件，您将在每天上午8点半左右' \
                      '获得一条含有该事件列表的消息推送。\n\n' \
                      '比如回复： E增持， 便可订阅增持事件。\n\n' \
                      '目前支持的事件有：\n{}。'.format(event_names)
            return content

        if msg['EventKey'] == 'about_us':
            print("handle about_us for {} {}".format(nickname, openId))
            content = "YearOne(新晋元年)是一家创业中的量化对冲基金公司。" \
                      "创始团队具有多年、多市场、多交易标的的投资经验，并以" \
                      "最严格的合规性与职业道德准准则来要求自己，通过借助" \
                      "交叉学科的力量持续创新，不停改进自己的投资方法。"
            return content

itchatmp.run(debug=True)
