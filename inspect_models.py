import joblib
import os

MODEL_PATHS = {
    "SMS": "models/best_sms_phishing_model.pkl",
    "EMAIL": "models/email_model.pkl",
    "URL": "models/url_model.pkl"
}

def inspect_model(name, path):
    print("\n" + "=" * 60)
    print(f"MODEL: {name}")
    print("=" * 60)

    if not os.path.exists(path):
        print("File tidak ditemukan:", path)
        return

    try:
        model = joblib.load(path)

        print("Class model:", type(model))
        print("Model classes:", getattr(model, "classes_", "Tidak tersedia"))
        print("Jumlah fitur:", getattr(model, "n_features_in_", "Tidak tersedia"))
        print("Nama fitur:", getattr(model, "feature_names_in_", "Tidak tersedia"))

        if hasattr(model, "steps"):
            print("\nPipeline steps:")
            for step_name, step in model.steps:
                print(f"- {step_name}: {type(step)}")

        if hasattr(model, "named_steps"):
            print("\nDetail pipeline:")
            for step_name, step in model.named_steps.items():
                print(f"- {step_name}: {type(step)}")

    except Exception as e:
        print("ERROR:", repr(e))


for name, path in MODEL_PATHS.items():
    inspect_model(name, path)
