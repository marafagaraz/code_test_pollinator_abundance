"""
FastAPI application for the Pollinator Abundance Calculator.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from pollinator_abundance.handler import pollinator_abundance_calculation

app = FastAPI(
    title="Pollinator Abundance Calculator API",
    description="API for calculating pollinator abundance based on plantation, ROI, and CA IDs",
    version="1.0.0",
)

class PollinatorAbundanceResult(BaseModel):
    """Output model for the pollinator abundance calculation endpoint."""
    result_values: Dict[str, Dict[str, Optional[float]]]

    # Add other fields as needed

    class Config:
        # Allow arbitrary types
        arbitrary_types_allowed = True


class PollinatorAbundanceInput(BaseModel):
    """Input model for the pollinator abundance calculation endpoint."""
    plantation_id: int
    roi_id: int
    ca_id: int


@app.post("/calculate", response_model=PollinatorAbundanceResult)
async def calculate_pollinator_abundance(input_data: PollinatorAbundanceInput):
    """
    Calculate pollinator abundance for the given plantation, ROI, and CA.

    Args:
        input_data: The input parameters containing plantation_id, roi_id, and ca_id

    Returns:
        The calculated pollinator abundance result
    """
    try:
        result = pollinator_abundance_calculation(
            plantation_id=input_data.plantation_id,
            roi_id=input_data.roi_id,
            ca_id=input_data.ca_id
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating pollinator abundance: {str(e)}")
