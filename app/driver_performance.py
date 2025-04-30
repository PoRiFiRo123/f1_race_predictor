import fastf1
import pandas as pd
from datetime import datetime

def get_driver_last_3_races(driver_abbr, current_year):
    fastf1.Cache.enable_cache('./cache')
    years = list(range(current_year - 5, current_year + 1))
    race_results = []

    for year in reversed(years):
        schedule = fastf1.get_event_schedule(year)
        for _, session in schedule.iterrows():
            if session['EventFormat'] != 'conventional':
                continue
            try:
                race = fastf1.get_session(year, session['EventName'], 'R')
                race.load()
                result = race.results
                driver_result = result[result['Abbreviation'] == driver_abbr]
                if not driver_result.empty:
                    race_results.append({
                        'Year': year,
                        'Circuit': session['EventName'],
                        'Position': int(driver_result['Position'].values[0])
                    })
                    if len(race_results) == 3:
                        return pd.DataFrame(race_results)
            except Exception as e:
                continue
    return pd.DataFrame(race_results)
