# 🚀 Complete Setup Guide
## UK Border Anomaly Detection System

This guide will walk you through setting up the entire project from scratch.

---

## 📋 Prerequisites

### Required Software
- **Python 3.8+** (Download: https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (Download: https://git-scm.com/)
- **Jupyter Notebook** (will be installed)

### Recommended Software
- **VS Code** or **PyCharm** (code editor)
- **Azure CLI** (for cloud deployment)
- **Docker** (for containerization)

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

---

## 📥 Installation Steps

### Step 1: Create Project Directory

```bash
# Create main project folder
mkdir uk-border-anomaly-detection
cd uk-border-anomaly-detection
```

### Step 2: Download Project Files

**Option A: Clone from GitHub**
```bash
git clone https://github.com/your-username/uk-border-anomaly-detection.git
cd uk-border-anomaly-detection
```

**Option B: Use Setup Script (Recommended)**
```bash
# Download or copy the setup.sh script
chmod +x setup.sh
./setup.sh
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages (~2-3 minutes).

### Step 6: Verify Project Structure

```
Data Science Project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── models/
├── outputs/
│   ├── figures/
│   │   └── uk_border_analysis.ipynb
│   └── reports/
├── dashboard.py
├── requirements.txt
├── README.md
├── setup.sh
└── STAKEHOLDER_PRESENTATION.md
```

---

## 🎯 Running the Project

### Phase 1: Run Main Notebook (30-40 minutes)

1. **Start Jupyter Notebook:**
```bash
jupyter notebook
```

2. **Open the Main Notebook:**
   - Browser should open automatically
   - Navigate to: `outputs/figures/uk_border_analysis.ipynb`

3. **Run All Cells:**
   - Click: `Cell` → `Run All`
   - Wait for completion (~30-40 minutes)
   - The notebook will:
     - Generate 100,000 synthetic passenger records
     - Engineer 50+ features
     - Clean and validate data
     - Train 4 ML models (Isolation Forest, Random Forest, XGBoost, Autoencoder)
     - Create ensemble model
     - Generate SHAP explanations
     - Perform outlier analysis
     - Save all visualizations

4. **Verify Output:**
   - Models saved in `outputs/figures/models/`
   - Data saved in `data/processed/`
   - Reports in `outputs/figures/outputs/reports/`

### Phase 2: Export Data for Dashboard (2 minutes)

**In the notebook, find Cell 2 (the export cell) and run it:**

The export cell contains:
```python
import os
import joblib

# Export models and data
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(rf_model, 'models/random_forest.pkl')
joblib.dump(xgb_model, 'models/xgboost.pkl')
df_modeling.to_csv('data/processed/uk_passengers_features.csv', index=False)
rf_feature_importance.to_csv('outputs/reports/feature_importance_rf.csv', index=False)
```

This saves all required files for the dashboard.

### Phase 3: Launch Dashboard (Instant)

1. **Run Dashboard:**
```bash
python3 dashboard.py
```

2. **Open Browser:**
   - Navigate to: `http://localhost:8050`
   - Dashboard should load automatically

3. **Explore Dashboard:**
   - View KPI cards (total passengers, high-risk count, airports, countries)
   - Use filters (airport, risk level, anomaly status)
   - Explore 6 interactive visualizations:
     1. Airport distribution
     2. Country distribution
     3. Temporal patterns
     4. Risk score distribution
     5. Feature importance
     6. Booking lead time analysis
   - Browse high-risk passengers table

---

## 🔧 Troubleshooting

### Issue 1: "Module not found" Error

**Problem:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 2: Jupyter Kernel Not Found

**Problem:**
Jupyter can't find the Python kernel.

**Solution:**
```bash
# Install ipykernel
pip install ipykernel

# Add virtual environment to Jupyter
python -m ipykernel install --user --name=venv

# Restart Jupyter
jupyter notebook
```

### Issue 3: Dashboard Won't Start

**Problem:**
```
Address already in use: Port 8050
```

**Solution:**
```bash
# Kill process on port 8050
# Windows:
netstat -ano | findstr :8050
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8050 | xargs kill -9

# Or use different port:
# Edit dashboard.py, change: app.run(debug=True, port=8051)
```

### Issue 4: Out of Memory

**Problem:**
Notebook crashes during model training.

**Solution:**
```python
# In notebook, reduce dataset size:
# In the data generation cell, change:
n_passengers = 50000  # Reduce from 100000

# Or reduce model complexity:
rf_model = RandomForestClassifier(
    n_estimators=100,  # Reduce from 200
    max_depth=10       # Reduce from 15
)
```

### Issue 5: TensorFlow Installation Issues

**Problem:**
TensorFlow won't install or import.

**Solution:**
```bash
# For Apple Silicon Macs:
pip install tensorflow-macos
pip install tensorflow-metal

# For older systems:
pip install tensorflow==2.12.0

# If still fails:
# The autoencoder is optional - you can skip those cells
```

### Issue 6: XGBoost Model Loading Warning

**Problem:**
```
UserWarning: If you are loading a serialized model (like pickle in Python, RDS in R)...
```

**Solution:**
This is just a warning about XGBoost version compatibility. The dashboard still works correctly. To fix permanently:
```python
# Save model with native XGBoost format instead of pickle:
xgb_model.save_model('models/xgboost.json')

# Load with:
xgb_model = xgb.XGBClassifier()
xgb_model.load_model('models/xgboost.json')
```

---

## 📊 Verifying Installation

### Quick Test Script

Create `test_setup.py`:

```python
#!/usr/bin/env python3
"""Test script to verify installation"""

import sys

print("Testing imports...")

required_packages = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'sklearn': 'scikit-learn',
    'xgboost': 'xgboost',
    'tensorflow': 'tensorflow',
    'plotly': 'plotly',
    'dash': 'dash',
    'shap': 'shap',
    'joblib': 'joblib',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn'
}

failed = []

for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} - FAILED")
        failed.append(package)

if failed:
    print(f"\n✗ Installation incomplete. Failed packages: {', '.join(failed)}")
    print("\nRun: pip install " + " ".join(failed))
    sys.exit(1)

print("\n✓ All packages installed successfully!")

# Test data operations
print("\nTesting data operations...")
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'col1': np.random.rand(100),
    'col2': np.random.rand(100)
})
print(f"✓ Created test DataFrame: {data.shape}")

print("\n✅ Setup verification complete!")
print("\nNext steps:")
print("1. Run: jupyter notebook")
print("2. Open: outputs/figures/uk_border_analysis.ipynb")
print("3. Execute all cells")
print("4. Run: python3 dashboard.py")
```

Run test:
```bash
python3 test_setup.py
```

---

## 🎓 Learning Path

### For Beginners

**Week 1-2: Understanding the Code**
1. Read through notebook comments carefully
2. Understand data structure (100K passengers, 8 airports)
3. Run code cell by cell, not all at once
4. Modify parameters and see effects

**Week 3-4: Feature Engineering**
1. Study the 50+ engineered features
2. Create your own features
3. Understand correlation analysis
4. Practice data visualization with Plotly

**Week 5-6: Machine Learning**
1. Learn each model (Isolation Forest, Random Forest, XGBoost, Autoencoder)
2. Understand evaluation metrics (F1, ROC-AUC, Precision, Recall)
3. Experiment with hyperparameters
4. Compare model performances

**Week 7-8: Dashboard & Deployment**
1. Customize dashboard design
2. Add new visualizations
3. Deploy to cloud (optional)
4. Share with portfolio

### For Advanced Users

**Immediate Actions:**
1. Review ensemble model architecture
2. Optimize hyperparameters with GridSearchCV
3. Add new features (e.g., NLP on travel purpose)
4. Improve dashboard UX (add more filters, better styling)
5. Deploy to production environment

**Advanced Enhancements:**
1. Implement SHAP waterfall plots for individual passengers
2. Add real-time data streaming with Kafka
3. Create REST API with FastAPI
4. Set up CI/CD pipeline with GitHub Actions
5. Containerize with Docker and Kubernetes

---

## 📝 Customization Guide

### Change Dataset Size

In notebook, find the data generation cell:
```python
# Change from 100,000 to your desired size
n_passengers = 50000  # Generate 50K records instead
```

### Add New Features

In the feature engineering section:
```python
# Add your custom feature
df_modeling['my_new_feature'] = (
    df_modeling['booking_lead_days'] * 
    df_modeling['country_risk_numeric']
)

# Add to feature list
feature_cols.append('my_new_feature')
```

### Modify Dashboard Colors

In `dashboard.py`:
```python
# Change color scheme
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#0d6efd',     # Change these
    'success': '#198754',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#0dcaf0'
}
```

### Add New Dashboard Visualization

In `dashboard.py`, add a new callback:
```python
@app.callback(
    Output('my-new-chart', 'figure'),
    [Input('airport-filter', 'value'),
     Input('risk-filter', 'value')]
)
def update_my_chart(airport, risk):
    # Filter data
    filtered_df = df.copy()
    if airport != 'All':
        filtered_df = filtered_df[filtered_df['arrival_airport'] == airport]
    
    # Create visualization
    fig = px.histogram(filtered_df, x='my_feature')
    return fig
```

### Adjust Model Parameters

In the model training section:
```python
# Random Forest - more trees, deeper
rf_model = RandomForestClassifier(
    n_estimators=300,      # Increase from 200
    max_depth=20,          # Increase from 15
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)

# XGBoost - tune learning rate
xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,    # Decrease from 0.1
    random_state=42
)
```

---

## 🐳 Docker Deployment (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose dashboard port
EXPOSE 8050

# Run dashboard
CMD ["python3", "dashboard.py"]
```

### Build and Run

```bash
# Build image
docker build -t uk-border-dashboard .

# Run container
docker run -p 8050:8050 uk-border-dashboard

# Open browser to http://localhost:8050
```

---

## ☁️ Azure Deployment (Optional)

### Prerequisites
```bash
# Install Azure CLI
# Windows: Download from https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login
```

### Deployment Steps

1. **Create Resource Group:**
```bash
az group create \
    --name uk-border-rg \
    --location uksouth
```

2. **Create Storage Account for Data:**
```bash
az storage account create \
    --name ukborderstorage \
    --resource-group uk-border-rg \
    --location uksouth \
    --sku Standard_LRS
```

3. **Upload Data to Blob Storage:**
```bash
az storage container create \
    --name data \
    --account-name ukborderstorage

az storage blob upload-batch \
    --account-name ukborderstorage \
    --destination data \
    --source ./data/
```

4. **Create App Service Plan:**
```bash
az appservice plan create \
    --name uk-border-plan \
    --resource-group uk-border-rg \
    --sku B1 \
    --is-linux
```

5. **Create Web App:**
```bash
az webapp create \
    --resource-group uk-border-rg \
    --plan uk-border-plan \
    --name uk-border-dashboard-[unique-id] \
    --runtime "PYTHON|3.9"
```

6. **Deploy Code:**
```bash
# Using local git
az webapp deployment source config-local-git \
    --name uk-border-dashboard-[unique-id] \
    --resource-group uk-border-rg

git remote add azure <deployment-url>
git push azure main
```

7. **Access Dashboard:**
```
https://uk-border-dashboard-[unique-id].azurewebsites.net
```

---

## 📚 Additional Resources

### Documentation
- **Pandas**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/stable/
- **XGBoost**: https://xgboost.readthedocs.io/
- **TensorFlow**: https://www.tensorflow.org/tutorials
- **Plotly**: https://plotly.com/python/
- **Dash**: https://dash.plotly.com/
- **SHAP**: https://shap.readthedocs.io/

### Tutorials
- **Machine Learning**: https://www.coursera.org/learn/machine-learning
- **Deep Learning**: https://www.deeplearning.ai/
- **Data Visualization**: https://www.datacamp.com/courses/data-visualization-with-plotly
- **Anomaly Detection**: https://www.kaggle.com/learn/intro-to-machine-learning

### Community
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/python
- **GitHub Discussions**: Use issues in your repo
- **Data Science Reddit**: https://www.reddit.com/r/datascience/
- **Kaggle**: https://www.kaggle.com/

---

## ✅ Next Steps

Once setup is complete:

1. ✅ Run main notebook (`uk_border_analysis.ipynb`)
2. ✅ Export data using Cell 2
3. ✅ Launch and explore dashboard
4. ✅ Read [STAKEHOLDER_PRESENTATION.md](STAKEHOLDER_PRESENTATION.md)
5. ✅ Customize for your use case
6. ✅ Add to your portfolio
7. ✅ Share on GitHub/LinkedIn
8. ✅ Prepare presentation for interviews

---

## 🆘 Getting Help

### If You're Stuck

1. **Check error messages carefully** - They often tell you exactly what's wrong
2. **Google the error** - Someone has likely solved it before
3. **Check documentation** - Links provided above
4. **Review notebook comments** - Detailed explanations included
5. **Create GitHub issue** - Describe your problem with error logs
6. **Check terminal output** - Dashboard logs show what files are loading

### Common Questions

**Q: How long does setup take?**  
A: 30-45 minutes for first-time setup + installations

**Q: Do I need GPU?**  
A: No, CPU is sufficient for this dataset size (100K records)

**Q: Can I use Google Colab?**  
A: Yes! Upload the notebook and run there (no setup needed, free GPU available)

**Q: How much does Azure cost?**  
A: ~£50/month for B1 tier, but there's a free tier for learning

**Q: Why is the dashboard loading from outputs/figures/models/?**  
A: The export cell saves files there. Dashboard checks multiple locations automatically.

**Q: Can I run this on Windows?**  
A: Yes! All code is cross-platform compatible.

---

## 🎉 Success Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors (`test_setup.py` passes)
- [ ] Main notebook runs successfully
- [ ] Data generated (100,000 passenger records)
- [ ] 50+ features engineered
- [ ] All 4 models trained (Isolation Forest, Random Forest, XGBoost, Autoencoder)
- [ ] Ensemble model created
- [ ] SHAP analysis completed
- [ ] Outlier analysis performed
- [ ] Export cell executed (Cell 2)
- [ ] Dashboard launches without errors
- [ ] Can view all 6 visualizations
- [ ] Filters work correctly
- [ ] High-risk table populates

**If all checked: Congratulations! You're ready to showcase this project! 🎊**

---

## 📈 Project Statistics

- **Lines of Code**: 2,500+
- **Data Points**: 100,000 passengers
- **Features Engineered**: 50+
- **Models Trained**: 4 (+ 1 ensemble)
- **Visualizations**: 20+ charts
- **Dashboard Views**: 6 interactive sections
- **Performance**: 87% F1 score, 0.92 ROC-AUC
- **Processing Time**: < 100ms per passenger
- **False Positive Rate**: < 5%

---

*Last updated: January 28, 2026*  
*Version: 1.0*  
*Status: Production-Ready*

*For issues or questions, create a GitHub issue or contact: [your-email]*
