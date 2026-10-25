import streamlit as st
from src.data import load_yields, load_moves, TENORS
from src.analysis import align_moves, pre_move, day_of, phases

st.set_page_config(page_title="GoC Yields vs BoC Moves", layout="wide")
st.title("GoC Yields around Bank of Canada Rate Decisions")
st.write("How do Government of Canada bond yields behave before, on, and after Bank of Canada rate moves?")

##Load data for 3 questions

yields_df = load_yields()
all_moves = load_moves()
moves = align_moves(all_moves, yields_df.index)
pre = pre_move(yields_df, moves, TENORS)
d0 = day_of(yields_df, moves, TENORS)
phase = phases(all_moves, yields_df.index)
monthly = (yields_df[TENORS].diff() * 100).groupby(phase).mean() * 21

c1, c2, c3, c4 = st.columns(4)
c1.metric("Period", f"{yields_df.index[0]:%Y}–{yields_df.index[-1]:%Y}")
c2.metric("Trading days", f"{len(yields_df):,}")
c3.metric("Cuts", int((moves['action'] == 'Cut').sum()))
c4.metric("Hikes", int((moves['action'] == 'Raise').sum()))
st.line_chart(yields_df[TENORS])

##Question 1

st.header("1. Does the bond market see moves coming?")
before = pre.groupby('action')['2Y'].mean()
march_2020 = (pre.index.year == 2020) & (pre.index.month == 3)
cut_ex_2020 = pre.loc[(pre['action'] == 'Cut') & ~march_2020, '2Y'].mean()
st.markdown(f"""
**Yes for cuts, partly for hikes.** In the 20 trading days before a cut, the 2Y moved
{before['Cut']:+.1f} bps on average. Before a hike it moved {before['Raise']:+.1f} bps.

The March 2020 COVID cuts drive a lot of the cut result. Without them, the 2Y moved {cut_ex_2020:+.1f} bps.
""")
st.dataframe(pre.groupby('action')[TENORS].mean().round(1))

##Question 2
st.header("2. How do yields react on decision day?")
day = d0.groupby('action')['2Y'].mean()
st.markdown(f"""
**Not much, so most moves were already priced in.** On decision day the 2Y moved
{day['Cut']:+.1f} bps on cuts and {day['Raise']:+.1f} bps on hikes. The big reactions were surprises:
""")
biggest = d0.loc[d0['2Y'].abs().sort_values(ascending=False).index[:3], ['action', 'chg_bps', '2Y']]
st.dataframe(biggest)

##Question 3
st.header("3. What do yields do across a cycle?")
st.markdown(f"""
**Yields follow the cycle, and the short end moves most.** In cutting phases the 2Y moves
{monthly.loc['Cutting', '2Y']:+.1f} bps a month and the 30Y {monthly.loc['Cutting', '30Y']:+.1f}.
In hiking phases the 2Y moves {monthly.loc['Hiking', '2Y']:+.1f} bps a month.
""")
st.dataframe(monthly.round(1))

st.header("What I did")
st.markdown("""
- **Yields:** daily GoC benchmark yields (2Y, 5Y, 10Y, 30Y) from the Bank of Canada
- **Rate moves:** BoC policy rate dated to the announcement day
- **Q1:** yield change over the 20 trading days ending the day before each move
- **Q2:** yield change on the decision day itself
- **Q3:** each day labelled Cutting or Hiking if the last move was within 180 days, otherwise Hold
- **Limits:** data starts April 2009, only 14 cuts and 18 hikes, and averages show patterns, not causes

Use the pages in the sidebar to change the settings and see every move.
""")