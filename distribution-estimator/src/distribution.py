import abc

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gamma
from scipy import stats

EPSILON = 1e-9


class Distribution(abc.ABC):
    @abc.abstractmethod
    def fit(self, samples: np.ndarray):
        pass


class DiscreteDistribution(Distribution):
    @abc.abstractmethod
    def pmf(self, x):
        pass


class ContinuousDistribution(Distribution):
    @abc.abstractmethod
    def pdf(self, x):
        pass

    @abc.abstractmethod
    def cdf(self, x):
        pass


class DiscreteUniform(DiscreteDistribution):
    def __init__(self, a=None, b=None):
        if not isinstance(a, int) and a is not None:
            raise ValueError('Invalid value for a.')
        if not isinstance(b, int) and b is not None:
            raise ValueError('Invalid value for b.')
        if a is not None and b is not None and a > b:
            raise ValueError('Invalid values for a and b.')

        self.a = a
        self.b = b

    def fit(self, samples: np.ndarray):
        a_estimators = []
        b_estimators = []

        if samples.shape[0] == 0:
            raise ValueError('Empty samples given.')

        for i in range(samples.shape[0]):
            sample = samples[i]
            if sample.shape[0] == 0:
                raise ValueError('Empty sample given.')

            if np.any([not sample[j].is_integer() for j in range(sample.shape[0])]):
                raise ValueError('Values of the Discrete Uniform distribution should be integers.')

            a_estimators.append(np.min(sample))
            b_estimators.append(np.max(sample))

        self.a = int(np.round(np.mean(a_estimators)))
        self.b = int(np.round(np.mean(b_estimators)))
        return True

    def pmf(self, x: np.ndarray):
        if self.a is None or self.a is None:
            raise Exception('The model parameters are empty.')
        return np.ones(x.shape) / (self.b - self.a + 1)

    def __str__(self):
        return f'DiscreteUniform(a = {self.a}, b = {self.b})'


class Zipfian(DiscreteDistribution):
    def __init__(self, n=None, s=None):
        if n is not None and not isinstance(n, int):
            raise ValueError('Invalid value for n.')
        if n is not None and n <= 0:
            raise ValueError('Invalid value for n.')
        if s is not None and s <= 0:
            raise ValueError('Invalid value for s.')
        self.n = n
        self.s = s

    def fit(self, samples: np.ndarray):
        if samples.shape[0] == 0:
            raise ValueError('Empty samples given.')

        if np.any(samples <= 0):
            raise ValueError('Values of the Zipfian distribution should be strictly positive integers.')

        s_estimators = []
        for i in range(samples.shape[0]):
            sample = samples[i]
            if sample.shape[0] == 0:
                raise ValueError('Empty sample given.')

            if np.any([not sample[j].is_integer() for j in range(sample.shape[0])]):
                raise ValueError('Values of the Zipfian distribution should be strictly positive integers.')

            unique_values = np.unique(sample)
            self.n = int(unique_values.shape[0])
            sample_size = sample.shape[0]

            def objective(s):
                term1 = s * np.sum(np.log(sample))
                term2 = sample_size * np.log(np.sum(1 / np.power(np.arange(1, self.n + 1), s)))
                return term1 + term2

            best = minimize_scalar(objective, bounds=(0.01, 100.0))
            s_estimators.append(best.x)

        self.s = float(np.mean(s_estimators))
        return True

    def pmf(self, x: np.ndarray):
        if self.n is None or self.s is None:
            raise Exception('The model parameters are empty.')

        return np.power(x, -self.s) / np.sum(np.power(np.arange(1, self.n + 1), -self.s))

    def __str__(self):
        return f'Zipfian(s = {self.s}, n = {self.n})'


class Beta(ContinuousDistribution):
    def __init__(self, alpha=None, beta=None):
        if alpha is not None and alpha <= 0:
            raise ValueError('Invalid value for alpha.')
        if beta is not None and beta <= 0:
            raise ValueError('Invalid value for alpha.')
        self.alpha = alpha
        self.beta = beta

    def fit(self, samples: np.ndarray):
        if samples.shape[0] == 0:
            raise ValueError('Empty samples given.')

        if np.any(samples < 0.0) or np.any(samples > 1.0):
            raise ValueError('Values of the Beta distribution must be between 0 and 1.')

        alpha_estimators = []
        beta_estimators = []

        for i in range(samples.shape[0]):
            sample = samples[i]
            if sample.shape[0] == 0:
                raise ValueError('Empty sample given.')

            variance = np.var(sample)
            if variance < EPSILON:
                return False

            mean = np.mean(sample)
            common_factor = ((mean * (1 - mean)) / variance - 1)

            alpha_estimators.append(mean * common_factor)
            beta_estimators.append((1 - mean) * common_factor)

        self.alpha = float(np.mean(alpha_estimators))
        self.beta = float(np.mean(beta_estimators))
        return True

    def pdf(self, x: np.ndarray):
        if self.alpha is None or self.beta is None:
            raise Exception('The model parameters are empty.')
        if np.any(x < 0.0) or np.any(x > 1.0):
            raise ValueError('Values of the Beta distribution must be between 0 and 1.')

        c = gamma(self.alpha + self.beta) / (gamma(self.alpha) * gamma(self.beta))
        return c * np.power(x, self.alpha - 1) * np.power(1.0 - x, self.beta - 1)

    def cdf(self, x: np.ndarray):
        return stats.beta.cdf(x, a=self.alpha, b=self.beta)

    def __str__(self):
        return f'Beta(alpha = {self.alpha}, beta = {self.beta})'
