# Machine Health Monitor

Edge monitoring for legacy industrial machines. Reads sensor data, detects faults,
and keeps working when the network is down.

## Problem
Legacy machines in factories and hospitals often have unreliable or no connectivity.
Faults go unnoticed until something breaks.

## Solution
- Monitors 3 sensors: temperature, vibration, pressure
- Detects anomalies using a rolling statistical check (z-score)
- Severity levels: WARNING and CRITICAL
- Stores all readings in a local SQLite database
- Offline mode: readings are buffered locally when the network is down
  and synced when it returns

## How to use the demo
1. Click **Collect new readings** to generate sensor data and see alerts.
2. Turn **Network online** off and collect again. The "Pending sync" counter rises.
3. Turn it back on and click **Sync buffered data to cloud**. Pending returns to 0.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Note
Sensor data and network outages are simulated for this demo (the "Network online"
toggle). The detection and buffering logic is designed to work with real sensor input.

## Tech
Python, Streamlit, SQLite, pandas
