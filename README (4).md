# Fleet Attention Ranker

A small project that ranks fleet vehicles by what needs a manager's attention first, with a plain-English reason and a suggested next action.

**All data is simulated.** No real vehicles, customers or Motorq data are used. This is an independent learning project inspired by public information about connected-vehicle products.

## Problem
Fleet managers see long lists of vehicles and alerts. The useful question is "what should I deal with first, and why?"

## How it works
1. `make_data.py` creates `fleet_data.csv` (40 simulated vehicles with 7 signals: overdue return days, hours since last signal, fuel drop with no trip, warning codes, days since service, idle hours).
2. `rank_fleet.py` scores each vehicle with transparent rules, labels it Critical / High / Watch, and writes the top reasons and a next action to `ranked_output.csv`.
3. Optional: `python rank_fleet.py --llm` asks an LLM (Claude API, needs `ANTHROPIC_API_KEY`) to rewrite each reason as one plain sentence for a manager.

## Run it
```
python make_data.py
python rank_fleet.py
```

## Result
9 of 40 vehicles need attention. V004 ranks first (5 days overdue and no signal for 52 hours). See `fleet-attention-ranker-case-study.pdf` for the full write-up.

## Limitations
- Weights are hand-set, not learned from real outcomes.
- Data is simulated, so results show the method, not real-world accuracy.
- The first version under-ranked a 22% fuel drop; I raised its weight. Weights need validation with real fleet operators.

## Next steps
Interview fleet operators about what they check first, replace guessed weights with their priorities, and measure whether the ranking saves time.
