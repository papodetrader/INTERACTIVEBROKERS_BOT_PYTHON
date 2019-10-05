from plan import build_plan
from variable import execution, plan, read_variables
from calendario import calendar
import os
import time
import datetime as dt
import pandas as pd
import pickle
import pytz
import warnings
warnings.filterwarnings("ignore")

calendar = calendar()
print('\n', calendar[0])
print('\n', calendar[1], '\n')

while True:
    starttime = time.time()

    if dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).weekday() in [0, 1, 2, 3, 4]: 

        if execution.current_time() > 000 and execution.current_time() < 100:
            new_plan = (f'plan_{dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()}')
            if new_plan not in os.listdir('./DATA/plan/'):            
                build_plan().run_daily() 
                read_variables() 

        elif execution.current_time() > max(pd.DataFrame(plan.values(), plan.keys()).end)+300 or execution.current_time() > 2200:
            execution.close_all()

        else:
            for id in plan: 
                curr = plan[id]['asset']

                execution.condition(id, curr) 

            x1 = int(time.time() - starttime)
            print(f'execution.condition took {x1} seconds')

            execution.order_update() 

            execution.day_mgt()


        print(f'stopped for {int((60.0 - ((time.time() - starttime) % 60.0)))} seconds at {str(execution.current_time())[:-2]+":"+str(execution.current_time())[-2:]} \n')
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    else:
        print(f'stopped for {int((3600.1 - ((time.time() - starttime) % 60.0)))} seconds at {str(execution.current_time())[:-2]+":"+str(execution.current_time())[-2:]} \n')
        time.sleep(3600.1 - ((time.time() - starttime) % 60.0))


        
