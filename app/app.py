import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Project paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_rul, feature_columns


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Turbofan RUL Predictor",
    page_icon="✈️",
    layout="wide"
)


# --------------------------------------------------
# Dataset column names
# --------------------------------------------------
column_names = (
    ["unit_id", "cycle"]
    + ["setting_1", "setting_2", "setting_3"]
    + [f"sensor_{i}" for i in range(1, 22)]
)


# --------------------------------------------------
# Load FD001 test data
# --------------------------------------------------
@st.cache_data
def load_test_data():
    test_path = PROJECT_ROOT / "data" / "raw" / "test_FD001.txt"
    rul_path = PROJECT_ROOT / "data" / "raw" / "RUL_FD001.txt"

    test_df = pd.read_csv(
        test_path,
        sep=r"\s+",
        header=None
    )

    test_df.columns = column_names

    true_rul_df = pd.read_csv(
        rul_path,
        sep=r"\s+",
        header=None
    )

    true_rul_df.columns = ["true_RUL"]

    return test_df, true_rul_df


test_df, true_rul_df = load_test_data()


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("✈️ Turbofan Engine RUL Prediction")

st.write(
    "Machine learning dashboard for predicting the Remaining Useful "
    "Life (RUL) of turbofan engines using operational settings and "
    "sensor measurements."
)

st.caption(
    "Dataset: NASA C-MAPSS FD001 | Model: Random Forest Regression"
)

st.divider()


# --------------------------------------------------
# Input mode
# --------------------------------------------------
st.subheader("Prediction Mode")

prediction_mode = st.radio(
    "Choose how you want to provide engine measurements:",
    [
        "Load Sample Test Engine",
        "Manual Input"
    ],
    horizontal=True
)

st.divider()


# --------------------------------------------------
# Default manual values
# --------------------------------------------------
default_values = {
    "setting_1": 0.0,
    "setting_2": 0.0,
    "setting_3": 100.0,
    "sensor_2": 642.5,
    "sensor_3": 1585.0,
    "sensor_4": 1405.0,
    "sensor_6": 21.61,
    "sensor_7": 553.5,
    "sensor_8": 2388.0,
    "sensor_9": 9050.0,
    "sensor_11": 47.5,
    "sensor_12": 521.5,
    "sensor_13": 2388.0,
    "sensor_14": 8130.0,
    "sensor_15": 8.4,
    "sensor_17": 392.0,
    "sensor_20": 39.0,
    "sensor_21": 23.4
}


# --------------------------------------------------
# Shared variables
# --------------------------------------------------
input_data = {}
actual_rul = None
selected_engine_data = None
selected_engine = None


# --------------------------------------------------
# Sample engine mode
# --------------------------------------------------
if prediction_mode == "Load Sample Test Engine":

    st.subheader("🧪 Select FD001 Test Engine")

    engine_ids = sorted(
        test_df["unit_id"].unique()
    )

    selected_engine = st.selectbox(
        "Select Engine ID",
        engine_ids
    )

    selected_engine_data = test_df[
        test_df["unit_id"] == selected_engine
    ].copy()

    latest_engine_row = (
        selected_engine_data
        .sort_values("cycle")
        .tail(1)
        .iloc[0]
    )

    actual_rul = float(
        true_rul_df.iloc[
            int(selected_engine) - 1
        ]["true_RUL"]
    )

    # Engine summary cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Engine ID",
            int(selected_engine)
        )

    with col2:
        st.metric(
            "Last Observed Cycle",
            int(latest_engine_row["cycle"])
        )

    with col3:
        st.metric(
            "Historical Cycles",
            len(selected_engine_data)
        )

    st.divider()

    st.subheader("📊 Latest Engine Measurements")

    st.caption(
        "Measurements are loaded from the final observed cycle "
        "of the selected FD001 test engine."
    )

    cols = st.columns(3)

    for i, feature in enumerate(feature_columns):

        with cols[i % 3]:

            input_data[feature] = st.number_input(
                label=feature.replace("_", " ").title(),
                value=float(latest_engine_row[feature]),
                format="%.4f",
                key=f"sample_{selected_engine}_{feature}"
            )


