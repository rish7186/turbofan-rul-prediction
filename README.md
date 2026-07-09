# ✈️ Turbofan Engine Remaining Useful Life Prediction

A machine learning-based predictive maintenance system for estimating the **Remaining Useful Life (RUL)** of turbofan engines using operational settings and sensor measurements.

The project uses the **NASA C-MAPSS FD001 dataset**, compares multiple regression approaches, evaluates the final model on the official FD001 test set, and provides an interactive **Streamlit dashboard** for RUL prediction and engine health assessment.

---

## 📌 Project Overview

Unexpected engine failures can lead to high maintenance costs, operational downtime, and safety risks. Predictive maintenance aims to estimate equipment degradation before failure occurs.

This project predicts:

> **Remaining Useful Life (RUL)** — the estimated number of operational cycles an engine can continue operating before reaching failure.

The complete project workflow includes:

- Data loading and validation
- Exploratory Data Analysis (EDA)
- Engine lifetime analysis
- Sensor trend analysis
- Constant sensor detection
- RUL target generation
- Feature selection
- Engine-wise train/validation splitting
- Linear Regression baseline modeling
- Random Forest Regression
- Capped RUL experimentation
- Feature importance analysis
- Official FD001 test-set evaluation
- Model serialization
- Reusable prediction module
- Interactive Streamlit dashboard

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Analyze turbofan engine degradation patterns
- Understand sensor behavior across operational cycles
- Identify useful and non-informative sensor features
- Generate RUL targets from run-to-failure training trajectories
- Prevent engine-level data leakage during validation
- Compare linear and nonlinear regression models
- Improve model performance using a capped RUL target
- Evaluate generalization on the official FD001 test dataset
- Build an interactive interface for model demonstration

---

## 📊 Dataset

This project uses the **NASA C-MAPSS Turbofan Engine Degradation Simulation Dataset**.

### Dataset Subset

The current implementation focuses on:

```text
FD001
```

FD001 contains:

- One operating condition
- One fault mode
- Multiple turbofan engine units
- Run-to-failure training trajectories
- Truncated test trajectories
- Ground-truth RUL values for test engines

### Main Files Used

```text
train_FD001.txt
test_FD001.txt
RUL_FD001.txt
```

### Data Structure

Each row represents one engine at one operational cycle.

The dataset contains:

```text
unit_id
cycle

setting_1
setting_2
setting_3

sensor_1
sensor_2
...
sensor_21
```

This gives:

- 1 engine identifier
- 1 cycle index
- 3 operational settings
- 21 sensor measurements

---

## 🧮 Remaining Useful Life Calculation

For the run-to-failure training dataset, RUL is calculated as:

```text
RUL = Maximum Cycle of Engine - Current Cycle
```

### Example

If an engine fails at cycle 192 and the current observation is cycle 188:

```text
RUL = 192 - 188
RUL = 4 cycles
```

At the final observed failure cycle:

```text
RUL = 0
```

---

## ✂️ Capped RUL Strategy

In addition to the original RUL target, this project evaluates a capped RUL formulation:

```text
Capped RUL = min(Original RUL, 125)
```

This means:

```text
Original RUL = 200  →  Capped RUL = 125
Original RUL = 140  →  Capped RUL = 125
Original RUL = 90   →  Capped RUL = 90
Original RUL = 20   →  Capped RUL = 20
```

The capped target reduces the influence of very large early-life RUL values and allows the model to focus more effectively on degradation-related patterns.

---

## 🔍 Exploratory Data Analysis

The EDA notebook investigates the structure and behavior of the FD001 dataset.

Analysis includes:

- Dataset shape inspection
- Data type inspection
- Missing-value analysis
- Duplicate-row detection
- Engine count analysis
- Operational lifetime analysis
- Lifetime distribution visualization
- Individual engine sensor trends
- Sensor variability analysis
- Constant sensor identification

### Constant Sensors Identified

The following sensors were identified as constant or effectively constant in FD001:

```text
sensor_1
sensor_5
sensor_10
sensor_16
sensor_18
sensor_19
```

These features were excluded from model training because they provide little or no useful predictive variation.

---

## 🧠 Machine Learning Models

Two main regression approaches were evaluated.

### 1. Linear Regression

Linear Regression was used as a baseline model.

#### Validation Results

| Metric | Score |
|---|---:|
| MAE | 30.11 cycles |
| RMSE | 38.13 cycles |
| R² | 0.6626 |

The baseline provides a reference point for evaluating more flexible nonlinear models.

---

