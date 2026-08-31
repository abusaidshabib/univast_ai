from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pandas as pd
import pickle
from .serializers import PredictionSerializer
import os

MODEL_PATH = 'model_files/model.pkl'
model = None


def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. Place model.pkl in model_files/ before starting the predictor."
        )
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    return model


@method_decorator(csrf_exempt, name='dispatch')
class PredictView(APIView):
    def post(self, request, format=None):
        try:
            trained_model = get_model()
        except FileNotFoundError as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            payload = request.data
            many = isinstance(payload, list)
            serializer = PredictionSerializer(data=payload, many=many)

            if not serializer.is_valid():
                return Response(
                    {
                        'error': 'Invalid prediction payload',
                        'details': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = serializer.validated_data
            df = pd.DataFrame(data if many else [data])
            predictions = trained_model.predict(df)
            return Response(predictions.tolist(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
