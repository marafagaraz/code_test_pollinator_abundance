import time
import pytest
import logging
import statistics
from typing import List

from pollinator_abundance.main import pollinator_abundance_calculation

# Get a logger for this test module
logger = logging.getLogger(__name__)


def measure_execution_time(func, iterations: int = 3) -> List[float]:
    """
    Measure the execution time of a function over multiple iterations.
    
    Args:
        func: The function to measure
        iterations: Number of times to run the function
        
    Returns:
        List of execution times in seconds
    """
    execution_times = []
    
    for i in range(iterations):
        start_time = time.time()
        func()
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        logger.info(f"Iteration {i+1}/{iterations}: {execution_time:.4f} seconds")
    
    return execution_times


def test_execution_time():
    """
    Test that the pollinator_abundance_calculation function executes within an acceptable time range.
    
    This test measures the execution time over multiple iterations and ensures that:
    1. The average execution time is below a maximum threshold
    2. The execution time is consistent (low standard deviation)
    """
    # Number of iterations to run
    iterations = 3
    
    # Maximum acceptable average execution time (in seconds)
    max_avg_time = 5.0
    
    # Maximum acceptable standard deviation (in seconds)
    max_std_dev = 1.0
    
    # Measure execution times
    execution_times = measure_execution_time(pollinator_abundance_calculation, iterations)
    
    # Calculate statistics
    avg_time = statistics.mean(execution_times)
    std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
    
    # Log the results
    logger.info(f"Average execution time: {avg_time:.4f} seconds")
    logger.info(f"Standard deviation: {std_dev:.4f} seconds")
    
    # Assert that the average execution time is below the threshold
    assert avg_time < max_avg_time, f"Average execution time ({avg_time:.4f}s) exceeds maximum ({max_avg_time:.4f}s)"
    
    # Assert that the execution time is consistent
    assert std_dev < max_std_dev, f"Execution time variation ({std_dev:.4f}s) exceeds maximum ({max_std_dev:.4f}s)"


if __name__ == "__main__":
    # This allows running the tests directly from this file
    pytest.main(["-xvs", __file__])
