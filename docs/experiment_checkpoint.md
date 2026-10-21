# TCP vs QUIC — Experiment Checkpoint

Date: October 21, 2026
Status: EXPERIMENTS COMPLETE

## Experiment Progress

Total planned: 270
Completed: 270 (100%)
Remaining: 0

## Completed RTT Configurations

All three packet-loss levels (0%, 1%, 3%) were completed for:

- 10 ms
- 50 ms
- 100 ms
- 250 ms
- 500 ms
- 1000 ms

Each RTT and packet-loss combination includes:

- TCP CUBIC: 5 trials
- TCP Reno: 5 trials
- QUIC Reno: 5 trials

Total: 3 configurations x 6 RTT levels x 3 loss levels x 5 trials = 270.

## Experimental Results

- Dataset: `results/results.csv`
- Statistical analysis: `analysis/analyze_results.py`
- Throughput figures: `analysis/plot_results.py`
- Connection-time figures: `analysis/plot_connection_time.py`
- Methodology: `docs/experimental_design.md`

The complete dataset, analysis scripts, and generated figures
have been committed and pushed to GitHub.

## Remaining Deliverables

- Interpret the experimental findings and limitations.
- Prepare the final research report.
- Prepare the final presentation.

## Important

The experimental matrix is complete. No additional trials
are currently required.

Preserve `results/results.csv` as the completed dataset.

The previous checkpoint, recorded on October 20, 2026,
documented a paused experiment at 210/270 trials.
A local backup preserves that historical checkpoint.
