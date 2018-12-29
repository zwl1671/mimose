import numpy as np
from ..utils.abc_models import linearModel


class lassoRegression(linearModel):
    """Lasso regression model."""

    def __init__(self, n_iter=1000, alpha=0.5, threshold=0.1):
        """
        :param n_iter: number of algorithm iterations.
        :type n_iter: int.
        :param alpha: regularization coefficient.
        :type alpha: alpha in [0, 1].
        :param threshold: stop iteration condition.
        :type threshold: float number and threshold > 0.
        """
        super().__init__()
        self.n_iter = n_iter
        self.alpha = alpha
        self.threshold = threshold

    def fit(self, X, y):
        self.coef = self.coordinate_descent(X, y)
        return self

    def coordinate_descent(self, X, y):
        """Get lasso regression coefficients.

        :param X: features matrix.
        :type X: the n x m dimension np.array.
        :param y: real value vector.
        :type y: the n dimension column vector.
        :return: parameters of the lasso regression model.
        :rtype: the t dimension np.array.
        """
        self.scaler.fit(X)
        X = self.scaler(X)
        y = y.reshape(-1, 1)
        X_ = np.c_[np.ones(X.shape[0]), X]
        coef = np.zeros((X_.shape[1], 1))

        while self.n_iter:
            z = np.sum(X_ * X_, axis=0)
            _ = np.zeros((X_.shape[1], 1))
            for k in range(X_.shape[1]):
                w_k = coef[k]
                coef[k] = 0
                p_k = X_[:, k] @ (y - X_ @ coef)
                if p_k < self.alpha / 2:
                    w_k = (p_k + self.alpha / 2) / z[k]
                elif -self.alpha / 2 <= p_k <= self.alpha / 2:
                    w_k = 0
                else:
                    w_k = (p_k - self.alpha / 2) / z[k]
                _[k] = w_k
                coef[k] = w_k
            if np.linalg.norm(coef - _) < self.threshold:
                break
            self.n_iter -= 1

        return coef