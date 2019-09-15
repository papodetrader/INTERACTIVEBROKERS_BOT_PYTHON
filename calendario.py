import datetime as dt
import pandas as pd
import pytz



def calendar():
    try:
        df = pd.read_pickle('./calendar')
    except:
        df = pd.DataFrame()
        pass

    if dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() in df.index:
        return df

    else:
        df = pd.read_html('https://tradingeconomics.com/calendar')[1]
        df.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        df = df[[1, 2, 3]]

        df[1] = pd.to_datetime(df[1])

        cal = {}
        count = 0

        for i in range(len(df)):
            if len(cal.keys()) == 0:
                cal.update({count: {'date': df.iloc[i][1], 'description': df.iloc[i][3], 'country': df.iloc[i][2]}})
            elif len(cal.keys()) > 0 and cal.get(i-1) != None:
                if df.iloc[i][1] >= cal.get(i-1)['date']:
                    cal.update({count: {'date': df.iloc[i][1], 'description': df.iloc[i][3], 'country': df.iloc[i][2]}})
            count += 1

        df = pd.DataFrame(cal.values(), cal.keys()).set_index('date')
        df.index = df.index + dt.timedelta(hours=3)

        pd.to_pickle(df, './calendar')

        return df


def cal_list(tempo):

    tempo_min = tempo - dt.timedelta(hours=1)
    tempo_max = tempo + dt.timedelta(hours=1)

    cal = calendar()

    range_time = [i for i in cal.index if i > tempo_min and i < tempo_max]

    cal = cal[cal.index.isin(range_time)]

    events = [(cal.iloc[i].name, cal.iloc[i].country, cal.iloc[i].description) for i in range(len(cal))]

    return events


