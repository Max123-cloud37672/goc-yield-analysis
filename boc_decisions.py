import json, urllib.request
import pandas as pd

## BoC policy rate (target for the overnight rate), daily since 2001
url = "https://www.bankofcanada.ca/valet/observations/V39079/json?start_date=2001-01-01"
data = json.load(urllib.request.urlopen(url))

policy_df = pd.DataFrame([{'date': o['d'], 'rate': float(o['V39079']['v'])}
                          for o in data['observations'] if o.get('V39079')])
policy_df['date'] = pd.to_datetime(policy_df['date'])
policy_df = policy_df.set_index('date').sort_index()

## Decisions = days the rate changed (in bps)
policy_df['chg_bps'] = policy_df['rate'].diff() * 100
moves = policy_df[policy_df['chg_bps'] != 0].dropna().copy()
moves['action'] = moves['chg_bps'].apply(lambda x: 'Raise' if x > 0 else 'Cut')

## Only print when this file is run directly (not when another file imports `moves` from it)
if __name__ == '__main__':
    print(moves)
    print(moves['action'].value_counts())
