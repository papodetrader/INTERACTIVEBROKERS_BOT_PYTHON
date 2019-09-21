import datetime as dt
import pandas as pd
import pytz



def calendar():
    try:
        df = pd.read_pickle('./calendar')
    except:
        df = pd.DataFrame()
        pass
    
    if dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() in df.index.unique():
        df = df[df.index.date == dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]
        return df

    else:
        df = pd.read_html('https://tradingeconomics.com/calendar')[1]

        lt = []
        for i in df.columns:
            for ii in i:
                if '2019' in ii:
                    lt.append(ii)

        first_date = pd.to_datetime(lt[0]).date()


        df.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        df = df[[1, 2, 3]]

        df[1] = pd.to_datetime(df[1])

        df[1] = df[1] + dt.timedelta(hours=3)
        df = df.dropna()
        df.columns = ['date', 'country', 'description']
        df.set_index('date', inplace=True)

        if first_date != dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date():
            date = dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() - first_date
            df.index = df.index - date    

        lt = [0]
        start = 0
        last = 0
        cal = pd.DataFrame()

        for i in range(len(df)):

            if df.iloc[i].name.hour >= max(lt):

                lt.append(df.iloc[i].name.hour)

                start = i

            else:

                lt = [0]

                day = df.iloc[last:start+1]

                last = start+1

                if len(cal) > 0:
                    day.index = day.index + dt.timedelta(1)
                    df.index = df.index + dt.timedelta(1)

                cal = pd.concat([cal, day], sort=True)

        df = cal.copy(deep=True)


        if dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() == df.index[0].date():
            weekday = 4 - df.index[0].weekday()
            df = df[df.index.date <= (dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() + dt.timedelta(weekday))]
        else:
            weekday = dt.timedelta(4) - (dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() - df.index[0].date())
            df = df[df.index.date <= (dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() + weekday)]


        pd.to_pickle(df, './calendar')

        df = df[df.index.date == dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]

        return df


def cal_list(tempo):

    tempo_min = tempo - dt.timedelta(hours=1)
    tempo_max = tempo + dt.timedelta(hours=1)

    cal = calendar()

    range_time = [i for i in cal.index if i.time() > tempo_min.time() and i.time() < tempo_max.time()]

    cal = cal[cal.index.isin(range_time)]

    events = [(cal.iloc[i].name, cal.iloc[i].country, cal.iloc[i].description) for i in range(len(cal))]

    return events

