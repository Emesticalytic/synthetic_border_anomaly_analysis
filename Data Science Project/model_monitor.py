"""
UK Border Anomaly Detection - Model Monitoring System
Tracks model performance, data drift, and system health
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    """Monitor ML model performance and data drift"""
    
    def __init__(self, model_name: str, baseline_data: pd.DataFrame):
        """
        Initialize model monitor
        
        Args:
            model_name: Name of the model being monitored
            baseline_data: Training/baseline data for comparison
        """
        self.model_name = model_name
        self.baseline_data = baseline_data
        self.baseline_stats = self._calculate_baseline_stats()
        self.alerts = []
        
        logger.info(f"Initialized monitor for {model_name}")
    
    def _calculate_baseline_stats(self) -> Dict:
        """Calculate baseline statistics for numerical features"""
        stats_dict = {}
        
        numerical_cols = self.baseline_data.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            stats_dict[col] = {
                'mean': self.baseline_data[col].mean(),
                'std': self.baseline_data[col].std(),
                'min': self.baseline_data[col].min(),
                'max': self.baseline_data[col].max(),
                'q25': self.baseline_data[col].quantile(0.25),
                'q75': self.baseline_data[col].quantile(0.75)
            }
        
        return stats_dict
    
    def detect_data_drift(self, new_data: pd.DataFrame, threshold: float = 0.05) -> Dict:
        """
        Detect statistical drift in feature distributions
        
        Args:
            new_data: New production data
            threshold: P-value threshold for KS test
            
        Returns:
            Dictionary with drift detection results
        """
        drift_results = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'total_features': 0,
            'drifted_features': [],
            'drift_scores': {},
            'has_significant_drift': False
        }
        
        numerical_cols = [col for col in self.baseline_stats.keys() if col in new_data.columns]
        drift_results['total_features'] = len(numerical_cols)
        
        for col in numerical_cols:
            # Kolmogorov-Smirnov test
            ks_statistic, p_value = stats.ks_2samp(
                self.baseline_data[col].dropna(),
                new_data[col].dropna()
            )
            
            drift_results['drift_scores'][col] = {
                'ks_statistic': float(ks_statistic),
                'p_value': float(p_value),
                'drifted': p_value < threshold
            }
            
            if p_value < threshold:
                drift_results['drifted_features'].append(col)
                drift_results['has_significant_drift'] = True
                
                alert = {
                    'type': 'DATA_DRIFT',
                    'severity': 'HIGH' if p_value < 0.01 else 'MEDIUM',
                    'feature': col,
                    'ks_statistic': float(ks_statistic),
                    'p_value': float(p_value),
                    'timestamp': datetime.now().isoformat()
                }
                self.alerts.append(alert)
                logger.warning(f"Data drift detected in {col}: KS={ks_statistic:.4f}, p={p_value:.4f}")
        
        return drift_results
    
    def check_feature_ranges(self, new_data: pd.DataFrame, tolerance: float = 3.0) -> Dict:
        """
        Check if new data features are within expected ranges
        
        Args:
            new_data: New production data
            tolerance: Number of standard deviations to allow
            
        Returns:
            Dictionary with range check results
        """
        range_results = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'out_of_range_features': [],
            'outlier_counts': {}
        }
        
        for col, stats_info in self.baseline_stats.items():
            if col not in new_data.columns:
                continue
            
            mean = stats_info['mean']
            std = stats_info['std']
            
            # Check for values outside tolerance range
            lower_bound = mean - (tolerance * std)
            upper_bound = mean + (tolerance * std)
            
            outliers = new_data[
                (new_data[col] < lower_bound) | (new_data[col] > upper_bound)
            ]
            
            outlier_count = len(outliers)
            outlier_pct = (outlier_count / len(new_data)) * 100
            
            range_results['outlier_counts'][col] = {
                'count': outlier_count,
                'percentage': float(outlier_pct),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
            
            if outlier_pct > 5:  # More than 5% outliers
                range_results['out_of_range_features'].append(col)
                
                alert = {
                    'type': 'FEATURE_RANGE',
                    'severity': 'HIGH' if outlier_pct > 10 else 'MEDIUM',
                    'feature': col,
                    'outlier_percentage': float(outlier_pct),
                    'timestamp': datetime.now().isoformat()
                }
                self.alerts.append(alert)
                logger.warning(f"Feature range alert for {col}: {outlier_pct:.2f}% outliers")
        
        return range_results
    
    def monitor_predictions(self, predictions: np.ndarray, scores: np.ndarray) -> Dict:
        """
        Monitor prediction distribution and anomaly scores
        
        Args:
            predictions: Binary predictions (0/1)
            scores: Anomaly scores or probabilities
            
        Returns:
            Dictionary with prediction monitoring results
        """
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'total_predictions': len(predictions),
            'anomaly_rate': float(np.mean(predictions)),
            'score_stats': {
                'mean': float(np.mean(scores)),
                'std': float(np.std(scores)),
                'min': float(np.min(scores)),
                'max': float(np.max(scores)),
                'q25': float(np.percentile(scores, 25)),
                'q50': float(np.percentile(scores, 50)),
                'q75': float(np.percentile(scores, 75))
            }
        }
        
        # Check for unusual anomaly rates
        expected_anomaly_rate = 0.05  # 5% baseline
        if monitoring_results['anomaly_rate'] > expected_anomaly_rate * 2:
            alert = {
                'type': 'ANOMALY_RATE',
                'severity': 'HIGH',
                'current_rate': float(monitoring_results['anomaly_rate']),
                'expected_rate': expected_anomaly_rate,
                'timestamp': datetime.now().isoformat()
            }
            self.alerts.append(alert)
            logger.warning(f"Unusual anomaly rate: {monitoring_results['anomaly_rate']:.2%}")
        
        return monitoring_results
    
    def generate_report(self, output_path: str = None) -> Dict:
        """
        Generate monitoring report
        
        Args:
            output_path: Optional path to save report JSON
            
        Returns:
            Complete monitoring report
        """
        report = {
            'model_name': self.model_name,
            'report_timestamp': datetime.now().isoformat(),
            'total_alerts': len(self.alerts),
            'alerts': self.alerts,
            'alert_summary': {
                'critical': len([a for a in self.alerts if a.get('severity') == 'HIGH']),
                'warnings': len([a for a in self.alerts if a.get('severity') == 'MEDIUM']),
                'info': len([a for a in self.alerts if a.get('severity') == 'LOW'])
            }
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Monitoring report saved to {output_path}")
        
        return report
    
    def clear_alerts(self):
        """Clear all accumulated alerts"""
        self.alerts = []
        logger.info("Alerts cleared")


def create_monitoring_dashboard_data(monitor: ModelMonitor, 
                                      new_data: pd.DataFrame,
                                      predictions: np.ndarray,
                                      scores: np.ndarray) -> Dict:
    """
    Create comprehensive monitoring data for dashboard
    
    Args:
        monitor: ModelMonitor instance
        new_data: Production data
        predictions: Model predictions
        scores: Anomaly scores
        
    Returns:
        Dictionary with all monitoring metrics
    """
    drift_results = monitor.detect_data_drift(new_data)
    range_results = monitor.check_feature_ranges(new_data)
    prediction_results = monitor.monitor_predictions(predictions, scores)
    
    dashboard_data = {
        'timestamp': datetime.now().isoformat(),
        'model': monitor.model_name,
        'data_drift': drift_results,
        'feature_ranges': range_results,
        'predictions': prediction_results,
        'alerts': monitor.alerts,
        'system_health': {
            'status': 'HEALTHY' if not drift_results['has_significant_drift'] else 'WARNING',
            'drift_detected': drift_results['has_significant_drift'],
            'alert_count': len(monitor.alerts)
        }
    }
    
    return dashboard_data


if __name__ == "__main__":
    print("🔍 Model Monitoring System")
    print("=" * 50)
    print("\nThis module provides:")
    print("✓ Data drift detection using KS tests")
    print("✓ Feature range monitoring")
    print("✓ Prediction distribution tracking")
    print("✓ Alert generation and reporting")
    print("\nUsage:")
    print("  from model_monitor import ModelMonitor")
    print("  monitor = ModelMonitor('ensemble', training_data)")
    print("  results = monitor.detect_data_drift(production_data)")
