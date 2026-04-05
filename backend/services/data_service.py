"""
Data Service - Handles data loading, processing, and caching
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional, Tuple
import json
import hashlib
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing datasets and data operations"""
    
    def __init__(self, data_path: str = "data/data_csv"):
        self.data_path = data_path
        self.cache: Dict[str, pd.DataFrame] = {}
        self.metadata: Dict[str, Dict] = {}
        self.load_dataset_metadata()
    
    def load_dataset_metadata(self):
        """Load metadata for all available datasets"""
        if not os.path.exists(self.data_path):
            logger.warning(f"Data path not found: {self.data_path}")
            return
        
        for file in os.listdir(self.data_path):
            if file.endswith('.csv'):
                file_path = os.path.join(self.data_path, file)
                try:
                    df = pd.read_csv(file_path, nrows=5)  # Read only first 5 rows for metadata
                    
                    self.metadata[file] = {
                        'name': file,
                        'size': os.path.getsize(file_path),
                        'rows': len(pd.read_csv(file_path)),
                        'columns': len(df.columns),
                        'column_names': df.columns.tolist(),
                        'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
                        'dtypes': df.dtypes.astype(str).to_dict()
                    }
                    logger.info(f"Loaded metadata for {file}")
                except Exception as e:
                    logger.error(f"Failed to load metadata for {file}: {str(e)}")
    
    def get_dataset(self, dataset_name: str, use_cache: bool = True) -> Optional[pd.DataFrame]:
        """Get a dataset by name with caching"""
        if use_cache and dataset_name in self.cache:
            return self.cache[dataset_name].copy()
        
        file_path = os.path.join(self.data_path, dataset_name)
        if not os.path.exists(file_path):
            return None
        
        try:
            df = pd.read_csv(file_path)
            if use_cache:
                self.cache[dataset_name] = df.copy()
            return df
        except Exception as e:
            logger.error(f"Failed to load dataset {dataset_name}: {str(e)}")
            return None
    
    def get_dataset_preview(self, dataset_name: str, rows: int = 10) -> Optional[Dict]:
        """Get preview of a dataset"""
        df = self.get_dataset(dataset_name)
        if df is None:
            return None
        
        return {
            'name': dataset_name,
            'preview': df.head(rows).to_dict(orient='records'),
            'columns': df.columns.tolist(),
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'metadata': self.metadata.get(dataset_name, {})
        }
    
    def get_dataset_statistics(self, dataset_name: str) -> Optional[Dict]:
        """Get statistical summary of a dataset"""
        df = self.get_dataset(dataset_name)
        if df is None:
            return None
        
        statistics = {}
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        for col in numeric_cols:
            statistics[col] = {
                'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                'median': float(df[col].median()) if not pd.isna(df[col].median()) else None,
                'std': float(df[col].std()) if not pd.isna(df[col].std()) else None,
                'min': float(df[col].min()) if not pd.isna(df[col].min()) else None,
                'max': float(df[col].max()) if not pd.isna(df[col].max()) else None,
                'missing': int(df[col].isnull().sum()),
                'missing_percentage': float(df[col].isnull().sum() / len(df) * 100)
            }
        
        return {
            'dataset': dataset_name,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': numeric_cols,
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'statistics': statistics,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        }
    
    def list_datasets(self) -> List[Dict]:
        """List all available datasets with their metadata"""
        datasets = []
        for name, metadata in self.metadata.items():
            datasets.append({
                'name': name,
                'rows': metadata.get('rows', 0),
                'columns': metadata.get('columns', 0),
                'size_mb': metadata.get('size', 0) / 1024 / 1024,
                'last_modified': metadata.get('last_modified', '')
            })
        return datasets
    
    def search_dataset(self, dataset_name: str, column: str, value: Any) -> Optional[List[Dict]]:
        """Search for records in a dataset"""
        df = self.get_dataset(dataset_name)
        if df is None or column not in df.columns:
            return None
        
        try:
            result = df[df[column] == value]
            return result.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return None
    
    def get_column_unique_values(self, dataset_name: str, column: str, limit: int = 50) -> Optional[List]:
        """Get unique values for a column"""
        df = self.get_dataset(dataset_name)
        if df is None or column not in df.columns:
            return None
        
        try:
            unique_values = df[column].dropna().unique().tolist()
            if len(unique_values) > limit:
                unique_values = unique_values[:limit]
            return unique_values
        except Exception as e:
            logger.error(f"Error getting unique values: {str(e)}")
            return None
    
    def clear_cache(self):
        """Clear the dataset cache"""
        self.cache.clear()
        logger.info("Dataset cache cleared")
    
    def get_cache_info(self) -> Dict:
        """Get information about cached datasets"""
        return {
            'cached_datasets': list(self.cache.keys()),
            'cache_size_mb': sum(df.memory_usage(deep=True).sum() for df in self.cache.values()) / 1024 / 1024,
            'cache_entries': len(self.cache)
        }