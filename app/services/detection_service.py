import pandas as pd

def detect_equipment_events(df: pd.DataFrame) -> pd.DataFrame:
    # Sort values by equipment_name and timestamp
    df = df.sort_values(by=['equipment_name', 'timestamp']).reset_index(drop=True)
    df['stop_time'] = pd.NaT
    df['restart_time'] = pd.NaT

    for i in range(1, len(df)):
        # Check if the current and previous rows belong to the same equipment
        if df.loc[i, 'equipment_name'] == df.loc[i - 1, 'equipment_name']:
            # Equipment stop condition
            if (df.loc[i, 'pressure_1'] > df.loc[i - 1, 'pressure_1'] + 5 and
                df.loc[i, 'pressure_2'] == df.loc[i - 1, 'pressure_2'] and
                df.loc[i, 'temperature'] < df.loc[i - 1, 'temperature']):
                df.loc[i, 'stop_time'] = df.loc[i, 'timestamp']

            # Equipment restart condition
            if (df.loc[i, 'pressure_1'] < df.loc[i - 1, 'pressure_1'] and
                df.loc[i, 'temperature'] > df.loc[i - 1, 'temperature'] + 2):
                df.loc[i, 'restart_time'] = df.loc[i, 'timestamp']

    # Filter the columns we want in the result
    result = df[['equipment_name', 'stop_time', 'restart_time']]

    # Return rows where either stop_time or restart_time is not NaN
    return result.dropna(how='all', subset=['stop_time', 'restart_time'])
