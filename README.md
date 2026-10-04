# machine-health-monitor
Offline-first machine health monitoring system that simulates sensor data, detects abnormal temperature patterns, and provides real-time alerts through a Streamlit dashboard.

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

## Run it
pip install streamlit pandas
streamlit run app.py


## Note
Sensor data is simulated for this demo. The detection and buffering logic
is designed to work with real sensor input.

## Tech
Python, Streamlit, SQLite, pandas,
