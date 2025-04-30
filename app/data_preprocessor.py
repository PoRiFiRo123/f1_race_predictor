import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(csv_path):
    df = pd.read_csv(csv_path)
    required_columns = ['Year', 'Circuit', 'Driver', 'RacePosition']
    df = df.dropna(subset=required_columns)

    le_circuit = LabelEncoder()
    le_driver = LabelEncoder()

    df['CircuitEncoded'] = le_circuit.fit_transform(df['Circuit'])
    df['DriverEncoded'] = le_driver.fit_transform(df['Driver'])

    X = df[['Year', 'CircuitEncoded', 'DriverEncoded']]
    y = df['RacePosition'].astype(int)

    print("Label Distribution:\n", y.value_counts().sort_index())
    return X, y, le_circuit, le_driver

if __name__ == "__main__":
    X, y, le_circuit, le_driver = preprocess_data('../data/raw_data.csv')
