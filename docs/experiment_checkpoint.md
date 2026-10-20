# TCP vs QUIC — Experiment Checkpoint

Date: October 20, 2026
Status: PAUSED

## Experiment Progress

Total planned: 270
Completed: 210 (77.8%)
Remaining: 60

## Completed RTT Configurations

10 ms:  0%, 1%, 3% loss
50 ms:  0%, 1%, 3% loss
100 ms: 0%, 1%, 3% loss
250 ms: 0%, 1%, 3% loss
500 ms: 0%, 1% loss

Each configuration includes:
- TCP CUBIC: 5 trials
- TCP Reno: 5 trials
- QUIC Reno: 5 trials

## Remaining Experiments

500 ms, 3% loss: 15 trials
1000 ms, 0% loss: 15 trials
1000 ms, 1% loss: 15 trials
1000 ms, 3% loss: 15 trials

## Next Experiment

TCP CUBIC
RTT: 500 ms
Packet loss: 3%
Trial: 1

## Resume Command

cd ~/QUIC-vs-TCP
sudo python3 -u experiments/run_batch.py --execute --limit 1

## Important

Do not reset results/results.csv.
The batch scheduler automatically skips completed trials.
Final analysis, figures, paper, and presentation remain pending.
