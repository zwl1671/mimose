import numpy as np

from ..utils.base import BaseModel
from ..utils.preprocessing import matrix_type_cast


class KNeighborClassifer(BaseModel):
    """K-th nearest neighbor classifier."""

    def __init__(self, n_neighbor, metric=2):
        """
        :@param n_neighbor: choose the n closest points.
        :type n: int.
        :@param metric: selection distance function, when metric=1 is
                        Manhattan-distance; metric=2 is Euclidean-distance.
        :type metric: int, value in {1, 2}.
        """

        self.n_neighbor = n_neighbor
        self.metric = metric


    @matrix_type_cast
    def fit(self, X, y):
        """fake fit function.

        :@param X: features matrix.
        :type X: the N x M dimension np.array or list.
        :@param y: class label vector.
        :type y: string or int.
        """
        self.X, self.y = X, y
        if self.n_neighbor > self.y.shape[0]:
            self.n_neighbor = self.y.shape[0]
        return self


    @matrix_type_cast
    def _predict(self, x):
        """Predict the label of single record.

        :@param x: single feature vector.
        :type x: np.array(N X 1 or 1 X N).
        :return: return label value.
        :rtype: string or int.
        """

        distance = np.linalg.norm(self.X - x, self.metric, axis=1)
        neighbors = np.argpartition(distance, self.n_neighbor-1)[:self.n_neighbor]
        neighbors_label = self.y[neighbors]
        labels, counts = np.unique(neighbors_label, return_counts=True)
        return labels[counts.argmax()]


    @matrix_type_cast
    def predict(self, X):
        """Predict the label of features matrix.

        :@param X: features matrix.
        :type X: np.array(M X N) or list(M X N).
        :return: the label of all features.
        :rtype: np.array(string | int).
        """

        return np.array([self._predict(x) for x in X])
