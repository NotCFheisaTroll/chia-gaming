import pytest
import random
from hsms.streamables.program import Program
from steprun import diag_run_clvm, compile_module_with_symbols

compile_module_with_symbols(['.'], 'smoke_test_deep_compare.clsp')
compare_program = Program.from_bytes(bytes.fromhex(open('smoke_test_deep_compare.clvm.hex').read()))

compile_module_with_symbols(['.'], 'smoke_test_sort.clsp')
sort_program = Program.from_bytes(bytes.fromhex(open('smoke_test_sort.clvm.hex').read()))

def test_smoke_compare():
    diag_run_clvm(compare_program, Program.to([]), 'smoke_test_deep_compare.sym')

def test_smoke_sort():
    for length in range(11): # 0-10 length
        for i in range(1 + (3 * length)): # A few orders each
            orig_list = [random.randint(0,100) for x in range(length)]
            sort_args = Program.to([orig_list])
            sorted_list = Program.to(sorted(orig_list))
            print(orig_list)
            sort_res = diag_run_clvm(sort_program, sort_args, 'smoke_test_sort.sym')
            print(sort_res,sorted_list)
            assert sort_res == sorted_list

if __name__ == '__main__':
    test_smoke_sort()
