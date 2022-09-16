import sys
from typing import Callable

import numpy as np

from sampling import DefaultResampler, Resampler
from src.distribution import Zipfian, DiscreteUniform, Beta, Distribution, DiscreteDistribution, ContinuousDistribution
from src.generic_utils import parse_sample_file
from statistical_testing import ChiSquareTest, KolmogorovSmirnovTest, GoodnessOfFitTest, \
    ContinuousDistributionGoodnessOfFitTest, DiscreteDistributionGoodnessOfFitTest


def fit_and_test_distributions(fitting_samples: np.ndarray,
                               test_sample: np.ndarray,
                               distributions: list[Distribution],
                               goodness_of_fit_test: GoodnessOfFitTest,
                               test_comparator: Callable[[dict, dict], bool]):
    best_test_result = None
    best_distribution = None
    for distribution in distributions:
        try:
            if distribution.fit(fitting_samples):
                test_result = goodness_of_fit_test.test(distribution, test_sample)
                if best_test_result is None or test_comparator(test_result, best_test_result):
                    best_distribution = distribution
                    best_test_result = test_result
        except ValueError:
            pass
    return best_distribution, best_test_result


def print_fit_result(distribution: Distribution,
                     goodness_of_fit_test: GoodnessOfFitTest,
                     distribution_test_result: dict,
                     distribution_type: str):
    if distribution is not None and distribution_test_result is not None:
        print(f'Best {distribution_type} distribution fit result:')
        print(distribution)
        print(f'according to the test: {goodness_of_fit_test}')
        print(f'statistic: {distribution_test_result["statistic"]}\n'
              f'p-value: {distribution_test_result["p_value"]}')
    else:
        print(f'No suitable {distribution_type} distribution was found for the given data.')


def distribution_fitting_and_testing_defaults_provider() -> tuple[Resampler,
                                                                  list[ContinuousDistribution],
                                                                  list[DiscreteDistribution],
                                                                  ContinuousDistributionGoodnessOfFitTest,
                                                                  DiscreteDistributionGoodnessOfFitTest,
                                                                  Callable[[dict, dict], bool]]:
    resampler = DefaultResampler()
    supported_discrete_distributions = [
        DiscreteUniform(),
        Zipfian()
    ]
    supported_continuous_distributions = [
        Beta()
    ]
    discrete_distribution_goodness_of_fit_test = ChiSquareTest()
    continuous_distribution_goodness_of_fit_test = KolmogorovSmirnovTest()

    return (resampler,
            supported_continuous_distributions,
            supported_discrete_distributions,
            continuous_distribution_goodness_of_fit_test,
            discrete_distribution_goodness_of_fit_test,
            lambda test1, test2: test1['p_value'] > test2['p_value'])


def estimate_distribution(sample_file: str,
                          file_parser: Callable[[str], list[int | float]],
                          distribution_fitting_and_testing_provider: Callable[[],
                                                                              tuple[Resampler,
                                                                                    list[ContinuousDistribution],
                                                                                    list[DiscreteDistribution],
                                                                                    ContinuousDistributionGoodnessOfFitTest,
                                                                                    DiscreteDistributionGoodnessOfFitTest,
                                                                                    Callable[[dict, dict], bool]]]):
    (resampler,
     supported_continuous_distributions,
     supported_discrete_distributions,
     continuous_distribution_goodness_of_fit_test,
     discrete_distribution_goodness_of_fit_test,
     test_comparator) = distribution_fitting_and_testing_provider()

    try:
        parsed_sample = file_parser(sample_file)
        if len(parsed_sample) == 0:
            print('File is either empty or contains invalid data.')
            return
    except FileNotFoundError:
        print(f'File: {sample_file} not found.')
        return

    sample = np.array(parsed_sample)
    samples = resampler.resample(sample)

    distribution, distribution_test_result = fit_and_test_distributions(samples,
                                                                        sample,
                                                                        supported_discrete_distributions,
                                                                        discrete_distribution_goodness_of_fit_test,
                                                                        test_comparator)

    print_fit_result(distribution,
                     discrete_distribution_goodness_of_fit_test,
                     distribution_test_result,
                     'discrete')

    distribution, distribution_test_result = fit_and_test_distributions(samples,
                                                                        sample,
                                                                        supported_continuous_distributions,
                                                                        continuous_distribution_goodness_of_fit_test,
                                                                        test_comparator)

    print_fit_result(distribution,
                     continuous_distribution_goodness_of_fit_test,
                     distribution_test_result,
                     'continuous')


if __name__ == '__main__':
    estimate_distribution(sys.argv[1],
                          parse_sample_file,
                          distribution_fitting_and_testing_defaults_provider)
