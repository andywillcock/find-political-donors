from unittest import TestCase
from src.political_donors_by_zip_and_date import *


bad_date_correct_array = np.array([['C00177436', '01312017', '384', '3', '998'],
                           ['C00384818', '01122017', '292', '2', '583']],dtype='|S10')
bad_zips_correct_array = np.array([['C00384818','02895','250','1','250'],
                          ['C00177436','30750','230','1','230'],
                         ['C00177436','04105','384','1','384'],
                        ['C00177436','04105','384','2','768'],
                        ['C00177436', '04105', '384', '3', '1268']],dtype='|S10')


class TestMedianvals_by_date(TestCase):
    def test_medianvals_by_date(self):
        test_array = medianvals_by_date('/Users/ATW/find_political_donors/insight_testsuite/tests/my_tests/bad_date.txt',None)
        for row in range(len(bad_date_correct_array)):
            for column in range(len(bad_date_correct_array[0])):
                self.assertTrue(test_array[row][column] == bad_date_correct_array[row][column])

    def test_medianvals_by_zip(self):
        test_array = medianvals_by_zip('/Users/ATW/find_political_donors/insight_testsuite/tests/my_tests/no_zip.txt',None)
        for row in range(len(bad_zips_correct_array)):
            for column in range(len(bad_zips_correct_array[0])):
                self.assertTrue(test_array[row][column]==bad_zips_correct_array[row][column])