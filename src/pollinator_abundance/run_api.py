"""
Script to run the FastAPI server for the Pollinator Abundance Calculator.
"""
import uvicorn
from pollinator_abundance.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
