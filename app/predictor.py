import joblib
import numpy as np

def predict_winner(year, circuit_name, driver_name):
    clf = joblib.load('./models/race_winner_model.pkl')
    le_circuit = joblib.load('./models/circuit_encoder.pkl')
    le_driver = joblib.load('./models/driver_encoder.pkl')

    try:
        circuit_encoded = le_circuit.transform([circuit_name])[0]
    except ValueError:
        return "❌ Unseen Circuit Name. Please check the input."

    try:
        driver_encoded = le_driver.transform([driver_name])[0]
    except ValueError:
        return "❌ Unseen Driver Name. Please check the input."

    X = np.array([[year, circuit_encoded, driver_encoded]])
    prediction = clf.predict(X)

    predicted_position = prediction[0]
    return f"🏁 Predicted Finishing Position: {predicted_position}"

if __name__ == "__main__":
    print(predict_winner(2023, 'Monza', 'VER'))
