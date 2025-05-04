"""
Script to profile the pollinator abundance calculation code to identify performance bottlenecks.
"""
import cProfile
import pstats
import io
import time
from pstats import SortKey

from pollinator_abundance.handler import pollinator_abundance_calculation

def profile_function():
    """Profile the pollinator_abundance_calculation function and print the results."""
    # Create a Profile object
    profiler = cProfile.Profile()
    
    # Start profiling
    profiler.enable()
    
    # Run the function
    print("Starting pollinator abundance calculation...")
    start_time = time.time()
    result = pollinator_abundance_calculation()
    end_time = time.time()
    
    # Stop profiling
    profiler.disable()
    
    # Print total execution time
    elapsed_time = end_time - start_time
    print(f"Pollinator abundance calculation completed in {elapsed_time:.2f} seconds.")
    
    # Print profiling results
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(30)  # Print top 30 functions by cumulative time
    print(s.getvalue())
    
    # Also print results sorted by total time
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.TIME)
    ps.print_stats(30)  # Print top 30 functions by total time
    print("Results sorted by total time:")
    print(s.getvalue())

if __name__ == "__main__":
    profile_function()
