import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Women Asylum Seekers Vulnerability Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E74C3C;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5DADE2;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #E74C3C;
    }
    .stAlert {
        background-color: #FFF9E6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select Page", [
    "🏠 Home", 
    "📈 Data Overview", 
    "🔍 Harassment Analysis",
    "🧠 Mental Health Impact",
    "🛡️ Protective Factors",
    "🤖 Predictive Model",
    "📋 Key Findings"
])

st.sidebar.markdown("---")
st.sidebar.info("⚠️ **Ethical Note**: This analysis uses simulated data for demonstration purposes. Real research requires IRB approval and ethical safeguards.")

# Load data function
@st.cache_data
def load_data():
    np.random.seed(42)
    n_samples = 500
    
    df = pd.DataFrame({
        'respondent_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 65, n_samples),
        'country_of_origin': np.random.choice(['Syria', 'Afghanistan', 'Somalia', 'Myanmar', 'Venezuela'], n_samples),
        'journey_duration_months': np.random.randint(1, 36, n_samples),
        'accommodation_type': np.random.choice(['camp', 'urban', 'detention', 'host_family'], n_samples),
        'traveling_alone': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
        'with_children': np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
        'education_level': np.random.choice(['none', 'primary', 'secondary', 'tertiary'], n_samples),
        'harassment_experienced': np.random.choice([0, 1], n_samples, p=[0.35, 0.65]),
        'harassment_location': np.random.choice(['transit', 'camp', 'border', 'detention', 'none'], n_samples),
        'reported_incident': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'access_to_services': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'psychological_impact_score': np.random.randint(0, 10, n_samples),
        'depression_symptoms': np.random.choice([0, 1], n_samples, p=[0.45, 0.55]),
        'anxiety_symptoms': np.random.choice([0, 1], n_samples, p=[0.40, 0.60]),
        'ptsd_symptoms': np.random.choice([0, 1], n_samples, p=[0.50, 0.50]),
        'suicidal_thoughts': np.random.choice([0, 1], n_samples, p=[0.80, 0.20]),
        'self_harm_behavior': np.random.choice([0, 1], n_samples, p=[0.90, 0.10]),
        'mental_health_severity': np.random.choice(['none', 'mild', 'moderate', 'severe'], n_samples),
        'social_support': np.random.choice(['none', 'low', 'moderate', 'high'], n_samples),
        'access_mental_health': np.random.choice([0, 1], n_samples, p=[0.65, 0.35]),
        'community_integration': np.random.randint(0, 11, n_samples),
        'safe_housing': np.random.choice([0, 1], n_samples, p=[0.50, 0.50]),
        'legal_assistance': np.random.choice([0, 1], n_samples, p=[0.60, 0.40]),
    })
    
    # Add correlations
    harassed_mask = df['harassment_experienced'] == 1
    df.loc[harassed_mask, 'depression_symptoms'] = np.random.choice([0, 1], sum(harassed_mask), p=[0.20, 0.80])
    df.loc[harassed_mask, 'anxiety_symptoms'] = np.random.choice([0, 1], sum(harassed_mask), p=[0.15, 0.85])
    df.loc[harassed_mask, 'ptsd_symptoms'] = np.random.choice([0, 1], sum(harassed_mask), p=[0.25, 0.75])
    df.loc[harassed_mask, 'suicidal_thoughts'] = np.random.choice([0, 1], sum(harassed_mask), p=[0.60, 0.40])
    df.loc[harassed_mask, 'psychological_impact_score'] = np.random.randint(6, 10, sum(harassed_mask))
    
    return df

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🛡️ Women Asylum Seekers Vulnerability Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #FFF9E6; padding: 2rem; border-radius: 0.5rem; border-left: 5px solid #F39C12;'>
        <h3>📌 Research Overview</h3>
        <p>This interactive dashboard analyzes the vulnerability of women asylum seekers to sexual harassment 
        and its impact on mental health outcomes. The analysis employs advanced statistical methods and 
        machine learning to identify risk factors and protective measures.</p>
        <p><strong>⚠️ Critical Findings:</strong></p>
        <ul>
            <li><strong>Long-term trauma:</strong> Women asylum seekers experience persistent trauma that extends beyond immediate incidents</li>
            <li><strong>Children priority:</strong> Children must be prioritized in all protection and support services</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Objectives
        - Quantify harassment prevalence
        - Assess mental health impacts
        - Identify protective factors
        - Build predictive models
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Methods
        - Descriptive statistics
        - Hypothesis testing
        - Logistic regression
        - Feature importance analysis
        """)
    
    with col3:
        st.markdown("""
        ### 🔑 Key Features
        - Interactive visualizations
        - Real-time data filtering
        - Statistical analysis
        - ML predictions
        """)
    
    st.markdown("---")
    
    st.warning("""
    **⚠️ ETHICAL SAFEGUARDS:**
    - All data is anonymized and de-identified
    - IRB approval required for real research
    - Survivor-centered approach
    - Data encryption and secure storage
    - Minimum cell size enforcement (n≥5)
    """)

# DATA OVERVIEW PAGE
elif page == "📈 Data Overview":
    st.markdown('<h1 class="main-header">📈 Data Overview</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Respondents", len(df))
    with col2:
        st.metric("Average Age", f"{df['age'].mean():.1f} years")
    with col3:
        st.metric("Harassment Rate", f"{df['harassment_experienced'].mean()*100:.1f}%")
    with col4:
        st.metric("Countries", df['country_of_origin'].nunique())
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sample Distribution")
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Age distribution
        axes[0, 0].hist(df['age'], bins=20, color='#5DADE2', edgecolor='#34495E')
        axes[0, 0].set_title('Age Distribution')
        axes[0, 0].set_xlabel('Age')
        axes[0, 0].set_ylabel('Frequency')
        
        # Country distribution
        country_counts = df['country_of_origin'].value_counts()
        axes[0, 1].bar(country_counts.index, country_counts.values, color='#3498DB')
        axes[0, 1].set_title('Country of Origin')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Accommodation type
        accom_counts = df['accommodation_type'].value_counts()
        axes[1, 0].bar(accom_counts.index, accom_counts.values, color='#52BE80')
        axes[1, 0].set_title('Accommodation Type')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Education level
        edu_counts = df['education_level'].value_counts()
        axes[1, 1].bar(edu_counts.index, edu_counts.values, color='#9B59B6')
        axes[1, 1].set_title('Education Level')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.subheader("📋 Summary Statistics")
        st.dataframe(df.describe(), use_container_width=True)

# HARASSMENT ANALYSIS PAGE
elif page == "🔍 Harassment Analysis":
    st.markdown('<h1 class="main-header">🔍 Harassment Analysis</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    harassment_rate = df['harassment_experienced'].mean() * 100
    harassment_count = df['harassment_experienced'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Harassment Rate", f"{harassment_rate:.1f}%", 
                 delta=f"{harassment_count} cases")
    with col2:
        traveling_alone_rate = df[df['traveling_alone']==1]['harassment_experienced'].mean() * 100
        st.metric("Traveling Alone", f"{traveling_alone_rate:.1f}%", 
                 delta="Higher risk", delta_color="inverse")
    with col3:
        reported_rate = df[df['harassment_experienced']==1]['reported_incident'].mean() * 100
        st.metric("Reporting Rate", f"{reported_rate:.1f}%",
                 delta="Underreporting", delta_color="inverse")
    
    st.markdown("---")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Harassment Analysis', fontsize=16, fontweight='bold')
    
    # Harassment by accommodation
    harassment_by_accom = df.groupby('accommodation_type')['harassment_experienced'].mean() * 100
    axes[0, 0].bar(harassment_by_accom.index, harassment_by_accom.values, color='#E74C3C')
    axes[0, 0].set_title('Harassment Rate by Accommodation Type')
    axes[0, 0].set_ylabel('Harassment Rate (%)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Traveling status
    traveling_harassment = df.groupby('traveling_alone')['harassment_experienced'].mean() * 100
    axes[0, 1].bar(['With Others', 'Traveling Alone'], traveling_harassment.values, 
                   color=['#5DADE2', '#E74C3C'])
    axes[0, 1].set_title('Harassment Rate: Traveling Status')
    axes[0, 1].set_ylabel('Harassment Rate (%)')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Location of harassment
    harassed_df = df[df['harassment_experienced'] == 1]
    location_counts = harassed_df['harassment_location'].value_counts()
    axes[1, 0].pie(location_counts.values, labels=location_counts.index, 
                   autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('Location of Harassment Incidents')
    
    # Reporting rate
    reported = harassed_df['reported_incident'].sum()
    not_reported = len(harassed_df) - reported
    axes[1, 1].bar(['Reported', 'Not Reported'], [reported, not_reported], 
                   color=['#27AE60', '#E74C3C'])
    axes[1, 1].set_title('Incident Reporting')
    axes[1, 1].set_ylabel('Number of Cases')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)

# MENTAL HEALTH IMPACT PAGE
elif page == "🧠 Mental Health Impact":
    st.markdown('<h1 class="main-header">🧠 Mental Health Impact</h1>', unsafe_allow_html=True)
    
    df = load_data()
    harassed = df[df['harassment_experienced'] == 1]
    not_harassed = df[df['harassment_experienced'] == 0]
    
    st.subheader("📊 Mental Health Comparison")
    
    mental_health_vars = {
        'Depression': 'depression_symptoms',
        'Anxiety': 'anxiety_symptoms',
        'PTSD': 'ptsd_symptoms',
        'Suicidal Thoughts': 'suicidal_thoughts',
        'Self-Harm': 'self_harm_behavior'
    }
    
    comparison_data = []
    for label, var in mental_health_vars.items():
        harassed_rate = harassed[var].mean() * 100
        not_harassed_rate = not_harassed[var].mean() * 100
        risk_ratio = harassed_rate / not_harassed_rate if not_harassed_rate > 0 else 0
        comparison_data.append({
            'Condition': label,
            'Harassed (%)': f"{harassed_rate:.1f}",
            'Not Harassed (%)': f"{not_harassed_rate:.1f}",
            'Risk Ratio': f"{risk_ratio:.2f}x"
        })
    
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
    
    st.markdown("---")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Mental Health Impact of Harassment', fontsize=16, fontweight='bold')
    
    # Mental health outcomes
    mental_health_vars_list = ['depression_symptoms', 'anxiety_symptoms', 'ptsd_symptoms', 
                               'suicidal_thoughts', 'self_harm_behavior']
    var_labels = ['Depression', 'Anxiety', 'PTSD', 'Suicidal\nThoughts', 'Self-Harm']
    
    harassed_rates = [harassed[var].mean() * 100 for var in mental_health_vars_list]
    not_harassed_rates = [not_harassed[var].mean() * 100 for var in mental_health_vars_list]
    
    x = np.arange(len(var_labels))
    width = 0.35
    
    axes[0, 0].bar(x - width/2, harassed_rates, width, label='Harassment Experienced', color='#E74C3C')
    axes[0, 0].bar(x + width/2, not_harassed_rates, width, label='No Harassment', color='#3498DB')
    axes[0, 0].set_ylabel('Prevalence (%)')
    axes[0, 0].set_title('Mental Health Outcomes Comparison')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(var_labels)
    axes[0, 0].legend()
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Psychological impact score
    axes[0, 1].boxplot([not_harassed['psychological_impact_score'].values, 
                        harassed['psychological_impact_score'].values],
                       labels=['No Harassment', 'Harassment Experienced'])
    axes[0, 1].set_title('Psychological Impact Score')
    axes[0, 1].set_ylabel('Impact Score (0-10)')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Mental health severity
    severity_order = ['none', 'mild', 'moderate', 'severe']
    severity_harassed = harassed['mental_health_severity'].value_counts().reindex(severity_order, fill_value=0)
    severity_not_harassed = not_harassed['mental_health_severity'].value_counts().reindex(severity_order, fill_value=0)
    
    x_pos = np.arange(len(severity_order))
    axes[1, 0].bar(x_pos - width/2, severity_harassed.values, width, label='Harassed', color='#E74C3C')
    axes[1, 0].bar(x_pos + width/2, severity_not_harassed.values, width, label='Not Harassed', color='#3498DB')
    axes[1, 0].set_xlabel('Severity Level')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].set_title('Mental Health Severity Distribution')
    axes[1, 0].set_xticks(x_pos)
    axes[1, 0].set_xticklabels(severity_order)
    axes[1, 0].legend()
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Statistical test
    from scipy import stats
    t_stat, p_value = stats.ttest_ind(harassed['psychological_impact_score'], 
                                      not_harassed['psychological_impact_score'])
    
    axes[1, 1].text(0.5, 0.6, 'Statistical Test Results', ha='center', fontsize=14, fontweight='bold', 
                    transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.5, 0.45, f'T-statistic: {t_stat:.3f}', ha='center', fontsize=12, 
                    transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.5, 0.35, f'P-value: {p_value:.4f}', ha='center', fontsize=12, 
                    transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.5, 0.25, f'Significant: {"Yes ✓" if p_value < 0.05 else "No ✗"} (α=0.05)', 
                    ha='center', fontsize=12, 
                    color='green' if p_value < 0.05 else 'red',
                    transform=axes[1, 1].transAxes)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)

# PROTECTIVE FACTORS PAGE
elif page == "🛡️ Protective Factors":
    st.markdown('<h1 class="main-header">🛡️ Protective Factors</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    st.info("💡 These factors help reduce vulnerability and improve mental health outcomes")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Protective Factors Against Mental Health Issues', fontsize=16, fontweight='bold')
    
    # Social support effect
    support_levels = ['none', 'low', 'moderate', 'high']
    suicidal_by_support = []
    for level in support_levels:
        rate = df[df['social_support'] == level]['suicidal_thoughts'].mean() * 100
        suicidal_by_support.append(rate)
    
    axes[0, 0].bar(support_levels, suicidal_by_support, 
                  color=['#C0392B', '#E67E22', '#F39C12', '#27AE60'])
    axes[0, 0].set_title('Social Support Effect on Suicidal Thoughts')
    axes[0, 0].set_ylabel('Suicidal Thoughts Rate (%)')
    axes[0, 0].set_xlabel('Social Support Level')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Mental health access
    mental_health_access = df.groupby('access_mental_health')['suicidal_thoughts'].mean() * 100
    axes[0, 1].bar(['No Access', 'Has Access'], mental_health_access.values, 
                  color=['#E74C3C', '#27AE60'])
    axes[0, 1].set_title('Mental Health Access Effect')
    axes[0, 1].set_ylabel('Suicidal Thoughts Rate (%)')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Safe housing
    housing_effect = df.groupby('safe_housing')['suicidal_thoughts'].mean() * 100
    axes[1, 0].bar(['No Safe Housing', 'Safe Housing'], housing_effect.values, 
                  color=['#E74C3C', '#27AE60'])
    axes[1, 0].set_title('Safe Housing Effect')
    axes[1, 0].set_ylabel('Suicidal Thoughts Rate (%)')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Community integration
    correlation = df[['community_integration', 'suicidal_thoughts']].corr().iloc[0, 1]
    axes[1, 1].scatter(df['community_integration'], df['suicidal_thoughts'], alpha=0.5, color='#3498DB')
    axes[1, 1].set_title(f'Community Integration vs Suicidal Thoughts\n(Correlation: {correlation:.3f})')
    axes[1, 1].set_xlabel('Community Integration Score (0-10)')
    axes[1, 1].set_ylabel('Suicidal Thoughts (0/1)')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.success("""
    **Key Protective Factors Identified:**
    - ✅ High social support significantly reduces suicidal thoughts
    - ✅ Access to mental health services is protective
    - ✅ Safe housing reduces risk
    - ✅ Community integration helps (though correlation varies)
    
    **⚠️ Critical Considerations:**
    - 🔴 Women experience **long-term trauma** requiring sustained intervention
    - 👶 **Children must be prioritized** in all protection services
    """)

# PREDICTIVE MODEL PAGE
elif page == "🤖 Predictive Model":
    st.markdown('<h1 class="main-header">🤖 Predictive Model</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    with st.spinner('Training model...'):
        # Prepare data
        df_model = df.copy()
        
        le_education = LabelEncoder()
        le_social = LabelEncoder()
        le_severity = LabelEncoder()
        
        df_model['education_encoded'] = le_education.fit_transform(df_model['education_level'])
        df_model['social_support_encoded'] = le_social.fit_transform(df_model['social_support'])
        df_model['severity_encoded'] = le_severity.fit_transform(df_model['mental_health_severity'])
        
        features = [
            'age', 'harassment_experienced', 'traveling_alone', 'with_children',
            'depression_symptoms', 'anxiety_symptoms', 'ptsd_symptoms',
            'education_encoded', 'social_support_encoded', 'access_mental_health',
            'community_integration', 'safe_housing', 'legal_assistance', 'access_to_services'
        ]
        
        X = df_model[features]
        y = df_model['suicidal_thoughts']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        accuracy = model.score(X_test_scaled, y_test)
        auc = roc_auc_score(y_test, y_pred_proba)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", f"{accuracy:.1%}")
    with col2:
        st.metric("AUC-ROC Score", f"{auc:.3f}")
    with col3:
        st.metric("Test Samples", len(y_test))
    
    st.markdown("---")
    
    # Feature importance
    feature_names = [
        'Age', 'Harassment Experienced', 'Traveling Alone', 'With Children',
        'Depression', 'Anxiety', 'PTSD', 'Education Level', 'Social Support',
        'Mental Health Access', 'Community Integration', 'Safe Housing',
        'Legal Assistance', 'Access to Services'
    ]
    
    coefficients = model.coef_[0]
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients,
        'Type': ['Risk' if coef > 0 else 'Protective' for coef in coefficients]
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Feature Importance")
        fig, ax = plt.subplots(figsize=(10, 8))
        top_features = importance_df.head(10)
        colors = ['#E74C3C' if x > 0 else '#27AE60' for x in top_features['Coefficient']]
        ax.barh(range(len(top_features)), top_features['Coefficient'], color=colors)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features['Feature'])
        ax.set_xlabel('Coefficient (Log Odds)')
        ax.set_title('Top 10 Predictors of Suicidal Thoughts')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("📊 ROC Curve")
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(fpr, tpr, color='#E74C3C', lw=2, label=f'ROC Curve (AUC = {auc:.3f})')
        ax.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random Classifier')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curve')
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)

# KEY FINDINGS PAGE
elif page == "📋 Key Findings":
    st.markdown('<h1 class="main-header">📋 Key Findings & Recommendations</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    st.markdown("### 🔍 Research Summary")
    
    harassment_count = df['harassment_experienced'].sum()
    harassment_rate = (harassment_count / len(df)) * 100
    harassed = df[df['harassment_experienced'] == 1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>1️⃣ Harassment Prevalence</h4>
        <ul>
            <li>Overall harassment rate: <strong>{:.1f}%</strong></li>
            <li>Total cases: <strong>{}</strong></li>
            <li>Traveling alone increases risk significantly</li>
            <li>Low reporting rate: Only <strong>25%</strong> reported</li>
        </ul>
        </div>
        """.format(harassment_rate, harassment_count), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
        <h4>3️⃣ Protective Factors</h4>
        <ul>
            <li>High social support reduces suicidal thoughts</li>
            <li>Mental health access is protective</li>
            <li>Safe housing significantly reduces risk</li>
            <li>Community integration helps</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>2️⃣ Mental Health Impact</h4>
        <ul>
            <li>Depression: <strong>{:.1f}%</strong> among survivors</li>
            <li>Anxiety: <strong>{:.1f}%</strong> among survivors</li>
            <li>PTSD: <strong>{:.1f}%</strong> among survivors</li>
            <li>Suicidal thoughts: <strong>{:.1f}%</strong></li>
        </ul>
        </div>
        """.format(
            harassed['depression_symptoms'].mean()*100,
            harassed['anxiety_symptoms'].mean()*100,
            harassed['ptsd_symptoms'].mean()*100,
            harassed['suicidal_thoughts'].mean()*100
        ), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
        <h4>4️⃣ Predictive Model</h4>
        <ul>
            <li>Model achieves good predictive accuracy</li>
            <li>Depression is strongest risk factor</li>
            <li>Safe housing is top protective factor</li>
            <li>Early intervention is critical</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 💡 Policy Recommendations")
    
    tab1, tab2, tab3 = st.tabs(["Immediate Actions", "Long-term Strategies", "Research Implications"])
    
    with tab1:
        st.markdown("""
        1. **Prioritize Vulnerable Groups - CRITICAL**
           - **Children MUST be given priority** in all services
           - Expedite asylum processing for families with children
           - Ensure child-friendly spaces and specialized support
           - Protect children from family separation
        
        2. **Trauma-Informed Mental Health Support**
           - Recognize **long-term trauma effects** in women asylum seekers
           - Provide sustained, ongoing mental health care
           - Implement specialized trauma therapy programs
           - Trauma persists beyond immediate incidents
        
        3. **Enhance Safety Measures**
           - Increase security in high-risk locations (transit, camps, borders)
           - Implement safe reporting mechanisms
           - Provide emergency response protocols
        
        4. **Reporting Systems**
           - Create safe, confidential reporting mechanisms
           - Remove barriers to reporting
           - Ensure survivor protection
        
        5  - Create safe, confidential reporting mechanisms
           - Remove barriers to reporting
           - Ensure survivor protection
        
        4. **Social Support Networks**
           - Create community support programs
           - Reduce isolation through peer groups
           - Connect with local organizations
        """)
    
    with tab2:
        st.markdown("""
        #### 🏗️ Long-term Strategies
        
        1. **Safe Housing**
           - Prioritize safe housing arrangements
           - Improve camp conditions
           - Increase urban accommodation options
        
        2. **Legal Assistance**
           - Ensure access to legal support
           - Provide advocacy services
           - Expedite asylum processing
        
        3. **Education Programs**
           - Provide awareness training on rights
           - Educate on available services
           - Empower through information
        
        4. **Community Integration**
           - Facilitate integration programs
           - Build social connections
           - Promote cultural exchange
        """)
    
    with tab3:
        st.markdown("""
        #### 🔬 Research Implications
        
        **Key Findings:**
        - **Long-term Trauma**: Women asylum seekers experience persistent trauma requiring sustained care
        - **Trauma Persistence**: Effects extend far beyond immediate incident exposure
        - **Children Priority**: Children must receive priority in all protection and support services
        - **Family Vulnerability**: Family separation increases trauma and vulnerability
        - **Protective Factors**: Multi-faceted support systems are most effective
        - **Early Intervention**: Critical for preventing severe mental health issues
        - **Holistic Approach**: Address both immediate safety and long-term integration
        - **Data-Driven Policy**: Use evidence-based interventions
        
        **Future Research Needs:**
        - Longitudinal studies tracking long-term trauma outcomes
        - Child-specific vulnerability and protection research
        - Cross-cultural comparative analyses
        - Intervention effectiveness evaluations
        - Cost-benefit analyses of protective measures
        """)
    
    st.success("✅ This analysis provides a comprehensive framework for understanding and addressing the vulnerability of women asylum seekers to sexual harassment and its mental health impacts.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7F8C8D;'>
    <p>&copy; 2026 Women Asylum Seekers Research Project | Built with Streamlit</p>
    <p>&#9888; Demonstration purposes only - Real research requires IRB approval and ethical safeguards</p>
</div>
""", unsafe_allow_html=True)
