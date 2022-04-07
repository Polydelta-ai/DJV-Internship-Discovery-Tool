import pandas as pd
import os
from datetime import datetime


from label_features import *


test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../etl/new_combined_source_data.csv"))

labelers = [name for name in dir() if 'LR_' in name]

labeled_df = label_features(
                        test_df, 
                        labelers,
                        {'job_title' : 0.60, 'full_job_description': 0.40},
                        "job_title", 
                        "job_title" )


labeled_df = test_df

file_timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M%p")
file_location = f"feature_vectors/Feature_Matrix-{file_timestamp}.csv"

labeled_df.to_csv(file_location)