# --------------------------------------------------
# Manual input mode
# --------------------------------------------------
else:

    st.subheader("⌨️ Manual Engine Measurements")

    st.caption(
        "Enter operational settings and sensor measurements manually."
    )

    cols = st.columns(3)

    for i, feature in enumerate(feature_columns):

        with cols[i % 3]:

            input_data[feature] = st.number_input(
                label=feature.replace("_", " ").title(),
                value=float(
                    default_values.get(feature, 0.0)
                ),
                format="%.4f",
                key=f"manual_{feature}"
            )


st.divider()


# --------------------------------------------------
# Prediction button
# --------------------------------------------------
if st.button(
    "🔍 Predict Remaining Useful Life",
    type="primary",
    use_container_width=True
):

    try:
        # Prepare input
        input_df = pd.DataFrame([input_data])

        # Exact model feature order
        input_df = input_df[feature_columns]

        # Prediction
        prediction = predict_rul(input_df)[0]

        prediction = max(
            0.0,
            float(prediction)
        )

        st.success(
            "Prediction completed successfully!"
        )

        st.subheader("📈 Prediction Results")

        # --------------------------------------------------
        # Sample mode results
        # --------------------------------------------------
        if actual_rul is not None:

            prediction_error = abs(
                actual_rul - prediction
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:
                st.metric(
                    "Predicted RUL",
                    f"{prediction:.2f} cycles"
                )

            with result_col2:
                st.metric(
                    "Actual RUL",
                    f"{actual_rul:.2f} cycles"
                )

            with result_col3:
                st.metric(
                    "Absolute Error",
                    f"{prediction_error:.2f} cycles"
                )

        # --------------------------------------------------
        # Manual mode results
        # --------------------------------------------------
        else:

            st.metric(
                "Predicted Remaining Useful Life",
                f"{prediction:.2f} cycles"
            )


        # --------------------------------------------------
        # Maintenance status
        # --------------------------------------------------
        st.subheader("🔧 Maintenance Assessment")

        if prediction <= 30:

            st.error(
                "🔴 Critical Condition — "
                "Maintenance is recommended soon."
            )

        elif prediction <= 60:

            st.warning(
                "🟠 Warning Condition — "
                "Engine health is degrading."
            )

        else:

            st.info(
                "🟢 Healthy Condition — "
                "Engine currently has relatively higher remaining life."
            )


        # --------------------------------------------------
        # Sensor history chart for sample engine
        # --------------------------------------------------
        if selected_engine_data is not None:

            st.divider()

            st.subheader(
                "📉 Important Sensor Trends"
            )

            st.caption(
                "Historical trends of selected high-importance sensors "
                "for the chosen engine."
            )

            trend_sensors = [
                "sensor_11",
                "sensor_9",
                "sensor_4",
                "sensor_12"
            ]
            

            
            # Prepare sensor history data
            chart_data = (
                selected_engine_data[
                    ["cycle"] + trend_sensors
                    ]
                    .set_index("cycle")
                    .copy()
                )

            # Normalize each sensor independently to 0-1 range
            normalized_chart_data = (
                chart_data - chart_data.min()
                ) / (
                    chart_data.max() - chart_data.min()
                    )

            # Handle any constant sensor safely
            normalized_chart_data = normalized_chart_data.fillna(0)

            st.line_chart(
            normalized_chart_data
        )

            st.caption(
            "Sensor values are normalized independently to a 0–1 scale "
            "so trends with different measurement ranges can be compared."
        )


    except Exception as e:

        st.error(
            f"Prediction error: {e}"
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.caption(
    "Turbofan RUL Prediction Project | "
    "NASA C-MAPSS FD001 | Random Forest Regression"
)   