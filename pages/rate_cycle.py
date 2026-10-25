import pandas as pd
import streamlit as st
from src.data import load_yields, load_moves, TENORS
from src.analysis import phases

st.title("Q3: What do yields do across a whole cycle?")
st.caption("Every day is labelled by the BoC's current phase: Cutting or Hiking if the last move "
           "was within the window, Hold if there's been no move for longer.")

## Load data and set controls

yields_df = load_yields()
window = st.sidebar.slider("Phase window (calendar days)", 60, 365, 180)

phase = phases(load_moves(), yields_df.index, window)
daily = yields_df[TENORS].diff() * 100


c1, c2 = st.columns(2)
c1.subheader("Avg yield level (%)")
c1.dataframe(yields_df[TENORS].groupby(phase).mean().round(2))
c2.subheader("Avg change per month (bps)")
c2.dataframe((daily.groupby(phase).mean() * 21).round(1))

st.subheader("2Y yield, coloured by phase")
st.scatter_chart(pd.DataFrame({'2Y': yields_df['2Y'], 'phase': phase}).reset_index(),
                 x='date', y='2Y', color='phase')

st.caption("Trading days in each phase: " +
           ", ".join(f"{k} {v}" for k, v in phase.value_counts().items()))