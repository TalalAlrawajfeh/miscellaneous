import abc

import numpy as np


class Resampler(abc.ABC):
    @abc.abstractmethod
    def resample(self, sample):
        pass


class DefaultResampler(Resampler):
    def resample(self, sample):
        sample_copy = np.array(sample)
        np.random.shuffle(sample_copy)
        return np.expand_dims(sample_copy, axis=0)
