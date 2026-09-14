import copy, itertools, unittest
from deep_tests.upgrade_model import IncompatibleChange, assert_non_destructive_required_change, negotiate, read_with_version
class UpgradeStressMatrixTests(unittest.TestCase):
    def test_negotiation_permutations(self):
        orders=list(itertools.permutations((1,2,3)))
        for left in orders:
            for right in orders: self.assertEqual(negotiate(left,right),3)
    def test_projection_does_not_mutate_input(self):
        record={"version":3,"id":"edge","display_name":"name","status":"active","metadata":{"future":[1,2,3]},"future_field":{"x":True}}; before=copy.deepcopy(record)
        self.assertEqual(read_with_version(record,1),{"id":"edge","name":"name"}); self.assertEqual(record,before)
    def test_all_required_removal_combinations_fail(self):
        required={"id","display_name","status"}
        for count in range(1,4):
            for removed in itertools.combinations(required,count):
                with self.assertRaises(IncompatibleChange): assert_non_destructive_required_change(required,required-set(removed))
if __name__ == "__main__": unittest.main()
