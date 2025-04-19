from django.http import JsonResponse
import joblib
import os
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Initialize model as None
model = None

try:
    # Try to load the fraud detection model
    model_path = os.path.join(os.path.dirname(__file__), '../../ml_models/fraud_model.joblib')
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logger.info("Fraud detection model loaded successfully")
    else:
        logger.warning("Fraud model file not found, using dummy model")
except Exception as e:
    logger.error(f"Error loading fraud model: {str(e)}")
    model = None

def detect_fraud(request):
    if request.method == 'POST':
        try:
            # Get input data from request
            input_data = request.POST.dict()
            
            # Preprocess input data
            features = preprocess_data(input_data)
            
            # If model is not loaded, use dummy implementation
            if model is None:
                return JsonResponse({
                    'is_fraud': False,
                    'probability': 0.1,
                    'status': 'success',
                    'warning': 'Using dummy model - real model not loaded'
                })
            
            # Make prediction
            prediction = model.predict([features])
            probability = model.predict_proba([features])[0][1]
            
            return JsonResponse({
                'is_fraud': bool(prediction[0]),
                'probability': float(probability),
                'status': 'success'
            })
        except Exception as e:
            logger.error(f"Error in fraud detection: {str(e)}")
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def preprocess_data(input_data):
    # Implement your preprocessing logic here
    features = np.array([
        float(input_data.get('amount', 0)),
        float(input_data.get('time_diff', 0)),
        float(input_data.get('location_mismatch', 0))
    ])
    return features
