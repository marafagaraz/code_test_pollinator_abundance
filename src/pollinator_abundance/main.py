import time
import sys
from pollinator_abundance.handler import pollinator_abundance_calculation


if __name__ == "__main__":
    # Example usage
    print("Starting pollinator abundance calculation...")
    start_time = time.time()
    # Using default values for plantation_id, roi_id, and ca_id
    result = pollinator_abundance_calculation()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Pollinator abundance calculation completed in {elapsed_time:.2f} seconds.")
    print("Result keys:", result.keys())
