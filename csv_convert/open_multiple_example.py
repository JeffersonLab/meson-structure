import pandas as pd
import glob

def concat_csvs_with_unique_events(files):
    """Load and concatenate CSV files with globally unique event IDs"""

    dfs = []
    offset = 0

    for file in files:
        df = pd.read_csv(file)
        df['evt'] = df['evt'] + offset
        offset = df['evt'].max() + 1
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# Usage
lambda_df = concat_csvs_with_unique_events(sorted(glob.glob("mcpart_lambda*.csv")))
dis_df = concat_csvs_with_unique_events(sorted(glob.glob("dis_parameters*.csv")))

# Join them
joined = lambda_df.merge(dis_df, on='evt', how='inner')