### 2. Random Forest Regression

Random Forest Regression was used to capture nonlinear relationships between operational settings, sensor measurements, and RUL.

#### Validation Results

| Metric | Score |
|---|---:|
| MAE | 25.87 cycles |
| RMSE | 35.37 cycles |
| R² | 0.7098 |

Random Forest outperformed the Linear Regression baseline.

---

## 🚀 Capped RUL Experiment

A Random Forest model was trained using the capped RUL target with a maximum value of 125 cycles.

### Validation Results

| Metric | Score |
|---|---:|
| MAE | 12.35 cycles |
| RMSE | 17.07 cycles |
| R² | 0.8326 |

### Experiment Comparison

| Experiment | MAE | RMSE | R² |
|---|---:|---:|---:|
| Original RUL - Random Forest | 25.87 | 35.37 | 0.7098 |
| Capped RUL (125) - Random Forest | **12.35** | **17.07** | **0.8326** |

The capped RUL experiment achieved substantially better validation performance.

---

## 🧪 Final FD001 Test Evaluation

The selected model was evaluated on the official FD001 test set.

The final evaluation used:

```text
100 test engines
```

For each engine:

1. The latest available operational cycle was selected
2. Model features were extracted
3. RUL was predicted
4. Predictions were compared with the official ground-truth values from `RUL_FD001.txt`

### Final Test Results

| Metric | Score |
|---|---:|
| MAE | **12.92 cycles** |
| RMSE | **17.75 cycles** |
| R² | **0.8175** |

These results indicate that the model captures a substantial portion of RUL variation on unseen FD001 test engines.

---

## 📈 Feature Importance

Random Forest feature importance analysis was used to identify influential model inputs.

### Top 10 Important Features

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | sensor_11 | 0.487307 |
| 2 | sensor_9 | 0.133372 |
| 3 | sensor_4 | 0.078096 |
| 4 | sensor_12 | 0.043313 |
| 5 | sensor_14 | 0.036145 |
| 6 | sensor_7 | 0.033212 |
| 7 | sensor_15 | 0.027508 |
| 8 | sensor_21 | 0.026378 |
| 9 | sensor_3 | 0.023659 |
| 10 | sensor_2 | 0.022337 |

Among the evaluated features, `sensor_11` had the highest Random Forest feature importance.

> Feature importance reflects the behavior of the trained model and should not automatically be interpreted as physical causality.

---

## 📉 Visualizations

The project generates multiple analytical and evaluation visualizations, including:

- Operational lifetime of each engine
- Distribution of engine lifetimes
- Sensor trends over operational cycles
- Individual important sensor trends
- Random Forest feature importance
- Actual vs Predicted RUL
- Distribution of absolute prediction errors

These visualizations help analyze degradation behavior and model performance.

---

## 🖥️ Streamlit Dashboard

An interactive Streamlit dashboard is included for model demonstration.

### Dashboard Features

The application supports:

- Selection of actual FD001 test engines
- Automatic loading of the selected engine's latest observed measurements
- Manual sensor input
- RUL prediction
- Actual RUL display for FD001 sample engines
- Absolute prediction error calculation
- Maintenance condition assessment
- Important sensor trend visualization

### Prediction Results

For sample FD001 engines, the dashboard can display:

```text
Predicted RUL
Actual RUL
Absolute Error
```

The **Actual RUL** is obtained from the official FD001 ground-truth file:

```text
RUL_FD001.txt
```

In a real production environment, the future true RUL would not normally be known at prediction time.

---

## 🔧 Maintenance Assessment

The dashboard converts predicted RUL into simple maintenance categories.

| Predicted RUL | Assessment |
|---|---|
| RUL ≤ 30 | 🔴 Critical Condition |
| 30 < RUL ≤ 60 | 🟡 Warning Condition |
| RUL > 60 | 🟢 Healthy Condition |

> These thresholds are application-level demonstration rules. They are not official NASA or aerospace maintenance thresholds.

---

## 📊 Sensor Trend Visualization

The dashboard visualizes selected high-importance sensors such as:

```text
sensor_11
sensor_12
sensor_4
sensor_9
```

Because these sensors operate on very different numerical scales, trend values are normalized for visualization.

The normalization is applied only to the dashboard chart.

> The trained model continues to use the original sensor measurements for prediction.

---

## 🏗️ Project Structure

