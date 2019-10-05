import datetime as dt
import pandas as pd
import pytz



def calendar():
    try:
        df = pd.read_pickle('./calendar')[0]
        holiday = pd.read_pickle('./calendar')[1]
    except:
        df = pd.DataFrame()
        pass
    
    if dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() in df.index.unique():
        df = df[df.index.date == dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]
        return df, holiday

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

        x = df[df.index.date == dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]

        df = [df, holidays()]

        pd.to_pickle(df, './calendar')

        return x, df[1]


def cal_list(tempo):

    tempo_min = tempo - dt.timedelta(hours=1)
    tempo_max = tempo + dt.timedelta(hours=1)

    cal = calendar()[0]

    range_time = [i for i in cal.index if i.time() > tempo_min.time() and i.time() < tempo_max.time()]

    cal = cal[cal.index.isin(range_time)]

    events = [(cal.iloc[i].name, cal.iloc[i].country, cal.iloc[i].description) for i in range(len(cal))]

    return events


def holidays():

    df = pd.read_html('https://tradingeconomics.com/holidays')

    df = df[0][[0, 2, 3]].fillna(method='ffill').rename({0: 'temp', 2: 'country', 3: 'description'}, axis=1)

    lt = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    countries = {
        'Germany': 'EUR', 
        'China': 'CNH', 
        'Australia': 'AUD', 
        'Switzerland': 'CHF',
        'Hong Kong': 'HKD', 
        'India': 'INR', 
        'Spain': 'EUR', 
        'Brazil': 'BRL', 
        'United States': 'USD', 
        'Japan': 'JPY', 
        'Canada': 'CAD', 
        'New Zealand': 'NZD', 
        'Turkey': 'TRY', 
        'France': 'EUR', 
        'Italy': 'EUR', 
        'Sweden': 'SEK', 
        'Mexico': 'MXN', 
        'South Africa': 'ZAR', 
        'Norway': 'NOR', 
        'Netherlands': 'EUR', 
        'United Kingdom': 'GBP',
    }


    date = {}

    for i in range(len(df)):
        x = df.temp.iloc[i].split('/')
        y = [lt.get(i) for i in lt.keys() if i == x[0]][0]
        xx = dt.datetime(2019, y, int(x[1])).date()

        date.update({df.iloc[i].name: (xx, countries.get(df.iloc[i].country))})

    df = pd.concat([df, pd.DataFrame(date.values(), date.keys())], axis=1).rename({0: 'date', 1: 'currency'}, axis=1).set_index('date').drop('temp', axis=1)
    df = df[df.country.isin(countries.keys())]

    df = df[df.index == dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]


    return df

