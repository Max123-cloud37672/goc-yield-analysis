import pandas as pd

def align_moves(moves, dates, n=20):
    m = moves[(moves.index > dates[n + 1]) & (moves.index <= dates[-1])].copy()
    m['yield_day'] = [dates[dates.searchsorted(d)] for d in m.index]
    return m

def pre_move(yields_df, moves, tenors, n=20):
    dates = yields_df.index
    out = moves[['chg_bps', 'action']].copy()
    for t in tenors:
        out[t] = [(yields_df[t].iloc[j - 1] - yields_df[t].iloc[j - 1 - n]) * 100
                  for j in dates.get_indexer(moves['yield_day'])]
    return out

def event_path(yields_df, moves, tenor, before=20, after=20):
    s = yields_df[tenor]
    paths = {}
    for day, j in zip(moves['yield_day'], s.index.get_indexer(moves['yield_day'])):
        if j - before < 0 or j + after >= len(s):
            continue
        window = s.iloc[j - before:j + after + 1].values
        paths[day] = (window - s.iloc[j - 1]) * 100
    return pd.DataFrame(paths, index=range(-before, after + 1))


##Question 2:

def day_of(yields_df, moves, tenors):
    daily = yields_df[tenors].diff() * 100
    out = moves[['chg_bps', 'action']].copy()
    for t in tenors:
        out[t] = daily[t].loc[moves['yield_day']].values
    return out


##Question 3:
def phases(moves, dates, window=180):
    last_action = moves['action'].reindex(dates, method='ffill')
    last_move_day = pd.Series(moves.index, index=moves.index).reindex(dates, method='ffill')
    days_since = (dates.to_series() - last_move_day).dt.days

    phase = last_action.where(days_since <= window, 'Hold').fillna('Hold')
    return phase.replace({'Cut': 'Cutting', 'Raise': 'Hiking'}).rename('phase')