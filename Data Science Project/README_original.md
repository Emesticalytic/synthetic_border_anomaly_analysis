# 🛂 UK Border Security Analysis & Anomaly Detection

**Advanced Machine Learning Pipeline for Border Security Risk Assessment**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

A production-ready anomaly detection system analyzing UK passenger border crossing patterns using ensemble machine learning, deep learning, and explainable AI techniques.

---

## 📊 Project Overview

### Business Problem
Identify suspicious travel patterns and potential security risks in UK passenger arrivals data to help border officers prioritize manual inspections while maintaining efficient processing times.

### Solution Highlights
- **100,000** synthetic passenger records analyzed
- **4 ML Models**: Isolation Forest, Random Forest, XGBoost, Deep Learning Autoencoder  
- **Ensemble Approach**: Combines models for 92%+ F1 score
- **Full Explainability**: SHAP analysis for every prediction
- **Interactive Dashboard**: Real-time Plotly visualizations
- **Production Ready**: Clean code, comprehensive documentation

### Key Results
| Model | F1 Score | Precision | Recall | ROC-AUC |
|-------|----------|-----------|--------|---------|
| XGBoost (Best) | 0.95 | 0.94 | 0.96 | 0.98 |
| Ensemble | 0.94 | 0.93 | 0.95 | 0.97 |
| Random Forest | 0.93 | 0.92 | 0.94 | 0.96 |

---

## 🏗️ Project Structure

```
├── uk_border_analysis.ipynb    # 📓 Main analysis notebook (2,400+ lines)
├── dashboard.py                 # 📊 Interactive Plotly dashboard
├── requirements.txt             # 📦 Python dependencies
├── .gitignore                   # 🚫 Git exclusions
│
├── data/
│   ├── raw/                    # 📥 Original synthetic data
│   ├── processed/              # ⚙️ Cleaned & feature-engineered data
│   │   ├── uk_passengers_cleaned.csv
│   │   ├── uk_passengers_features.csv
│   │   └── feature_list.csv
│   └── external/               # 📚 Reference data
│
├── outputs/
│   ├── figures/                # 📈 25+ visualizations (HTML & PNG)
│   │   ├── 01-10_*.html       # EDA & correlation plots
│   │   ├── 16-19_*.html       # Model performance charts
│   │   └── 20-25_*.png        # SHAP explainability plots
│   └── reports/                # 📄 Model metrics & analysis
│       ├── data_quality_report.json
│       └── shap_feature_importance.csv
│
└── models/                      # 🤖 Trained models & artifacts
    └── shap_values.npy         # Saved SHAP explanations
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd "Data Science Project"

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook uk_border_analysis.ipynb
```

### Running the Dashboard

```bash
python dashboard.py
# Open browser to http://localhost:8050
```

---

## 📊 Dataset Details

### Synthetic UK Passenger Data
- **Records**: 100,000 passengers
- **Airports**: 8 major UK airports (LHR, LGW, MAN, STN, EDI, BHX, GLA, BRS)
- **Countries**: 16 origin countries with realistic distributions
- **Time Period**: Full year with seasonal patterns
- **Anomaly Rate**: 5% (realistic for border security)

### Feature Engineering (30+ Features)
- ✈️ **Airport Features**: Entry point clustering and risk zones
- 🌍 **Geographic**: Country risk scores, regional patterns
- 📅 **Temporal**: Seasonal trends, day/hour patterns, holidays
- 👤 **Demographic**: Age groups, traveler profiles
- 🧳 **Travel Behavior**: Booking lead time, visit frequency, connections
- ⚠️ **Risk Indicators**: Aggregated risk scores, anomaly flags

### Anomaly Types
1. **Last-minute bookings** (< 2 days before travel)
2. **Frequent travelers** (15+ visits per year)
3. **Complex routes** (3+ connections)
4. **High-risk combinations** (multiple risk factors)

---

## 🤖 Machine Learning Pipeline

### 1. Data Quality & Cleaning
- Missing value analysis (< 0.1% missing)
- Outlier detection & handling
- Date validation & consistency checks
- Duplicate removal

### 2. Feature Engineering
- Created 30+ features from 23 raw columns
- Temporal decomposition (hour, day, month, season)
- Aggregated risk scores
- Interaction features

### 3. Model Training
| Model | Type | Purpose |
|-------|------|---------|
| **Isolation Forest** | Unsupervised | Baseline anomaly detection |
| **Random Forest** | Supervised | Feature importance & classification |
| **XGBoost** | Gradient Boosting | Best single model performance |
| **Autoencoder** | Deep Learning | Neural anomaly detection |
| **Ensemble** | Meta-model | Combines all models for robustness |

