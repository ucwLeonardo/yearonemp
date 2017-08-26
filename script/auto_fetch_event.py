from yearonequant.event import *
from yearonequant.event_object import *

from subprocess import call
import os.path
import os
import re

from collections import defaultdict  # listmultimap

# solve the error: NotImplementedError: Implement enable_gui in a subclass
from IPython import get_ipython
ip = get_ipython()
ip.enable_gui = lambda x: False
# initialize rqdatac to enable online functions such as get_price()
rqdatac.init('xinjin', '123456', ('172.19.182.162', 16003))


def previous_days_event2file(days_before_today):
    """
    Keep only days before today's event, save to a separate file
    :param days_before_today:   number of days before today
    :return:    file path of written file
    """

    today = datetime.datetime.now() - datetime.timedelta(days=1)
    start_date = today - datetime.timedelta(days=days_before_today)

    today_str = datetime2ymd_str(today)
    start_str = datetime2ymd_str(start_date)
    start_display = start_date - datetime.timedelta(days=1)
    start_display_str = datetime2ymd_str(start_display)

    directory = './file/event/{}'.format(today_str)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    write_file_path = './file/event/{}/events_from_{}_to_{}.csv' \
        .format(today_str, start_display_str, today_str)

    # return if already has the file
    if os.path.isfile(write_file_path):
        return write_file_path

    print("generating previous {} days announcement file..."
          .format(days_before_today))

    fd = open(write_file_path, "wb")
    pattern_argument = "0,/{}/p".format(start_str)
    call(["sed", "-n", pattern_argument,
          "../Documents/announcements_abstract.csv"], stdout=fd)

    print('file saved as {}\n'.format(write_file_path))
    return write_file_path


def event_to_push_to_file(announce_file, event_name, all_event_dict, days_before_today=7):
    """

    :param announce_file:       announcement file crawled from info
    :param event_name:          name of event in English, should be a key of all_event_dict
    :param all_event_dict:      dict of event_object, defined in yearonequant.event module
    :param days_before_today:   number of days previously
    :return:    DataFrame of filtered events
    """
    print("\nnow generating event list files for {}...".format(event_name))

    if event_name not in all_event_dict:
        print("event {} has not been defined yet".format(event_name))
        return

    event_dict = all_event_dict.get(event_name)

    # get param for filter
    target_words = event_dict.target_words
    filter_words = event_dict.filter_words
    filter_mode = event_dict.filter_mode

    count = 0
    lines = str()
    series_list = list()
    df = read_announce_csv(announce_file)

    # loop over rows of df
    found_dict = defaultdict(list)  # code to title map, make list unique
    for date, row in df.iterrows():
        code = complete_code(str(row['Code']))
        if not code:
            continue
        info = instruments(code)
        if not info:
            continue
        symbol = info.symbol
        title = row['Title']

        passed = filter_title(title, target_words, filter_words, filter_mode)
        if date and symbol and passed:
            if code in found_dict and title in found_dict[code]:
                continue     # pass if same title already in dict
            found_dict[code].append(title)
            # prepare DataFrame content
            series_list.append(transform_event_series(row))

            count += 1

    filtered_event_df = pd.DataFrame(series_list)
    return filtered_event_df


def event_to_push2file(event_name, days_before_today=7):
    """
    Save specific events into human-readable format, for pushing to wechat user.
    :param event_name:          event name
    :param days_before_today:   number of days to look back
    :return:    void
    """

    print("\nnow generating event list files for {}...".format(event_name))

    if event_name not in ALL_EVENTS:
        print("event {} has not been defined yet".format(event_name))
        return

    event_dict = ALL_EVENTS.get(event_name)

    announce_path = str(previous_days_event2file(days_before_today))

    matcher_start = re.match('.+from_(.+)_to.+', announce_path)
    matcher_end = re.match('.+to_(.+)\.csv', announce_path)
    start_str = matcher_start.group(1)
    today_str = matcher_end.group(1)

    write_file_path = './file/event/{}/{}.txt'\
        .format(today_str, event_name)
    write_fd = open(write_file_path, 'w+')

    # get param for filter
    target_words = event_dict.target_words
    filter_words = event_dict.filter_words
    filter_mode = event_dict.filter_mode

    count = 0
    lines = str()
    series_list = list()
    df = read_announce_csv(announce_path)

    # loop over rows of df
    found_dict = defaultdict(list)  # code to title map, make list unique
    for date, row in df.iterrows():
        code = complete_code(str(row['Code']))
        if not code:
            continue
        info = instruments(code)
        if not info:
            continue
        symbol = info.symbol
        title = row['Title']

        passed = filter_title(title, target_words, filter_words, filter_mode)
        if date and symbol and passed:
            if code in found_dict and title in found_dict[code]:
                continue     # pass if same title already in dict
            found_dict[code].append(title)
            # prepare txt file content
            title_url = "<a href=\"{}\">{}</a>".format(row['Link'], row['Title'])
            line = "股票名称:{}, 公告标题:{}, 发布时间:{}\n\n".format(symbol, title_url, date)
            lines += line
            # prepare html file content
            series_list.append(transform_event_series(row))

            count += 1

    # write to txt file
    write_fd.write("以下是从{}到{}的共{}个 {} 事件\n"
                   "点击蓝色\"公告标题\"查阅公告全文\n\n"
                   .format(start_str, today_str, count, event_dict.chinese_name))
    write_fd.write(lines)

    # write to html file
    filtered_event_df = pd.DataFrame(series_list)
    html_file_path = './file/event/{}/{}.html'\
        .format(today_str, event_name)
    event_df2html(filtered_event_df, html_file_path)

    print("{} {} events, file saved as {}\n"
          .format(count, event_name, write_file_path))


def transform_event_series(series):
    """
    Transform a row of event in announcement df,
    to human-readable from.
    :param series:  event series
    :return:    human-readable series
    """
    code = complete_code(str(series['Code']))
    symbol = instruments(code).symbol
    title = series['Title']
    link = series['Link']
    time = series.name

    hyper_text = '<a href=\"{}\">{}</a>'.format(link, title)

    result = pd.Series({'股票名称': symbol, '公告标题': hyper_text, '发布时间': time})

    return result


def event_df2html(df, html_file_path):
    """
    Save DataFrame of events as html file.
    :param df:              input DataFrame
    :param html_file_path:  path to save the html file
    :return:    void
    """

    write_fd = open(html_file_path, 'w')

    if df.shape[0] == 0:
        write_fd.write("近7天没有该事件")
        return

    styles = [
        hover(),
        dict(selector="th", props=[("font-size", "150%"),
                                   ("text-align", "center")])
        # dict(selector="caption", props=[("caption-side", "top")])
    ]

    css = df.style \
        .set_properties(**{'background-color': '#F0F8FF',
                           'color': 'black',
                           'border-color': 'white'}) \
        .set_table_styles(styles) \
        .render()

    html = "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n" \
           "<meta charset=\"utf-8\"/>\n</head>\n{}" \
           "</body>\n</html>\n".format(css)

    write_fd.write(html)
    print("html done")


def hover(hover_color="#3399FF"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])


if __name__ == '__main__':

    for event_name in ALL_EVENTS:
        event_to_push2file(event_name)
        print("#################### finished at {} ####################"
              .format(datetime.datetime.now()))
