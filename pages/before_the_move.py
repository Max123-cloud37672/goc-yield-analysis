import streamlit as st
from src.data import load_yields, load_moves, TENORS
from src.analysis import align_moves, pre_move, event_path

st.title("Q1: Does the bond market see BoC moves coming?")
st.caption("If it does, yields should fall in the weeks before a cut and rise before a hike. "
           "The 2Y should react most, since it's closest to the policy rate.")


## Load data and set controls

yields_df = load_yields()
n = st.sidebar.slider("Lookback (trading days)", 5, 60, 20)
tenor = st.sidebar.selectbox("Tenor for the chart", TENORS)

moves = align_moves(load_moves(), yields_df.index, n)
pre = pre_move(yields_df, moves, TENORS, n)

st.subheader(f"Avg yield change in the {n} trading days before the move (bps)")
st.dataframe(pre.groupby('action')[['chg_bps'] + TENORS].mean().round(1))


path = event_path(yields_df, moves, tenor, before=n, after=0)
avg = path.T.groupby(moves.set_index('yield_day')['action']).mean().T
st.subheader(f"{tenor}: avg path into the decision (bps vs. day before)")
st.line_chart(avg)

with st.expander("Every move"):
    st.dataframe(pre.round(1))