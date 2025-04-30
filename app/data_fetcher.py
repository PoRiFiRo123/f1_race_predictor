import fastf1
import pandas as pd
import os

def fetch_race_data(year):
    cache_path = './cache'
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    fastf1.Cache.enable_cache(cache_path)
    sessions = fastf1.get_event_schedule(year)
    race_data = []

    for index, session in sessions.iterrows():
        if session['EventFormat'] == 'conventional':
            try:
                quali = fastf1.get_session(year, session['EventName'], 'Q')
                quali.load()
                race = fastf1.get_session(year, session['EventName'], 'R')
                race.load()

                for drv in quali.laps['Driver'].unique():
                    drv_race = race.laps.pick_drivers(drv)
                    if not drv_race.empty:
                        race_data.append({
                            'Year': year,
                            'Circuit': session['EventName'],
                            'Driver': drv,
                            'RacePosition': drv_race.pick_fastest().get('Position')
                        })

            except Exception as e:
                print(f"Error processing {session['EventName']}: {e}")

    return pd.DataFrame(race_data)

if __name__ == "__main__":
    all_years_df = pd.DataFrame()
    for year in [2021, 2022, 2023]:
        df = fetch_race_data(year)
        all_years_df = pd.concat([all_years_df, df], ignore_index=True)

    all_years_df.to_csv(r'D:\DWDM\chat_predictor_f1\data\raw_data.csv', index=False)
    print(f"Combined dataset shape: {all_years_df.shape}")
