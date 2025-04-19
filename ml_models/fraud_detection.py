import logging
from django.conf import settings
import os

logger = logging.getLogger(__name__)

class FraudDetector:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Try to load the trained model or use simple rules as fallback"""
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'fraud_model.joblib')
        try:
            import joblib
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Loaded trained fraud detection model")
            else:
                logger.warning("No trained model found, using rule-based fallback")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.warning("Using rule-based fallback for fraud detection")

    def predict(self, transaction_data):
        """Predict fraud probability using model or simple rules"""
        if self.model:
            try:
                import pandas as pd
                features = pd.DataFrame([transaction_data])
                return float(self.model.predict_proba(features)[0][1])
            except Exception as e:
                logger.error(f"Model prediction failed: {str(e)}")
                
        # Fallback rule-based detection
        amount = transaction_data.get('amount', 0)
        time_diff = transaction_data.get('time_diff', 0)
        location_mismatch = transaction_data.get('location_mismatch', 0)
        
        # Simple heuristic rules
        risk_score = 0
        if amount > 1000:
            risk_score += 0.3
        if time_diff < 30:
            risk_score += 0.2 
        if location_mismatch:
            risk_score += 0.5
            
        return min(1.0, max(0.0, risk_score))

def get_fraud_detector():
    """Singleton pattern to load detector once"""
    if not hasattr(settings, '_fraud_detector'):
        settings._fraud_detector = FraudDetector()
    return settings._fraud_detector
