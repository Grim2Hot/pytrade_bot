# Broker Class Bot

## What does it do?
- Fetches data on the given stock
- Runs analysis on the data using Strategy objects
- Strategy objects return Confidence Index Value
- Confidence Index Value returned from Strategy object should be all it receives?
    - For clarity, the CIV might be obtained from numerous other Strategy objects from within another Strategy object
    - Weighting might be applied to each returned sub CIV depending on 'trust' of that Strategy
    - Once all CIV's are returned and weighted, mean(?) is taken and returned by (or stored in) the object
- Once a CIV is received to the broker:
    - Compare against risk appetite
    - Compare against portfolio/positions
    - Generate recommended investment position depending on available funds and confidence level?
- Commit trade action indicated by CIV using Broker class