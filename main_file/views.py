from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import pandas as pd
import pickle
from pathlib import Path
import subprocess
import sys
from .serializers import PredictionSerializer

MODEL_PATH = Path(settings.BASE_DIR) / "model_files" / "model.pkl"
bundle = None


def train_if_missing():
    if MODEL_PATH.exists():
        return
    script = Path(settings.BASE_DIR) / "train_model.py"
    subprocess.check_call([sys.executable, str(script)], cwd=str(settings.BASE_DIR))


def load_bundle():
    global bundle
    if bundle is not None:
        return bundle
    train_if_missing()
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. Run python train_model.py"
        )
    with open(MODEL_PATH, "rb") as file:
        loaded = pickle.load(file)
    if isinstance(loaded, dict) and "model" in loaded:
        bundle = loaded
    else:
        bundle = {"model": loaded, "features": None, "labels": ["Dropout", "Enrolled", "Graduate"]}
    return bundle


def format_predictions(raw, probabilities=None, labels=None):
    names = labels or ["Dropout", "Enrolled", "Graduate"]
    formatted = []
    for index, code in enumerate(raw):
        code = int(code)
        item = {
            "code": code,
            "label": names[code] if 0 <= code < len(names) else "Unknown",
        }
        if probabilities is not None:
            row = probabilities[index]
            item["confidence"] = round(float(max(row)), 3)
            if len(row) > 0:
                item["dropoutProbability"] = round(float(row[0]), 3)
        formatted.append(item)
    return formatted


@method_decorator(csrf_exempt, name="dispatch")
class PredictView(APIView):
    def get(self, request, format=None):
        try:
            load_bundle()
            return Response({"status": "ok", "model": str(MODEL_PATH.name)})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request, format=None):
        try:
            loaded = load_bundle()
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            payload = request.data
            many = isinstance(payload, list)
            serializer = PredictionSerializer(data=payload, many=many)

            if not serializer.is_valid():
                return Response(
                    {
                        "error": "Invalid prediction payload",
                        "details": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = serializer.validated_data
            df = pd.DataFrame(data if many else [data])
            features = loaded.get("features")
            if features:
                df = df.reindex(columns=features, fill_value=0)
            model = loaded["model"]
            predictions = model.predict(df)
            probabilities = model.predict_proba(df) if hasattr(model, "predict_proba") else None
            return Response(
                format_predictions(predictions, probabilities, loaded.get("labels")),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
