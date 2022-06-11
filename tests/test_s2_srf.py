import os
import unittest

import numpy as np
from numpy.testing import assert_array_equal

from colour import MultiSpectralDistributions
from sentinel_toolkit import S2Srf


class TestS2Srf(unittest.TestCase):
    _SRF_FILENAME = os.path.dirname(__file__) + "/test_data/s2a_srf.xlsx"

    _B1_NAME = "S2A_SR_AV_B1"
    _B1_INDEX = 0

    _B2_NAME = "S2A_SR_AV_B2"
    _B2_INDEX = 1

    _EXPECTED_BANDS_RESPONSES_DISTRIBUTION = MultiSpectralDistributions(
        {
            438: (0.810893815261278, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            439: (0.824198756004815, 0.010315428586995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            440: (0.854158107215052, 0.0300419331664615, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            441: (0.870790876711332, 0.0268758905675229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            442: (0.887310969404313, 0.0241431503861076, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            443: (0.926199242291321, 0.0202100642531871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        }
    )

    _WAVELENGTH_RANGE = (438, 439)

    _EXPECTED_ALL_BAND_NAMES = ["S2A_SR_AV_B1",
                                "S2A_SR_AV_B2",
                                "S2A_SR_AV_B3",
                                "S2A_SR_AV_B4",
                                "S2A_SR_AV_B5",
                                "S2A_SR_AV_B6",
                                "S2A_SR_AV_B7",
                                "S2A_SR_AV_B8",
                                "S2A_SR_AV_B8A",
                                "S2A_SR_AV_B9",
                                "S2A_SR_AV_B10",
                                "S2A_SR_AV_B11",
                                "S2A_SR_AV_B12"]

    def setUp(self):
        self.s2_srf = S2Srf(self._SRF_FILENAME)

    def test_get_wavelengths(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.wavelengths
        actual = self.s2_srf.get_wavelengths()
        assert_array_equal(expected, actual)

    def test_get_band_responses(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.range[:, self._B1_INDEX]
        actual = self.s2_srf.get_band_responses(self._B1_NAME)
        assert_array_equal(expected, actual)

    def test_get_band_masked_responses(self):
        wavelengths = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.wavelengths
        mask = (wavelengths >= self._WAVELENGTH_RANGE[0]) & (wavelengths <= self._WAVELENGTH_RANGE[1])
        values = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[mask]
        expected = values[:, self._B1_INDEX]
        actual = self.s2_srf.get_band_responses(self._B1_NAME, wavelength_range=self._WAVELENGTH_RANGE)
        assert_array_equal(expected, actual)

    def test_get_all_bands_responses(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values.T
        actual = self.s2_srf.get_bands_responses()
        assert_array_equal(expected, actual)

    def test_get_specific_bands_responses(self):
        b1_values = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[:, self._B1_INDEX]
        b2_values = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[:, self._B2_INDEX]
        expected = np.array([b1_values, b2_values])
        actual = self.s2_srf.get_bands_responses([self._B1_NAME, self._B2_NAME])
        assert_array_equal(expected, actual)

    def test_get_bands_masked_responses(self):
        wavelengths = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.wavelengths
        mask = (wavelengths >= self._WAVELENGTH_RANGE[0]) & (wavelengths <= self._WAVELENGTH_RANGE[1])
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[mask].T
        actual = self.s2_srf.get_bands_responses(wavelength_range=self._WAVELENGTH_RANGE)
        assert_array_equal(expected, actual)

    def test_get_all_bands_names(self):
        actual = self.s2_srf.get_all_band_names()
        assert_array_equal(self._EXPECTED_ALL_BAND_NAMES, actual)

    def test_get_bands_responses_distribution(self):
        actual = self.s2_srf.get_bands_responses_distribution()
        self.assertEqual(self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION, actual)


if __name__ == '__main__':
    unittest.main()
