from unittest import TestCase
import numpy as np
from find-political-donors.src.political_donors_by_zip_and_date import *

test_data = open('/Users/ATW/find-political-donors/insight_testsuite/tests/my_tests/no_zip.txt').readlines()
correct_array = np.array([['C00384818','02895','01122017','250','','250','1','250'],
                          ['C00177436','30750','01312017','230','','250','1','250'],
                         ['C00177436','04105','','01312017','384','','384','1','384'],
                        ['C00177436','04105','01312017','384','','384','2','768']])


class TestMedianvals_by_zip(TestCase):
    def test_medianvals_by_zip(self):
        test_arrau =
        np.testing.assert_almost_equal(test_array,correct_array)
