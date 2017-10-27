from unittest import TestCase
from src.political_donors_by_zip_and_date import *

bad_zips_correct_array = np.array([['C00384818','02895','250','1','250'],
                          ['C00177436','30750','230','1','230'],
                         ['C00177436','04105','384','1','384'],
                        ['C00177436','04105','384','2','768'],
                        ['C00177436', '04105', '384', '3', '1268']],dtype='|S10')
bad_date_correct_array = np.array([['C00177436', '01312017', '384', '3', '998'],
                           ['C00384818', '01122017', '292', '2', '583']],dtype='|S10')
bad_cmte_correct_array = np.array([['C00384818','02895','250','1','250'],
                          ['C00177436','30750','230','1','230'],
                         ['C00177436','04105','384','1','384'],
                        ['C00177436','04105','384','2','768']],dtype='|S10')


class TestMedianvals_by_zip(TestCase):
    def test_medianvals_by_zip(self):
        def test_bad_zips(self):
            test_array = medianvals_by_date('/Users/ATW/find_political_donors/insight_testsuite/tests/my_tests/no_zip.txt', None)
            for row in range(len(bad_zips_correct_array)):
                for column in range(len(bad_zips_correct_array[0])):
                    self.assertTrue(test_array[row][column] == bad_zips_correct_array[row][column])

    def test_cmte_catcher(self):
        def test_bad_cmte(self):
            test_array = medianvals_by_date('/Users/ATW/find_political_donors/insight_testsuite/tests/my_tests/bad_date.txt',None)
            self.assertTrue(len(test_array) == len(bad_cmte_correct_array))

    def test_medianvals_by_date(self):
        def test_bad_dates(self):
            test_array = medianvals_by_date('/Users/ATW/find_political_donors/insight_testsuite/tests/my_tests/bad_date.txt',None)
            for row in range(len(bad_date_correct_array)):
                for column in range(len(bad_date_correct_array[0])):
                    self.assertTrue(test_array[row][column] == bad_date_correct_array[row][column])

