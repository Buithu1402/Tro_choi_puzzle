import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


class KNNModel:
    def __init__(self, filename):
        self.filename = filename
        self.model = self.train_knn()

    def load_data(self):
        # Ensure that the data is loaded correctly, separating values properly
        df = pd.read_csv(self.filename)

        # Extract puzzle state columns and move labels
        X = df.iloc[:, :-1].values  # Puzzle state
        y = df.iloc[:, -1].values  # Corresponding move

        return X, y

    def train_knn(self):
        X, y = self.load_data()

        # Create and train KNN model
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X, y)

        return knn

    def predict(self, puzzle_state):
        return self.model.predict([puzzle_state])[0]
