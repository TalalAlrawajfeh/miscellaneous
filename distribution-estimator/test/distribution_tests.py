import unittest

import numpy as np

from src.distribution import DiscreteUniform, Zipfian, Beta


class DiscreteUniformTests(unittest.TestCase):
    def test_discrete_uniform_init_with_valid_parameters1(self):
        self.assertIsInstance(DiscreteUniform(1, 3), DiscreteUniform)

    def test_discrete_uniform_init_with_valid_parameters2(self):
        self.assertIsInstance(DiscreteUniform(-1, 10), DiscreteUniform)

    def test_discrete_uniform_init_with_invalid_parameters1(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform(3, 1))

    def test_discrete_uniform_init_with_invalid_parameters2(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform(1.5, 3))

    def test_discrete_uniform_init_with_invalid_parameters3(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform(2, 5.6))

    def test_discrete_uniform_fit_with_valid_sample_values(self):
        discrete_uniform = DiscreteUniform()
        fit_result = discrete_uniform.fit(np.array([[2, 2, 3, 3]]))
        self.assertTrue(fit_result)
        self.assertEqual(2, discrete_uniform.a)
        self.assertEqual(3, discrete_uniform.b)

    def test_discrete_uniform_fit_with_valid_samples_values(self):
        discrete_uniform = DiscreteUniform()
        fit_result = discrete_uniform.fit(np.array([[2, 2, 3, 3], [1, 1, 4, 4], [1, 2, 3, 4]]))
        self.assertTrue(fit_result)
        self.assertEqual(1, discrete_uniform.a)
        self.assertEqual(4, discrete_uniform.b)

    def test_discrete_uniform_fit_with_invalid_sample_values1(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform().fit(np.array([[1.5, 2, 2, 3, 3]])))

    def test_discrete_uniform_fit_with_invalid_sample_values2(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform().fit(np.array([[]])))

    def test_discrete_uniform_fit_with_invalid_sample_values3(self):
        self.assertRaises(ValueError, lambda: DiscreteUniform().fit(np.array([])))

    def test_discrete_uniform_pmf_with_empty_parameters(self):
        self.assertRaises(Exception, lambda: DiscreteUniform().pmf(np.array(1)))

    def test_discrete_uniform_pmf_with_valid_parameters(self):
        discrete_uniform = DiscreteUniform(1, 10)
        self.assertAlmostEqual(1 / 10, discrete_uniform.pmf(np.array(5)))
        self.assertAlmostEqual(1 / 10, discrete_uniform.pmf(np.array(7)))


class ZipfianTests(unittest.TestCase):
    def test_zipfian_init_with_valid_parameters1(self):
        self.assertIsInstance(Zipfian(3, 0.5), Zipfian)

    def test_zipfian_init_with_valid_parameters2(self):
        self.assertIsInstance(Zipfian(2, 5.0), Zipfian)

    def test_zipfian_init_with_invalid_parameters1(self):
        self.assertRaises(ValueError, lambda: Zipfian(-3, 1))

    def test_zipfian_init_with_invalid_parameters2(self):
        self.assertRaises(ValueError, lambda: Zipfian(1.5, 3))

    def test_zipfian_init_with_invalid_parameters3(self):
        self.assertRaises(ValueError, lambda: Zipfian(0, 2))

    def test_zipfian_init_with_invalid_parameters4(self):
        self.assertRaises(ValueError, lambda: Zipfian(1, -1.5))

    def test_zipfian_fit_with_valid_sample_values(self):
        zipfian = Zipfian()
        fit_result = zipfian.fit(np.array([[1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4]]))
        self.assertTrue(fit_result)
        self.assertEqual(4, zipfian.n)
        self.assertLess(abs(1.31325 - zipfian.s), 1e-3)

    def test_zipfian_fit_with_valid_samples_values(self):
        zipfian = Zipfian()
        fit_result = zipfian.fit(np.array([[1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4],
                                           [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4]]))
        self.assertTrue(fit_result)
        self.assertEqual(4, zipfian.n)
        self.assertLess(abs(1.31325 - zipfian.s), 0.1)

    def test_zipfian_fit_with_invalid_sample_values1(self):
        self.assertRaises(ValueError, lambda: Zipfian().fit(np.array([[1.5, 2, 2, 3, 3]])))

    def test_zipfian_fit_with_invalid_sample_values2(self):
        self.assertRaises(ValueError, lambda: Zipfian().fit(np.array([[]])))

    def test_zipfian_fit_with_invalid_sample_values3(self):
        self.assertRaises(ValueError, lambda: Zipfian().fit(np.array([])))

    def test_zipfian_pmf_with_empty_parameters(self):
        self.assertRaises(Exception, lambda: Zipfian().pmf(np.array(10)))

    def test_zipfian_pmf_with_valid_parameters(self):
        self.assertLess(abs(0.025810 - Zipfian(10, 2.0).pmf(np.array(5))), 1e-3)


class BetaTests(unittest.TestCase):
    def test_beta_init_with_valid_parameters1(self):
        self.assertIsInstance(Beta(3, 0.5), Beta)

    def test_beta_init_with_valid_parameters2(self):
        self.assertIsInstance(Beta(5.0, 2), Beta)

    def test_beta_init_with_invalid_parameters1(self):
        self.assertRaises(ValueError, lambda: Beta(-3, 1))

    def test_beta_init_with_invalid_parameters2(self):
        self.assertRaises(ValueError, lambda: Beta(1, -1.5))

    def test_beta_fit_with_valid_sample_values(self):
        beta = Beta()
        fit_result = beta.fit(np.array([[0.98628268, 0.19492956, 0.66751278, 0.9671618, 0.12858784,
                                         0.09519136, 0.53246531, 0.4043925, 0.54584022, 0.64959293]]))
        self.assertTrue(fit_result)
        self.assertLess(abs(1 - beta.alpha), 0.2)
        self.assertLess(abs(1 - beta.beta), 0.2)

    def test_beta_fit_with_valid_samples_values(self):
        beta = Beta()
        fit_result = beta.fit(np.array([[0.85497183, 0.36853287, 0.67301374, 0.87876569, 0.99579135,
                                         0.381166, 0.91232281, 0.30419054, 0.09536585, 0.65673097],
                                        [0.85310439, 0.42415401, 0.61761029, 0.70964134, 0.12058527,
                                         0.13129141, 0.67940086, 0.56411184, 0.11423515, 0.19126808]]))
        self.assertTrue(fit_result)
        self.assertLess(abs(1 - beta.alpha), 0.2)
        self.assertLess(abs(1 - beta.beta), 0.2)

    def test_beta_fit_with_invalid_sample_values1(self):
        self.assertRaises(ValueError, lambda: Beta().fit(np.array([[1.5, 2, 2, 3, 3]])))

    def test_beta_fit_with_invalid_sample_values2(self):
        self.assertRaises(ValueError, lambda: Beta().fit(np.array([[]])))

    def test_beta_fit_with_invalid_sample_values3(self):
        self.assertRaises(ValueError, lambda: Beta().fit(np.array([])))

    def test_beta_pdf_with_empty_parameters(self):
        self.assertRaises(Exception, lambda: Beta().pdf(np.array(10)))

    def test_beta_pmf_with_valid_parameters(self):
        self.assertLess(abs(0.37158912 - Beta(3, 7).pdf(np.array(0.6))), 1e-3)


if __name__ == '__main__':
    unittest.main()
