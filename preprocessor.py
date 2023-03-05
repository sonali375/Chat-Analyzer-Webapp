import re
import pandas as pd

def preprocess(data):
    pattern = "\d{2}\/\d{2}\/\d{4},\s\d{1,2}:\d{1,2}:\d{1,2}\s[A-Z][A-Z]\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'date_time': dates, 'user_msg': messages})
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y, %H:%M:%S %p - ')

    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i)
        if (a[1:]):
            usernames.append(a[1])
            msgs.append(a[2])
        else:
            usernames.append("group_notification")
            msgs.append(a[0])

    df['user'] = usernames
    df['message'] = msgs
    df.drop('user_msg', axis=1, inplace=True)

    df['day'] = df['date_time'].dt.strftime('%a')
    df['month'] = df['date_time'].dt.strftime('%b')
    df['date'] = df['date_time'].dt.date
    df['month_num'] = df['date_time'].dt.month
    df['year'] = df['date_time'].dt.year
    df['day_name'] = df['date_time'].dt.day_name()
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['second'] = df['date_time'].dt.second
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df