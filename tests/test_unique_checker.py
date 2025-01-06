from util import unique_checker

class TestUniqueChecker:
    def test_initialization(self):
        items = {1, 2, 3}
        checker = unique_checker(items)
        assert checker.unique == {1, 2, 3}
    
    def test_context_manager(self):
        items = {1, 2, 3}
        with unique_checker(items) as checker:
            assert checker.unique == {1, 2, 3}
        assert checker.unique == set()
    
    def test_check_method(self):
        with unique_checker({1, 2, 3}) as checker:
            assert checker.check(4) == True
            assert checker.check(1) == False
    
    def test_add_method(self):
        with unique_checker({1, 2, 3}) as checker:
            checker.add(4)
            assert 4 in checker.unique
            assert checker.check(4) == False
    
