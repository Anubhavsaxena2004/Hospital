import logging
import joblib
import os
from django.conf import settings
import numpy as np

logger = logging.getLogger(__name__)

class ReadmissionPredictor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the trained model or use simple rules as fallback"""
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'readmission_model.joblib')
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Loaded trained readmission prediction model")
            else:
                logger.warning("No trained model found, using rule-based fallback")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.warning("Using rule-based fallback for readmission prediction")

    def predict(self, patient_data):
        """Predict readmission probability using model or simple rules"""
        if self.model:
            try:
                features = np.array([
                    patient_data['age'],
                    patient_data['previous_admissions'],
                    patient_data['chronic_conditions_count'],
                    patient_data['length_of_stay'],
                    patient_data['medication_count']
                ]).reshape(1, -1)
                return float(self.model.predict_proba(features)[0][1])
            except Exception as e:
                logger.error(f"Model prediction failed: {str(e)}")

        # Fallback rule-based prediction
        risk_score = 0.0
        
        # Age factor (older patients have higher risk)
        risk_score += min(0.3, patient_data['age'] / 100)
        
        # Previous admissions factor
        risk_score += min(0.3, patient_data['previous_admissions'] * 0.1)
        
        # Chronic conditions factor
        risk_score += min(0.2, patient_data['chronic_conditions_count'] * 0.1)
        
        # Length of stay factor (longer stays have higher risk)
        risk_score += min(0.2, patient_data['length_of_stay'] / 30)
        
        return min(1.0, max(0.0, risk_score))

def get_readmission_predictor():
    """Singleton pattern to load predictor once"""
    if not hasattr(settings, '_readmission_predictor'):
        settings._readmission_predictor = ReadmissionPredictor()
    return settings._readmission_predictor
