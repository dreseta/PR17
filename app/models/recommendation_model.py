import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

class SegmentRecommender:
    def __init__(self, segment_data: pd.DataFrame):
        self.df = segment_data.copy()
        self.features = ['distance', 'climb_score']  # add more if needed
        self.scaler = MinMaxScaler()
        self.model = NearestNeighbors(n_neighbors=5)
        self._prepare()

    def _prepare(self):
        self.df[self.features] = self.scaler.fit_transform(self.df[self.features])
        self.model.fit(self.df[self.features])

    def recommend(self, user_input: dict):
        # Transform user input
        user_vector = pd.DataFrame([user_input])[self.features]
        user_vector_scaled = self.scaler.transform(user_vector)
        distances, indices = self.model.kneighbors(user_vector_scaled)
        return self.df.iloc[indices[0]]
