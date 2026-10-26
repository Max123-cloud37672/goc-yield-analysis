# GoC Yields around Bank of Canada Rate Decisions

This is a streamlit app that tests whether the Government of Canada benchmark bonds react to Bank of Canada rate changes in the coming weeks before the initial announcment, not on the day of. Having followed equities and crypto, I'd often watch a rate decision barely move prices because the market had already priced in the change weeks before the announcement, and I wanted to see from a statistical perspective how true that was in bonds.

## Questions

1. **Before the move:** Does the bond market see BoC moves coming? I expected to see that yields would move 20 days or less before a cut, hold, or hike. If they did it means that the market did see it coming and most priced it accurately. 
2. **Decision day:** How do yields react on decision day? A small jump means it was already priced in. A big jump means it was a suprise. 
3. **Rate cycles:** What do yields do across a whole cycle? Yields are constantly changing, drifiting down in a cutting cycle and up during a hiking cycle, with the 2Y tener moving the most, and the 30y moving the least.

## Data

- **Yields:** Daily Government of Canada benchmark bond yields (2Y,5Y,10Y,30Y) from the Bank of Canada.
- **Policy rate:** The Bank of Canada's key interest rate from April 2009 onward, downloaded from the BoC website.
- **Period:** April 2009 to October 2026, because the rate data starts in 2009 and the yields file ends in October 2026.

**How I found the data:** I searched up fixed income in Canada and stumbled onto the Bank of Canada's website, which has accessible data on government bond yields going back years. While I was there, I found it also lets you download its interest rate history, so then I was able to take both sources and implement it into this project. 

## How I got here

1. **Starting point:** I started with two Python scripts. The first, 'boc_decisions.py', downladed the Bank of Canada's interest rate history and picked out every day the bank changed its rate. The second, 'reading_yields.py', uploaded the bond yields and compared them to those rate changes. My hypothesis was that the bond market sees rate moves coming, therefore, in the coming weeks before a cut or hike, there should not be a large change in interest rates on the day of. After that, I then printed tables in the terminal. 
2. **Splitting into three questions:** One question I knew was not gonna be sufficient to test the idea properly, so I broke it into three. First, do yields move in the weeks before a decision? That's the main test of whether the market sees it coming. Second, how much do yields move on the day itself? If the market alreay saw it coming, the reaction should be small, so this checks the first answer from another angle. Third, what do yields do over a whole cutting, holding, or hiking cycle? That shows the much bigger picture of what is going on yearly beyond the individual decisions happening many times a year. 

3. **First problem:** When I made the chart of the 2Y yield coloured by cutting, hiking and hold, everything from 2001-2009 showed up as Hold. That was wrong, because the BoC cut and raised rates many times in those years. Looking into it, I found the rate data I was downloading only starts in April 2009, so the app had no rate decisions before then and labelled everyday as a Hold. I fixed it by starting all the data in April 2009, so every day has both a yield and the right label. 
4. **Second problem:** The recent decisions were all dated on Thursdays, but from what I learned the Bank of Canada usually announces on Wednesday. When I printed the weekdays, every move from 2022 on was a day late, so my "decision day" numbers were really measuring the day after. I shifted those dates back a day, and the big surpise move, like October 2022, finally ended up working out. 
5. **Checking the proof:** The averages show that yields fall before cuts, but not why. They might fall because traders see the cut coming, or economic news that came out pushes yields down, or for various other reasons. 
6. **Keeping it simple:** I learned about spreads, but they pulled me away from the main question, so I decided to leave those more advanced tests on the backburner, as this was a project for me to really understand the basics. This project was really about answering the three questions clearly, and then moving from here. 
## Why Streamlit

My first scripts just printed tables, and every time I wanted to try a different setting, like looking 10 days back instead of 20, I had to change the code and run it again. With Streamlit it was much simpler, I could put those settings on sliders and see the results change right away. It also let me give each question its own page, so it shows the evolution of my thought process i.e., how did I from Q1->Q2. 

## Code structure

```
app.py                  home page with the answers to all three questions
pages/
  before_the_move.py    Q1: do yields move before a decision? 
  decision_day.py       Q2: how much do they move on the day?
  rate_cycle.py         Q3: what do they do over a whole cycle?
src/
  data.py               loads the yields file and the Bank of Canada rate decisions. 
  analysis.py           the calcuations for each question.
data/
  bond_yields_all.csv   daily Government of Canada bond yields. 
```

**Why it's split this way:** Every page uses the same data and the same calculations, so I kept them in one place. When I found the date bug, I fixed it once in 'data.py' and every page was fixed. 

## How I tested it

- Before touching Streamlit, I ran 'data.py' straight from the terminal to make sure the yields and rate decisions loaded properly. 
- I tested the 'analysis.py' functions the same way and checked the numbers looked right.
- I only built the pages once those worked. 
- I printed the weekday of every decision, which is how I caught the real date bug. 
- I checked that the biggest decision-day moves were real suprises, like January 2015, October 2022 and June 2023. 

## How to run

```
pip install -r requirements.txt
streamlit run app.py
```

## Findings

**1. Before the move:** Yields usually fall before a cut. In the 20 trading days before one, the 2Y dropped 25.5 bps on average. Before a hike it rose 10 bps. The March 2020 COVID cuts drive a lot of this, though without them, the drop before cuts is 13.1 bps. 

**2. Decision day:** Not much happens on the day itself. The 2Y moved -4.9 bps on cuts and +2.2 bps on hikes, which suggests most moves were already priced in. The big reactions were suprises, like the unexpected cut in January 2015 (-29bps) and October 2022, when the Bank hiked less than expected and the 2Y fell 28 bps. 

**3. Rate cycles:** Yields follow the cycle, and the 2Y moves most. During cutting phases it fails about 5.8 bp a month, and during a hiking phases it rises about 6.2 bps a month. 

## Limits

- Only 14 cuts and 18 hikes since 2009, so a few big moves can swing the averages. 
- The averages show patterns, not the actual causes themselves. Yields could fall before a cut because of the same bad news that makes the Bank cut. 
- The data only goes back to April 2009. 

## What I'd do next

- Compare the moes before decisions to normal weeks in the same cycle, to test whether they're actually unsual. 
- Add the 2001 to 2009 decisions by hand so the data goes further back.
- Add a button to leaven out the March 2020 cuts. 
ss