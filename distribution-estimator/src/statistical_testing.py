import abc

import numpy as np
from scipy.stats import chisquare, kstest

from src.distribution import Distribution, DiscreteDistribution, ContinuousDistribution


class GoodnessOfFitTest(abc.ABC):
    @abc.abstractmethod
    def test(self, distribution: Distribution, observed_data: np.ndarray):
        pass


class DiscreteDistributionGoodnessOfFitTest(GoodnessOfFitTest):
    @abc.abstractmethod
    def test(self, distribution: DiscreteDistribution, observed_data: np.ndarray):
        pass


class ContinuousDistributionGoodnessOfFitTest(GoodnessOfFitTest):
    @abc.abstractmethod
    def test(self, distribution: ContinuousDistribution, observed_data: np.ndarray):
        pass


class ChiSquareTest(DiscreteDistributionGoodnessOfFitTest):
    def test(self,
             distribution: DiscreteDistribution,
             observed_data: np.ndarray):
        unique, observed_counts = np.unique(observed_data, return_counts=True)
        expected_counts = np.sum(observed_counts) * distribution.pmf(unique)
        result = chisquare(observed_counts, expected_counts)
        return {
            'statistic': result.statistic,
            'p_value': result.pvalue
        }

    def __str__(self):
        return 'Chi-Square Test'


class KolmogorovSmirnovTest(ContinuousDistributionGoodnessOfFitTest):
    def test(self,
             distribution: ContinuousDistribution,
             observed_data: np.ndarray):
        result = kstest(observed_data, distribution.cdf)
        return {
            'statistic': result.statistic,
            'p_value': result.pvalue
        }

    def __str__(self):
        return 'Kolmogorov-Smirnov Test'
