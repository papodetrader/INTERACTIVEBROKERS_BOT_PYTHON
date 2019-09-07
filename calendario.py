from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import requests
import logging
import csv
import re

def getEconomicCalendar(day):
    ''' got code from https://github.com/swishderzy and made some modifications'''

    startlink = f"calendar.php?week=sep{day}.2019"

    calendar = {}
    No = 0

    # get the page and make the soup
    baseURL = "https://www.forexfactory.com/"
    r = requests.get(baseURL + startlink)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    # get and parse table data, ignoring details and graph
    table = soup.find("table", class_="calendar__table")

    # do not use the ".calendar__row--grey" css selector (reserved for historical data)
    trs = table.select("tr.calendar__row.calendar_row")
    fields = ["date","time","currency","impact","event","actual","forecast","previous"]

    # some rows do not have a date (cells merged)
    curr_year = startlink[-4:]
    curr_date = ""
    curr_time = ""
    for tr in trs:

        # fields may mess up sometimes, see Tue Sep 25 2:45AM French Consumer Spending
        # in that case we append to errors.csv the date time where the error is
        try:
            for field in fields:
                data = tr.select("td.calendar__cell.calendar__{}.{}".format(field,field))[0]
                # print(data)
                if field=="date" and data.text.strip()!="":
                    curr_date = data.text.strip()
                elif field=="time" and data.text.strip()!="":
                    # time is sometimes "All Day" or "Day X" (eg. WEF Annual Meetings)
                    if data.text.strip().find("Day")!=-1:
                        curr_time = "12:00am"
                    else:
                        curr_time = data.text.strip()
                elif field=="currency":
                    currency = data.text.strip()

                elif field=="impact":
                    # when impact says "Non-Economic" on mouseover, the relevant
                    # class name is "Holiday", thus we do not use the classname
                    impact = data.find("span")["title"].split(' ')[0]
                elif field=="event":
                    event = data.text.strip()
            
            No += 1

            if int(curr_time.split(':')[0]) > 12 or curr_time[-2:] == 'pm':
                pass
            else:
                curr_time = str(int(curr_time.split(':')[0]) +7) + ':' + curr_time.split(':')[1][:2]

            
            date_cal = dt.datetime.strptime(",".join([curr_year, curr_date, curr_time]),
                                                "%Y,%a%b %d,%H:%M")

            calendar.update({No: {'date': date_cal.date(), 'time': date_cal.time(), 'currency': currency, 'impact': impact, 'event': event}})

        except:
            pass
        
        result = pd.DataFrame(calendar.values(), calendar.keys())

    result = result[result.currency.isin(['CNY', 'EUR', 'USD', 'JPY', 'GBP', 'AUD', 'CAD'])].set_index('date')
    result = result[result.index < result.index.unique()[1]]

    return result