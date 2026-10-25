import streamlit as st
from src.data import load_yields, load_moves, TENORS
from src.analysis import align_moves, day_of, event_path

st.title("Q2: How do yields react on decision day?")
st.caption("If the move was already priced in (Q1), the day-of reaction should be small.")

##Load data and set controls

yields_df = load_yields()
tenor = st.sidebar.selectbox("Tenor for the chart", TENORS)
after = st.sidebar.slider("Days after the decision", 1, 20, 5)

moves = align_moves(load_moves(), yields_df.index)
d0 = day_of(yields_df, moves, TENORS)

st.subheader("Avg yield change on decision day (bps)")
st.dataframe(d0.groupby('action')[TENORS].mean().round(1))

## Does a bigger move get a bigger reaction? (25 vs 50+ bps)
d0['size'] = d0['chg_bps'].abs().astype(int).astype(str) + ' bps'
st.subheader("By size of move")
by_size = d0.groupby(['action', 'size'])[TENORS].mean().round(1)
by_size['count'] = d0.groupby(['action', 'size']).size()
st.dataframe(by_size)

## What happens in the days after?
path = event_path(yields_df, moves, tenor, before=1, after=after)
avg = path.T.groupby(moves.set_index('yield_day')['action']).mean().T
st.subheader(f"{tenor}: avg path after the decision (bps vs. day before)")
st.line_chart(avg)

with st.expander("Every move"):
    st.dataframe(d0.round(1))

st.caption("Note: the Mar 13, 2020 emergency cut was announced after markets closed, "
           "so it shows here as Mar 16, the first day the market could react.")