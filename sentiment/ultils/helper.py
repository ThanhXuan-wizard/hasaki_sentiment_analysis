import pandas as pd
import numpy as np

# Read product data into DataFrame
def read_csv(file_path):
    return pd.read_csv(file_path, encoding='utf-8')
