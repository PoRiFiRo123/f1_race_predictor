import fastf1
import pandas as pd

def get_circuit_statistics(circuit_name, current_year):
    fastf1.Cache.enable_cache('./cache')
    years = list(range(current_year - 10, current_year + 1))
    winners = []

    for year in years:
        schedule = fastf1.get_event_schedule(year)
        for _, session in schedule.iterrows():
            if session['EventName'] != circuit_name or session['EventFormat'] != 'conventional':
                continue
            try:
                race = fastf1.get_session(year, session['EventName'], 'R')
                race.load()
                result = race.results
                winner = result[result['Position'] == 1]['Abbreviation'].values[0]
                winners.append(winner)
            except Exception as e:
                continue

    stats = pd.Series(winners).value_counts().reset_index()
    stats.columns = ['Driver', 'Wins']
    return stats
