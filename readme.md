# UNIVAST dropout predictor

Django service on port **8001**. The admin student list posts academic and finance features to `POST /api/v4/predict/`.

## Run

```bash
python -m venv --system-site-packages .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-run.txt
.\.venv\Scripts\python.exe train_model.py
.\.venv\Scripts\python.exe manage.py runserver 8001
```

`train_model.py` fits a random forest on `model_files/dataset.csv` and writes `model_files/model.pkl`. If the pickle is missing, the API trains it on first request.

## Check

`GET http://localhost:8001/api/v4/predict/` should return `{ "status": "ok" }`.
