# ABOUTME: Reference solution for the Qwasar "My Linear Regression" project (normal equation + gradient descent).
# ABOUTME: Scratch exploration to size the workshop; the teaching version lives in the workshop notebooks.
import numpy as np

np.random.seed(42)


def h(x, theta):
    """Linear hypothesis: one prediction per row of x. x already carries the bias column."""
    return x.dot(theta)


def mean_squared_error(y_predicted, y_label):
    return float(np.mean((np.asarray(y_predicted) - np.asarray(y_label)) ** 2))


def bias_column(X):
    """Prepend x0 = 1 so theta0 becomes an ordinary weight."""
    X = np.asarray(X)
    return np.hstack([np.ones((X.shape[0], 1)), X])


class LeastSquaresRegression:
    def __init__(self):
        self.theta_ = None

    def fit(self, X, y):
        # Normal equation: theta = (X^T X)^-1 X^T y. pinv instead of inv so a singular X^T X still answers.
        self.theta_ = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(y)
        return self

    def predict(self, X):
        return h(X, self.theta_)


class GradientDescentOptimizer:
    def __init__(self, f, fprime, start, learning_rate=0.1):
        self.f_ = f
        self.fprime_ = fprime
        self.current_ = np.asarray(start, dtype=float)
        self.learning_rate_ = learning_rate
        self.history_ = [self.current_.copy()]

    def step(self):
        # Walk downhill: against the gradient, scaled by the learning rate.
        self.current_ = self.current_ - self.learning_rate_ * self.fprime_(self.current_)
        self.history_.append(self.current_.copy())

    def optimize(self, iterations=100):
        for _ in range(iterations):
            self.step()
        return self.current_

    def getCurrentValue(self):
        return self.current_

    def print_result(self):
        print("Best theta found is " + str(self.current_))
        print("Value of f at this theta: f(theta) = " + str(self.f_(self.current_)))
        print("Value of f prime at this theta: f'(theta) = " + str(self.fprime_(self.current_)))


# f(x) = 3 + (x - [2, 6])^T (x - [2, 6]): a bowl whose minimum sits at [2, 6] with value 3.
TARGET = np.array([2.0, 6.0])


def f(x):
    d = np.asarray(x, dtype=float) - TARGET
    return float(3 + d.dot(d))


def fprime(x):
    return 2 * (np.asarray(x, dtype=float) - TARGET)


if __name__ == "__main__":
    X = 4 * np.random.rand(100, 1)
    y = 10 + 2 * X + np.random.randn(100, 1)
    X_new = bias_column(X)

    model = LeastSquaresRegression().fit(X_new, y)
    print("theta (normal equation):", model.theta_.ravel(), "<- generated with 10 and 2")
    print("MSE:", round(mean_squared_error(model.predict(X_new), y), 4))

    print("\n-- gradient descent on f, learning rates --")
    for lr in (0.01, 0.1, 0.5, 0.9, 1.0, 1.1):
        g = GradientDescentOptimizer(f, fprime, np.array([0.0, 0.0]), lr)
        g.optimize(50)
        print(f"  lr={lr:<4} -> theta={np.round(g.getCurrentValue(), 3)}  f={f(g.getCurrentValue()):.4f}")

    print("\n-- gradient descent fitting the regression itself --")
    m = len(X_new)

    def mse_cost(theta):
        return mean_squared_error(h(X_new, theta.reshape(-1, 1)), y)

    def mse_grad(theta):
        theta = theta.reshape(-1, 1)
        return (2 / m * X_new.T.dot(h(X_new, theta) - y)).ravel()

    for lr in (0.01, 0.1, 0.2):
        g = GradientDescentOptimizer(mse_cost, mse_grad, np.zeros(2), lr)
        g.optimize(1000)
        print(f"  lr={lr:<5} -> theta={np.round(g.getCurrentValue(), 3)}  MSE={mse_cost(g.getCurrentValue()):.4f}")

    # Scaling: the same descent on a feature 1000x larger, to show why convergence stalls without scaling.
    X_big = bias_column(4000 * np.random.rand(100, 1))

    def grad_big(theta):
        theta = theta.reshape(-1, 1)
        return (2 / m * X_big.T.dot(h(X_big, theta) - y)).ravel()

    g = GradientDescentOptimizer(lambda t: mean_squared_error(h(X_big, t.reshape(-1, 1)), y), grad_big, np.zeros(2), 0.1)
    g.optimize(50)
    print("\nunscaled feature (x1000), lr=0.1 ->", np.round(g.getCurrentValue(), 2), "(diverges)")
