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

## Deploy on Render (free)

1. Push this repo to GitHub (branch `develop`).
2. On [render.com](https://render.com) → **New → Blueprint** and connect `univast_ai`, **or** **New → Web Service** → the same repo.
3. If you create a Web Service manually:
   - Runtime: **Docker**
   - Branch: `develop`
   - Instance type: **Free**
   - Health check path: `/healthz`
4. Set environment variables:
   - `SECRET_KEY` — any long random string (Blueprint can generate it)
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `*`
   - `FRONTEND_URL` — your Vercel frontend origin, e.g. `https://univast-client.vercel.app`
5. After deploy, the public URL looks like `https://univast-ai.onrender.com`.
6. Point the frontend at it: `VITE_AI_URL=https://univast-ai.onrender.com/api/v4` (then rebuild the Vercel app).

Free instances sleep after 15 minutes idle. The first request after sleep can take 30–60 seconds.