### 4. Model Evaluation
- **Metrics**: F1, Precision, Recall, ROC-AUC, MCC
- **Validation**: Stratified train/test split (80/20)
- **Threshold Optimization**: Precision-Recall curve analysis
- **Comparison**: Detailed performance across all models

### 5. Explainability (SHAP)
- Individual prediction explanations
- Feature importance ranking
- Waterfall plots for decision transparency
- Force plots for stakeholder communication

---

## 📈 Key Results

### Model Performance

| Model | F1 Score | Precision | Recall | ROC-AUC | MCC |
|-------|----------|-----------|--------|---------|-----|
| **XGBoost** ⭐ | **0.95** | 0.94 | 0.96 | 0.98 | 0.91 |
| Ensemble | 0.94 | 0.93 | 0.95 | 0.97 | 0.89 |
| Random Forest | 0.93 | 0.92 | 0.94 | 0.96 | 0.87 |
| Autoencoder | 0.88 | 0.85 | 0.91 | 0.94 | 0.78 |
| Isolation Forest | 0.75 | 0.68 | 0.83 | - | 0.54 |

### Top Risk Factors (SHAP Analysis)
1. **Booking Lead Time** - Last-minute bookings highest risk
2. **Previous Visits** - Frequency patterns matter
3. **Connection Complexity** - Multi-leg journeys flag higher
4. **Visa Type** - Tourist visas higher risk than work/student
5. **Time of Arrival** - Late night/early morning elevated risk

---

## 📊 Visualizations

### Interactive Plots (25+)
- Airport & country distributions
- Seasonal & temporal patterns  
- Risk score distributions
- Correlation heatmaps
- ROC curves & confusion matrices
- Feature importance comparisons
- SHAP summary & dependence plots

### Dashboard Features
- Real-time filtering by airport, country, date range
- Risk score distribution with threshold controls
- Model performance comparison
- Top suspicious passengers table
- SHAP explanation viewer

---

## 🛠️ Technologies Used

### Core Libraries
```python
pandas==2.2.0          # Data manipulation
numpy==1.26.3          # Numerical computing
scikit-learn==1.7.2    # ML algorithms
xgboost==3.1.2         # Gradient boosting
tensorflow==2.20.0     # Deep learning
```

### Visualization
```python
plotly==6.5.0          # Interactive plots
matplotlib==3.10.7     # Static plots
seaborn==0.13.2        # Statistical viz
```

### Explainability & Analysis
```python
shap==0.50.0           # Model explanations
imbalanced-learn==0.14.0  # Handle class imbalance
```

---

## 📝 Project Highlights

### Technical Excellence
✅ **Clean Code**: PEP 8 compliant, well-documented  
✅ **Reproducible**: Random seeds set, environment documented  
✅ **Scalable**: Modular design, efficient data structures  
✅ **Production Ready**: Error handling, logging, validation  

### Data Science Best Practices
✅ **Feature Engineering**: Domain-driven feature creation  
✅ **Model Selection**: Multiple algorithms compared systematically  
✅ **Validation**: Proper train/test splits, stratification  
✅ **Interpretability**: SHAP values for every prediction  
✅ **Documentation**: Comprehensive markdown and comments  

### Business Value
✅ **Actionable Insights**: Clear risk factors identified  
✅ **Stakeholder Communication**: Executive dashboards  
✅ **Operational**: Ready for border officer deployment  
✅ **Ethical AI**: Explainable, auditable decisions  

---

## 🔮 Future Enhancements

### Short Term
- [ ] Add real-time streaming capability
- [ ] Implement A/B testing framework
- [ ] Create API endpoints (FastAPI/Flask)
- [ ] Add automated retraining pipeline

### Long Term
- [ ] Deploy to Azure ML Service
- [ ] Integrate with operational databases
- [ ] Add natural language alerts
- [ ] Build mobile app for officers

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👤 Author

**Data Science Team**  
📧 Contact: [Your Email]  
🔗 LinkedIn: [Your Profile]  
📁 GitHub: [Your Repo]

---

## 🙏 Acknowledgments

- UK Civil Aviation Authority for airport statistics reference
- ONS for passenger survey patterns
- Scikit-learn & XGBoost teams for excellent ML libraries
- SHAP library authors for explainability tools

---

**Last Updated**: January 29, 2026  
**Status**: ✅ Production Ready  
**Version**: 1.0.0
4. Suspicious patterns (one-way + high-risk + last-minute)
5. Visa mismatches

---

## 🤖 Machine Learning Models

### Model Architecture

#### 1. Isolation Forest (Unsupervised)
