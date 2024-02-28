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

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def create_list_data(list_data):
    csv_file_path = os.path.join('model_files', 'dataset.csv')
    df = pd.read_csv(csv_file_path)
    features = df.columns.tolist()
    random_values = {}
    for feature in features:
        random_value = df[feature].sample(n=1).values[0]
        random_values[feature] = random_value
    for data in list_data:
        for feature in features:
            if feature not in data and feature != 'target':
                data[feature] = random_values[feature]
    if 'target' in list_data[-1]:
        del list_data[-1]['target']

    return list_data

model = load_model(MODEL_PATH)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(APIView):
    def post(self, request, format=None):
        try:
            if isinstance(request.data, list):
                serializer = PredictionSerializer(data=request.data, many=True)
            else:
                serializer = PredictionSerializer(data=request.data)

            if serializer.is_valid():
                print("done")
                data = serializer.validated_data
                all_predictions = []
                if isinstance(data, list):
                    for item in data:
                        predictions = model.predict(pd.DataFrame([item]))
                        all_predictions.extend(predictions)
                        print("Predictions:", predictions)
                else:
                    predictions = model.predict(pd.DataFrame([data]))
                    all_predictions.extend(predictions)
                    print("Predictions:", predictions)
                return Response({'predictions': all_predictions}, status=status.HTTP_200_OK)
            else:
                def convert_to_dataframe(data):
                    return pd.DataFrame(data)
                list_data = create_list_data(request.data)
                df = convert_to_dataframe(list_data)
                predictions = model.predict(df)
                return Response({'prediction': predictions}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
