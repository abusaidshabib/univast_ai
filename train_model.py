from pathlib import Path
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

LABELS = ["Dropout", "Enrolled", "Graduate"]
BASE_DIR = Path(__file__).resolve().parent
DATASET = BASE_DIR / "model_files" / "dataset.csv"
MODEL_PATH = BASE_DIR / "model_files" / "model.pkl"


def encode_target(series):
    mapping = {name: index for index, name in enumerate(LABELS)}
    return series.map(lambda value: mapping.get(str(value).strip(), 1))


def train_and_save(model_path=MODEL_PATH, dataset_path=DATASET):
    df = pd.read_csv(dataset_path)
    if "target" not in df.columns:
        raise ValueError("dataset.csv must include a target column")
    features = [column for column in df.columns if column != "target"]
    x = df[features]
    y = encode_target(df["target"])
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(x_train, y_train)
    print(classification_report(y_test, model.predict(x_test), target_names=LABELS, zero_division=0))
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as file:
        pickle.dump({"model": model, "features": features, "labels": LABELS}, file)
    print(f"Saved {model_path}")
    return model_path


if __name__ == "__main__":
    train_and_save()
