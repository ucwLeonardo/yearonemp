import itchatmp
from yearonequant.util_quant import *
from yearonequant.event_object import *


itchatmp.update_config(itchatmp.WechatConfig(
    token = 'YearoneInvest',
    appId = 'wxb6c1126cee0cb7a6',
    appSecret = '4bcf6c3e704f7f27af33f53daab5bc66'))

# userId = 'o76L3w8Qg94y3efLpwm_Caor8oxw'
# r = itchatmp.send('Hi Leo : )', userId)
# print(r)
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    text = msg['Content']
    # push event list
    if text[0] == 'E':
        text = text.replace(' ', '')
        event_name_chinese = text[1:]
        event_name = EVENT_NAME_C2E.get(event_name_chinese)
        if event_name:  # has this event
            print('pushing event {}'.format(event_name))

            today = datetime.datetime.now() - datetime.timedelta(days=1)
            today_str = datetime2ymd_str(today)

            file_path = 'file/event/{}/{}.txt' \
                .format(today_str, event_name)
            html_path = 'file/event/{}/{}.html' \
                .format(today_str, event_name)

            # read text file
            with open(file_path) as file:
                content = file.read()
            # give a link to html page if list too long
            if len(content) > 1000:
                url = "http://139.224.234.82:8653/event/acquire?file={}" \
                    .format(html_path)
                hyper_link = "<a href=\"{}\">此链接</a>".format(url)
                content = '因列表过长，只摘选部分事件，请点击{}查看完整列表。\n\n' \
                          .format(hyper_link) + content
                content = content[:1000]
                content = content[:content.rfind('\n')] + '\n...\n'
        else:
            content = '目前暂不支持事件{}，请尝试点击获取事件按钮。'\
                .format(event_name_chinese)

    else:
        content = "请告诉我您关心的事件吧，回复E+事件名"

    return content

@itchatmp.msg_register(itchatmp.content.EVENT)
def event_reply(msg):
    if msg['Event'] == 'CLICK':
        if msg['EventKey'] == 'acquire_event':
            event_names = '，'.join(EVENT_NAME_C2E.keys())
            content = '回复 E+事件名 可获得近7日发生该事件的股票列表。\n\n' \
                      '比如回复： E增持， 便可获得增持事件的列表。\n\n' \
                      '目前支持的事件有：\n{}。'.format(event_names)
            return content

        if msg['EventKey'] == 'about_us':
            print("handle about_us")
            content = "YearOne(新晋元年)是一家创业中的量化对冲基金公司。" \
                      "创始团队具有多年、多市场、多交易标的的投资经验，并以" \
                      "最严格的合规性与职业道德准准则来要求自己，通过借助" \
                      "交叉学科的力量持续创新，不停改进自己的投资方法。"
            return content

itchatmp.run(debug=True)
