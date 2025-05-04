import json
import pytest
import numpy as np
from pathlib import Path

from pollinator_abundance.main import pollinator_abundance_calculation


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session", autouse=True)
def ensure_test_data_dir(test_data_dir):
    """Ensure the test data directory exists."""
    test_data_dir.mkdir(exist_ok=True)
    return test_data_dir


def generate_reference_data(test_data_dir):
    """Generate reference data for testing."""
    # Run the function to get the output
    result = pollinator_abundance_calculation()

    # Extract key metrics from the result for comparison
    reference_data = {
        "ratio_x": result.get("ratio_x"),
        "ratio_y": result.get("ratio_y"),
        "width_km_ca": result.get("width_km_ca"),
        "height_km_ca": result.get("height_km_ca"),
        "alignment_point_x": result.get("alignment_point_x"),
        "alignment_point_y": result.get("alignment_point_y"),
    }

    # Add result values if they exist
    if "result_values" in result:
        result_values = result["result_values"]
        reference_data["result_values"] = {
            "CA": {k: v for k, v in result_values["CA"].items() if v is not None},
            "ROI": {k: v for k, v in result_values["ROI"].items() if v is not None},
            "Delta": {k: v for k, v in result_values["Delta"].items() if v is not None},
        }

    # Save the reference data to a file
    reference_file = test_data_dir / "pollinator_abundance_reference.json"
    with open(reference_file, "w") as f:
        json.dump(reference_data, f, indent=2)

    # Also save a hash of the full result for more detailed comparison if needed
    result_hash = hash(str(result))
    hash_file = test_data_dir / "pollinator_abundance_hash.txt"
    with open(hash_file, "w") as f:
        f.write(str(result_hash))

    return reference_data


def test_pollinator_abundance_calculation_stability(test_data_dir):
    """Test that pollinator_abundance_calculation output doesn't change."""
    reference_file = test_data_dir / "pollinator_abundance_reference.json"

    # Generate reference data if it doesn't exist
    if not reference_file.exists():
        reference_data = generate_reference_data(test_data_dir)
        pytest.skip("Reference data generated. Run the test again to compare.")

    # Load reference data
    with open(reference_file, "r") as f:
        reference_data = json.load(f)

    # Run the function to get the output
    result = pollinator_abundance_calculation()

    # Compare basic properties
    assert result["ratio_x"] == reference_data["ratio_x"], "ratio_x has changed"
    assert result["ratio_y"] == reference_data["ratio_y"], "ratio_y has changed"
    assert result["width_km_ca"] == reference_data["width_km_ca"], "width_km_ca has changed"
    assert result["height_km_ca"] == reference_data["height_km_ca"], "height_km_ca has changed"
    assert result["alignment_point_x"] == reference_data["alignment_point_x"], "alignment_point_x has changed"
    assert result["alignment_point_y"] == reference_data["alignment_point_y"], "alignment_point_y has changed"

    # Compare result values if they exist
    if "result_values" in reference_data and "result_values" in result:
        for area in ["CA", "ROI", "Delta"]:
            for key, value in reference_data["result_values"][area].items():
                assert np.isclose(result["result_values"][area][key], value, rtol=1e-5), f"{area}.{key} has changed"