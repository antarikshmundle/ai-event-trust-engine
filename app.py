import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Event Trust Engine", layout="centered")

# ---------- HEADER ----------
st.title("AI-based Event Trust Engine")
st.subheader("Detecting fake and spam events in crowdsourced platforms")

st.markdown("""
This dashboard analyzes **crowdsourced event data** and assigns a **Trust Score**
based on behavioral patterns such as description quality, organizer activity,
and suspicious keywords.
""")

st.markdown("---")

# ---------- LOAD DATA ----------
df = pd.read_csv("events.csv")

df["posted_events_count"] = pd.to_numeric(
    df["posted_events_count"], errors="coerce"
).fillna(0)

st.markdown("### Uploaded Event Data")
st.dataframe(df)

# ---------- AI LOGIC ----------
def calculate_trust_score(row):
    score = 100

    if len(row["description"].split()) < 6:
        score -= 30

    if row["posted_events_count"] > 10:
        score -= 40

    spam_words = ["free", "win", "giveaway", "click"]
    for word in spam_words:
        if word in row["description"].lower():
            score -= 20
            break

    return max(score, 0)

# ---------- RUN ANALYSIS ----------
if st.button("Run AI Trust Analysis"):
    df["Trust Score"] = df.apply(calculate_trust_score, axis=1)

    def label(score):
        if score >= 70:
            return "Trusted"
        elif score >= 40:
            return "Suspicious"
        else:
            return "High Risk"

    df["Status"] = df["Trust Score"].apply(label)

    # ---------- SUMMARY ----------
    risky_count = len(df[df["Status"] != "Trusted"])
    total = len(df)

    st.success(
        f"Analysis complete: {risky_count} out of {total} events "
        f"are flagged as suspicious or high risk."
    )

    # ---------- LEGEND ----------
    st.markdown("""
**Legend:**  
🟢 **Trusted Event**  
🟡 **Suspicious Event**  
🔴 **High Risk / Spam Event**
""")

    # ---------- COLOR CODING ----------
    def highlight_status(row):
        if row["Status"] == "Trusted":
            return ["background-color: #c6f6d5"] * len(row)
        elif row["Status"] == "Suspicious":
            return ["background-color: #fefcbf"] * len(row)
        else:
            return ["background-color: #fed7d7"] * len(row)

    st.markdown("### AI Analysis Result")
    st.dataframe(df.style.apply(highlight_status, axis=1))
