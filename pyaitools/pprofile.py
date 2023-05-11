import cProfile as cp
import pstats


def show_runtime(func:str, top=20, binary_path="restat.bin"):
    cp.run(func, binary_path)
    p = pstats.Stats(binary_path)
    p.sort_stats('time').print_stats(top)
