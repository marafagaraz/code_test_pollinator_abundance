# Pollinator Abundance Calculator
This is my personal project for the pollinator test.

This project calculates pollinator abundance metrics for agricultural and natural landscapes.

## Prerequisites 

Please note that the pre-requisites are the same as: https://github.com/3BeeHiveTech/code_test_pollinator_abundance
This project is a copy of the original project with some modifications requested by the assignment.

Before you begin, ensure you have the following installed:

1.  **Python 3.11**: This project requires Python version 3.11.
2.  **uv**: This project uses `uv` for environment and package management. You can install it by following the instructions on the [official uv GitHub repository](https://github.com/astral-sh/uv). The `Makefile` will check if `uv` is available in your `PATH`.
3.  **System Dependencies**: Some Python packages (like `opencv-python`) might require system-level libraries (e.g., C++ compilers, image format libraries). Ensure these are installed if you encounter installation issues.

## Installation

The `Makefile` simplifies the setup process. To create the virtual environment and install the necessary dependencies (listed in `pyproject.toml`), including the project package in editable mode:

```bash
make venv
```

This command will:
1. Check if `uv` is installed.
2. Create a Python 3.11 virtual environment named `.venv` using `uv` if it doesn't already exist.
3. Install the project package (`pollinator_abundance`) in editable mode (`pip install -e .`) along with its dependencies using `uv`.

Key dependencies include: `numpy`, `Pillow`, `opencv-python`, `requests`, `upolygon`, `mypy`, `ruff`, `pytest`, `fastapi`, and `uvicorn`.

## Performance Profiling

The project includes a profiling script to identify performance bottlenecks in the code.

### Using profile_code.py

The `profile_code.py` script uses Python's built-in `cProfile` module to profile the execution of the pollinator abundance calculation function and identify performance bottlenecks.

#### Running the Profiler

To run the profiler and analyze performance bottlenecks:

```bash
uv run profile_code.py
```

#### What the Profiler Shows

The profiler output includes:

1. **Total execution time** of the pollinator abundance calculation
2. **Function call statistics** sorted by:
   - Cumulative time (functions that took the most total time, including time in subfunctions)
   - Total time (functions that took the most time in their own code, excluding subfunctions)
3. **Call counts** showing how many times each function was called
4. **Time per call** showing the average time spent in each function call

#### Example Output Analysis

In a recent profiling run, the main bottlenecks were identified as:

1. Thread lock acquisition (2.146s) - related to ThreadPoolExecutor
2. Image processing operations (resize, create_and_color_image)
3. KPI elements generation (1.225s)
4. Image merging operations (0.313s)
5. Numpy operations including nanmean calculations

Interventions: 

1. Thread Synchronization: The most significant bottleneck is thread synchronization, which takes over 2 seconds.
This is related to the ThreadPool execution in the handler.py file.
I tried to use ProcessPoolExecutor but the code didn't produce the expected results, this is probably caused by the overhead of process
creation and data transfer likely outweighs any parallelism benefits, especially if the individual bee calculations
aren't extremely CPU-intensive or if they need to share large numpy arrays. Due to time constraints, I focused my optimization efforts on this specific area. The optimized implementation can be 
found in the test_execution_time_optimized function within the test_performance.py file.

## Test Configuration

I've made the following changes to the pyproject.toml file:

- Added `pytest>=7.4.0` to the dependencies list
- Added a `[tool.pytest.ini_options]` section with:
  - `testpaths = ["tests"]` - Tells pytest to look for tests in the "tests" directory
  - `python_files = "test_*.py"` - Identifies test files that start with "test_"
  - `python_functions = "test_*"` - Identifies test functions that start with "test_"

### Logging Configuration

```toml
# Logging configuration
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
```

This configuration enables:
- Console logging during test execution (`log_cli = true`)
- INFO level logging by default (`log_cli_level = "INFO"`)
- Formatted log messages with timestamp, log level, message, filename, and line number
- ISO-formatted date and time

### Running Tests

To run the tests, you can use:

```bash
uv run pytest
```

Or to run with verbose output:

```bash
uv run pytest -v
```

### Output Stability Tests

I've created a set of tests that verify the output stability of the `pollinator_abundance_calculation` function:

#### Basic Stability Test (`test_pollinator_abundance_calculation_stability`)
- Captures the current output of the function
- Saves it as a reference
- Verifies that future runs produce exactly the same output

#### Code Change Simulation Test (`test_output_stability_with_code_change`)
- Simulates a code change by patching a function to return slightly modified values
- Verifies that the test can detect the change
- Demonstrates how the test can be used to ensure output stability

### Performance Tests

The project includes performance tests to ensure that the code executes efficiently and to detect performance regressions:

#### Execution Time Test (`test_execution_time`)
- Measures the execution time of the `pollinator_abundance_calculation` function over multiple iterations
- Ensures that the average execution time is below a maximum threshold
- Verifies that execution times are consistent (low standard deviation)

#### Running Performance Tests

To run the performance tests specifically:

```bash
uv run pytest tests/test_performance.py
```

## API Implementation

## Overview

This document explains the implementation of a FastAPI endpoint for the pollinator abundance calculation. The API allows users to calculate pollinator abundance by providing plantation, ROI, and CA IDs.

## Changes Made

### 1. Created FastAPI Endpoint

A new FastAPI application was created in `src/pollinator_abundance/api.py` with the following features:

- A POST endpoint at `/calculate` that accepts plantation_id, roi_id, and ca_id as input parameters
- A Pydantic model (`PollinatorAbundanceInput`) to validate the input data (this is in the same file, but it should be in a separate file)
- An output model (`PollinatorAbundanceResult`) to structure the response data (this is in the same file, but it should be in a separate file)
- Error handling to provide meaningful error messages

### 2. Modified the Main Calculation Function

The `pollinator_abundance_calculation` function in `src/pollinator_abundance/handler.py` was modified to:

- Accept parameters for plantation_id, roi_id, and ca_id instead of using hardcoded values
- Use these parameters in the ROI and CA dictionaries
- Maintain backward compatibility by providing default values for these parameters

### 3. Updated Main Script

The main script in `src/pollinator_abundance/main.py` was updated to reflect the new function signature while maintaining backward compatibility.

## How to Use the API

### Running the API Server

You can start the API server using the existing Makefile target:

```bash
make api
```

This will start the FastAPI server on http://localhost:8000.

### Making API Requests

You can make requests to the API using any HTTP client. Here's an example using Python Console:

```python
import requests

response = requests.post(
    "http://localhost:8000/calculate",
    json={"plantation_id": 9827, "roi_id": 284086, "ca_id": 284085}
)
result = response.json()
print(result)
```

### API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: http://localhost:8000/docs

## Future Improvements

Potential future improvements could include:

1. Adding authentication to the API
2. Adding more detailed validation for the input parameters
3. Adding more endpoints for other calculations or data retrieval
