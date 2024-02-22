from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pandas as pd
import pickle

MODEL_PATH = 'model_files/model.pkl'

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model(MODEL_PATH)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(APIView):
    def post(self, request, format=None):
        try:
            def convert_to_list_format(data):
                converted_data = {}
                for key, value in data.items():
                    converted_data[key] = [value]
                return converted_data
            df = pd.DataFrame(convert_to_list_format(request.data))
            predictions = model.predict(df)
            return Response({'predictions': predictions}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
