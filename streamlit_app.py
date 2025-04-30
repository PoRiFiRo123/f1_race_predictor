import streamlit as st
from app.predictor import predict_winner
from app.driver_performance import get_driver_last_3_races
from app.circuit_statistics import get_circuit_statistics
from app.model_dashboard import model_dashboard
from app.driver_gif_map import DRIVER_GIF_MAP

st.set_page_config(page_title="F1 Race Predictor", layout="wide")
st.title('🏎️ F1 Race Winner Predictor')

# Page Selector
page = st.sidebar.selectbox("Select Page", [
    "Predictor", 
    "Driver Performance", 
    "Circuit Statistics", 
    "Model Dashboard"
])

# -----------------------------
# 🏁 Helper Function: GIF logic
# -----------------------------
def get_driver_gif(driver, position):
    driver = driver.upper()
    if driver not in DRIVER_GIF_MAP:
        return None
    if position == 1:
        return DRIVER_GIF_MAP[driver]['win']
    elif 2 <= position <= 10:
        return DRIVER_GIF_MAP[driver]['mid']
    else:
        return DRIVER_GIF_MAP[driver]['low']

# -----------------------------
# 1️⃣ Predictor Page
# -----------------------------
if page == "Predictor":
    circuit = st.selectbox('Circuit Name', [
        'Abu Dhabi Grand Prix', 'Australian Grand Prix', 'Bahrain Grand Prix',
        'British Grand Prix', 'Canadian Grand Prix', 'Dutch Grand Prix',
        'Hungarian Grand Prix', 'Italian Grand Prix', 'Japanese Grand Prix',
        'Las Vegas Grand Prix', 'Mexico City Grand Prix', 'Miami Grand Prix',
        'Monaco Grand Prix', 'Saudi Arabian Grand Prix', 'Singapore Grand Prix',
        'Spanish Grand Prix'
    ])
    year = st.number_input('Year', min_value=2000, max_value=2025, step=1, value=2025)
    driver = st.text_input('Driver Abbreviation (e.g., VER, HAM)')

    if st.button('Predict Winner'):
        result = predict_winner(year, circuit, driver)
        st.subheader(result)

        # Extract predicted position from result string
        if "Position:" in result:
            try:
                position = int(result.split(":")[-1].strip())
                gif_url = get_driver_gif(driver, position)
                if gif_url:
                    st.image(gif_url, use_container_width=True)
                else:
                    st.warning("No GIF available for this driver.")
            except:
                st.warning("Couldn't parse finishing position.")

# -----------------------------
# 2️⃣ Driver Performance Page
# -----------------------------
elif page == "Driver Performance":
    driver = st.text_input('Driver Abbreviation (e.g., VER, HAM)')
    year = st.number_input('Current Year', min_value=2000, max_value=2025, step=1, value=2025)

    if st.button('Show Performance'):
        df = get_driver_last_3_races(driver, year)
        if not df.empty:
            st.write(f"📊 Last 3 Races for `{driver}`:")
            st.dataframe(df)
        else:
            st.error("No data available for that driver/year.")

# -----------------------------
# 3️⃣ Circuit Statistics Page
# -----------------------------
elif page == "Circuit Statistics":
    circuit = st.selectbox('Circuit Name', [
        'Abu Dhabi Grand Prix', 'Australian Grand Prix', 'Bahrain Grand Prix',
        'British Grand Prix', 'Canadian Grand Prix', 'Dutch Grand Prix',
        'Hungarian Grand Prix', 'Italian Grand Prix', 'Japanese Grand Prix',
        'Las Vegas Grand Prix', 'Mexico City Grand Prix', 'Miami Grand Prix',
        'Monaco Grand Prix', 'Saudi Arabian Grand Prix', 'Singapore Grand Prix',
        'Spanish Grand Prix'
    ])
    year = st.number_input('Current Year', min_value=2000, max_value=2025, step=1, value=2025)

    if st.button('Show Statistics'):
        stats = get_circuit_statistics(circuit, year)
        if not stats.empty:
            st.write(f"🏆 Win Statistics for **{circuit}**:")
            st.dataframe(stats)
        else:
            st.warning("No race data available for this circuit.")

# -----------------------------
# 4️⃣ Model Dashboard Page
# -----------------------------
elif page == "Model Dashboard":
    model_dashboard()
