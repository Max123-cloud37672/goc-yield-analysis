import pandas as pd
from boc_decisions import moves

## GoC benchmark yields, short names, date as index
yields_df = pd.read_csv('data/bond_yields_all.csv')[['date','BD.CDN.2YR.DQ.YLD','BD.CDN.3YR.DQ.YLD','BD.CDN.5YR.DQ.YLD','BD.CDN.7YR.DQ.YLD','BD.CDN.10YR.DQ.YLD','BD.CDN.LONG.DQ.YLD']].rename({'BD.CDN.2YR.DQ.YLD':'2Y','BD.CDN.3YR.DQ.YLD':'3Y','BD.CDN.5YR.DQ.YLD':'5Y','BD.CDN.7YR.DQ.YLD':'7Y','BD.CDN.10YR.DQ.YLD':'10Y','BD.CDN.LONG.DQ.YLD':'30Y'},axis=1)
yields_df['date'] = pd.to_datetime(yields_df['date'])
yields_df = yields_df.set_index('date').sort_index()
dates = yields_df.index
tenors = ['2Y', '5Y', '10Y', '30Y']

## Daily change in each yield, in bps (yields are in %, so x100) + 20d changes
daily = yields_df[tenors].diff() * 100
moves = moves[(moves.index > dates[21]) & (moves.index <= dates[-1])].copy()
moves['yield_day'] = [dates[dates.searchsorted(d)] for d in moves.index]


## Question 1: Does the bond market see BoC moves coming?
## Yields trade on where the market thinks the policy rate is going.
## If the market sees it coming: yields fall in the weeks BEFORE a cut, rise BEFORE a hike.
## The 2Y should react most, since it's closest to the policy rate.

def pre_move(day, t, n=20):
    j = dates.get_loc(day)
    return (yields_df[t].iloc[j-1] - yields_df[t].iloc[j-1-n]) * 100

for t in tenors:
    moves[f'{t}_20d_before'] = moves['yield_day'].apply(pre_move, t=t)

print("Q1: Avg yield change in the 20 trading days BEFORE the move (bps)")
print(moves.groupby('action')[['chg_bps'] + [f'{t}_20d_before' for t in tenors]].mean().round(1))


## Question 2: How do yields react ON decision day?
## If the move was already priced in (Q1), the day-of reaction should be small.

for t in tenors:
    moves[f'{t}_day_of'] = daily[t].loc[moves['yield_day']].values

print("\nQ2: Avg yield change ON decision day (bps)")
print(moves.groupby('action')[[f'{t}_day_of' for t in tenors]].mean().round(1))


## Question 3: What do yields do across a whole cycle?
## Label every day by the BoC's last move:
##   'Cutting' or 'Hiking' = last move was a cut/hike within the past 6 months
##   'Hold'                = no move for 6+ months
## Then see the average yield level and monthly change in each regime.

last_action = moves['action'].reindex(dates, method='ffill')
last_move_day = pd.Series(moves.index, index=moves.index).reindex(dates, method='ffill')
days_since = (dates.to_series() - last_move_day).dt.days

regime = last_action.where(days_since <= 180, 'Hold').fillna('Hold')
regime = regime.replace({'Cut': 'Cutting', 'Raise': 'Hiking'})

print("\nQ3a: Avg yield level by regime (%)")
print(yields_df[tenors].groupby(regime).mean().round(2))

print("\nQ3b: Avg yield change per month by regime (bps)")
print((daily.groupby(regime).mean() * 21).round(1))

print("\nTrading days in each regime:")
print(regime.value_counts())
