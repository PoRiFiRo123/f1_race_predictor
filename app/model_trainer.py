import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from app.data_preprocessor import preprocess_data

def train_and_save_model():
    X, y, le_circuit, le_driver = preprocess_data('./data/raw_data.csv')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"✅ Accuracy: {acc:.3f}")
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix (Race Position Prediction)')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.show()

    joblib.dump(clf, './models/race_winner_model.pkl')
    joblib.dump(le_circuit, './models/circuit_encoder.pkl')
    joblib.dump(le_driver, './models/driver_encoder.pkl')

if __name__ == "__main__":
    train_and_save_model()