```text
turbofan-rul-prediction/
│
├── app/
│   └── app.py
│
├── data/
│   ├── processed/
│   ├── raw/
│   │   ├── train_FD001.txt
│   │   ├── train_FD002.txt
│   │   ├── train_FD003.txt
│   │   ├── train_FD004.txt
│   │   ├── test_FD001.txt
│   │   ├── test_FD002.txt
│   │   ├── test_FD003.txt
│   │   ├── test_FD004.txt
│   │   ├── RUL_FD001.txt
│   │   ├── RUL_FD002.txt
│   │   ├── RUL_FD003.txt
│   │   └── RUL_FD004.txt
│   └── reference/
│
├── models/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   └── 02_model_building.ipynb
│
├── reports/
│   └── figures/
│
├── src/
│   └── predict.py
│
├── tests/
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd turbofan-rul-prediction
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit Application

From the project root directory, run:

```bash
streamlit run app/app.py
```

The application will normally open automatically in your browser.

Typical local address:

```text
http://localhost:8501
```

---

## 🧪 Run the Prediction Module

The reusable prediction module can be tested using:

```bash
python src/predict.py
```

This verifies that the trained RUL prediction model and feature configuration can be loaded successfully.

---

## 🔄 Machine Learning Workflow

```text
NASA C-MAPSS FD001 Dataset
            │
            ▼
Data Loading and Validation
            │
            ▼
Exploratory Data Analysis
            │
            ▼
RUL Target Generation
            │
            ▼
Constant Sensor Detection
            │
            ▼
Feature Selection
            │
            ▼
Engine-Wise Train/Validation Split
            │
            ▼
Linear Regression Baseline
            │
            ▼
Random Forest Regression
            │
            ▼
Capped RUL Experiment
            │
            ▼
Feature Importance Analysis
            │
            ▼
Official FD001 Test Evaluation
            │
            ▼
Model Serialization
            │
            ▼
Reusable Prediction Module
            │
            ▼
Streamlit Dashboard
```

---

## 🛡️ Data Leakage Prevention

A key part of the project is engine-wise dataset splitting.

Instead of randomly splitting individual rows, complete engine IDs are assigned to either:

- Training set
- Validation set

This prevents observations from the same engine from appearing in both datasets.

The implemented split contained:

```text
Training engines   : 80
Validation engines : 20
```

The overlap verification confirmed:

```text
set()
```

Therefore, no engine appeared in both training and validation sets.

---

## 📏 Evaluation Metrics

The project uses three regression metrics.

### Mean Absolute Error (MAE)

Measures the average absolute difference between actual and predicted RUL.

Lower values are better.

### Root Mean Squared Error (RMSE)

Measures prediction error while penalizing large errors more strongly.

Lower values are better.

### R² Score

Measures how much variation in the target is explained by the model.

Higher values are generally better.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- Jupyter Notebook
- Joblib
- VS Code

---

## 📌 Key Results

The main project results are summarized below:

| Stage | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression Validation | 30.11 | 38.13 | 0.6626 |
| Random Forest Validation | 25.87 | 35.37 | 0.7098 |
| Capped RUL Random Forest Validation | **12.35** | **17.07** | **0.8326** |
| Final FD001 Test Evaluation | **12.92** | **17.75** | **0.8175** |

---

## ⚠️ Important Notes

- The current trained and evaluated workflow focuses on **FD001**
- Actual RUL values in sample-engine mode come from `RUL_FD001.txt`
- Actual future RUL would not be known during real-world inference
- Sensor trend normalization is used only for visualization
- Model predictions use the original feature values
- Maintenance thresholds are demonstration rules
- Random Forest feature importance does not prove physical causality
- The project is intended for educational, portfolio, and predictive-maintenance experimentation purposes

---

## 🔮 Future Improvements

Potential future improvements include:

- Hyperparameter optimization
- Cross-validation at engine level
- Rolling-window sensor features
- Sensor degradation-rate features
- XGBoost regression
- LightGBM regression
- LSTM-based sequence modeling
- Transformer-based time-series modeling
- Prediction uncertainty estimation
- SHAP-based explainability
- NASA scoring function evaluation
- FD002, FD003, and FD004 model support
- Automated testing
- REST API integration
- Docker containerization
- Cloud deployment
- MLOps experiment tracking

---

## 👨‍💻 Author

**Rishabh Brahmane**

Bachelor of Computer Science Engineering  
ITM (SLS) Baroda University

---

## 📄 Disclaimer

This project is developed for educational, academic, portfolio, and internship demonstration purposes.

The predictions and maintenance categories produced by this application should not be used for real-world aviation maintenance or safety-critical operational decisions without appropriate domain validation, certification, and engineering review.