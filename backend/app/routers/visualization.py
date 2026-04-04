"""
Data visualization endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
import os
from typing import List, Dict, Any
import json

router = APIRouter()

@router.get("/visualization/datasets")
async def get_datasets():
    """
    Get list of available datasets for visualization
    """
    try:
        data_path = "data/data_csv"
        if not os.path.exists(data_path):
            return {"datasets": [], "message": "No data folder found"}
        
        datasets = [f for f in os.listdir(data_path) if f.endswith('.csv')]
        return {"datasets": datasets, "count": len(datasets)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualization/data/{dataset_name}")
async def get_dataset_data(
    dataset_name: str,
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get dataset content for visualization
    """
    try:
        data_path = f"data/data_csv/{dataset_name}"
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = pd.read_csv(data_path)
        
        # Limit rows
        if len(df) > limit:
            df = df.head(limit)
        
        # Convert to dict for JSON response
        data = df.to_dict(orient='records')
        columns = df.columns.tolist()
        
        return {
            "success": True,
            "dataset": dataset_name,
            "rows": len(data),
            "columns": columns,
            "data": data,
            "shape": {"rows": df.shape[0], "columns": df.shape[1]}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualization/statistics/{dataset_name}")
async def get_dataset_statistics(dataset_name: str):
    """
    Get statistical summary of a dataset
    """
    try:
        data_path = f"data/data_csv/{dataset_name}"
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = pd.read_csv(data_path)
        
        # Generate statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        statistics = {}
        
        for col in numeric_cols:
            statistics[col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "missing": int(df[col].isnull().sum())
            }
        
        return {
            "success": True,
            "dataset": dataset_name,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "numeric_columns": numeric_cols,
            "statistics": statistics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))