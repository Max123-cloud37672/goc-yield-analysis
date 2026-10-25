import json, urllib.request
import pandas as pd
import streamlit as st

TENORS = ['2Y', '5Y', '10Y', '30Y']
COLS = {'BD.CDN.2YR.DQ.YLD': '2Y', 'BD.CDN.3YR.DQ.YLD': '3Y', 'BD.CDN.5YR.DQ.YLD': '5Y',
        'BD.CDN.7YR.DQ.YLD': '7Y', 'BD.CDN.10YR.DQ.YLD': '10Y', 'BD.CDN.LONG.DQ.YLD': '30Y'}



## cache is so streamlit doesn't reload the data every time the page is refreshed
@st.cache_data
def load_yields():
    df = pd.read_csv('data/bond_yields_all.csv', encoding='utf-8-sig', usecols=['date', *COLS])
    df = df.rename(columns=COLS)
    df['date'] = pd.to_datetime(df['date'])
    return df.set_index('date').sort_index().loc['2009-04-21':]

@st.cache_data(ttl=86400)
def load_moves():
    url = "https://www.bankofcanada.ca/valet/observations/V39079/json?start_date=2001-01-01"
    data = json.load(urllib.request.urlopen(url))

    policy = pd.DataFrame([{'date': o['d'], 'rate': float(o['V39079']['v'])}
                           for o in data['observations'] if o.get('V39079')])
    policy['date'] = pd.to_datetime(policy['date'])
    policy = policy.set_index('date').sort_index()

    policy['chg_bps'] = policy['rate'].diff() * 100
    moves = policy[policy['chg_bps'] != 0].dropna().copy()
    moves['action'] = moves['chg_bps'].apply(lambda x: 'Raise' if x > 0 else 'Cut')
    moves.index = pd.DatetimeIndex(
        [d - pd.Timedelta(days=1) if d.dayofweek == 3 else d for d in moves.index], name='date')
    return moves