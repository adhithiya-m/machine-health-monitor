import random
import sqlite3
import pandas as pd
import streamlit as st

SENSORS = {
    "temperature (°C)": (70, 2),
    "vibration (mm/s)": (5, 0.5),
    "pressure (kPa)": (100, 3),
}
DB = "readings.db"


def db():
    con = sqlite3.connect(DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS readings "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, sensor TEXT, value REAL, synced INTEGER)"
    )
    return con


def simulate(n):
    rows = []
    for _ in range(n):
        for name, (mu, sd) in SENSORS.items():
            v = random.gauss(mu, sd)
            if random.random() < 0.03:  # random fault
                v += random.choice([-1, 1]) * sd * random.choice([4, 7])
            rows.append((name, v))
    return rows


st.title("Machine Health Monitor")
st.caption("Edge monitoring for legacy machines: works offline, buffers data, alerts on faults")

online = st.toggle("Network online", value=True)
n = st.slider("Readings per sensor", 50, 300, 100)

con = db()
col_a, col_b = st.columns(2)
if col_a.button("Collect new readings"):
    con.executemany(
        "INSERT INTO readings (sensor, value, synced) VALUES (?,?,?)",
        [(s, v, 1 if online else 0) for s, v in simulate(n)],
    )
    con.commit()
if col_b.button("Reset all data"):
    con.execute("DELETE FROM readings")
    con.commit()

df = pd.read_sql("SELECT * FROM readings", con)
if df.empty:
    st.info("No data yet. Click 'Collect new readings'.")
    st.stop()

pending = int((df["synced"] == 0).sum())
m1, m2 = st.columns(2)
m1.metric("Total readings", len(df))
m2.metric("Pending sync (offline buffer)", pending)

if pending and online:
    if st.button("Sync buffered data to cloud"):
        con.execute("UPDATE readings SET synced=1 WHERE synced=0")
        con.commit()
        st.rerun()
elif pending:
    st.warning("Network is down. Readings are safely stored locally and will sync later.")

alerts = []
tabs = st.tabs(list(SENSORS))
for tab, name in zip(tabs, SENSORS):
    g = df[df["sensor"] == name].reset_index(drop=True)
    avg = g["value"].rolling(20, min_periods=5).mean().shift(1)
    std = g["value"].rolling(20, min_periods=5).std().shift(1)
    g["z"] = (g["value"] - avg).abs() / std
    with tab:
        st.line_chart(g["value"])
    for i, row in g[g["z"] > 3].iterrows():
        level = "CRITICAL" if row["z"] > 5 else "WARNING"
        alerts.append((level, name, i, row["value"]))

st.subheader(f"Alerts: {len(alerts)}")
for level, name, i, value in alerts:
    msg = f"{level}: {name} reading #{i} = {value:.1f} is abnormal. Inspect the machine."
    st.error(msg) if level == "CRITICAL" else st.warning(msg)
