import streamlit as st
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

class CloudStorage:
    def __init__(self):
        self.data_dir = Path("local_storage")
        self.data_dir.mkdir(exist_ok=True)

    def upload_dataframe(self, df, user_id, dataset_name):
        """Save DataFrame locally"""
        try:
            user_dir = self.data_dir / user_id
            user_dir.mkdir(exist_ok=True)
            file_name = f"{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            full_path = user_dir / file_name
            df.to_csv(full_path, index=False)
            return True, str(full_path)
        except Exception as e:
            return False, str(e)

    def get_user_datasets(self, user_id):
        """Get list of local datasets for a user"""
        try:
            user_dir = self.data_dir / user_id
            if not user_dir.exists():
                return []
            return [str(f.relative_to(self.data_dir)) for f in user_dir.glob("*.csv")]
        except Exception:
            return []

    def load_dataset(self, file_name):
        """Load a local dataset"""
        try:
            full_path = self.data_dir / file_name
            return pd.read_csv(full_path)
        except Exception:
            return None

    def delete_dataset(self, file_name):
        """Delete a local dataset"""
        try:
            full_path = self.data_dir / file_name
            full_path.unlink()
            return True
        except Exception:
            return False 