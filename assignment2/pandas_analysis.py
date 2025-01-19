import time
import sys
import constants
import pandas as pd
import pyarrow.parquet as pq
from input_validation import validate_input

def main():
    start_time = time.perf_counter_ns()

    time1, time2 = validate_input()

    # read data from parquet file into pandas dataframe
    df = pd.read_parquet('../rplace.parquet', filters=[("timestamp", '>=', time1), ("timestamp", '<=', time2)])

    max_color = df.pixel_color.mode()
    max_coord = df.coordinate.mode()

    end_time = time.perf_counter_ns()
    elapsed_time = end_time - start_time
        
    print("**TIMEFRAME**: ", sys.argv[1], " to ", sys.argv[2])
    print("**EXECUTION TIME:** ", round(elapsed_time / 1000000, 2), " milliseconds")
    print("**MOST PLACED COLOR**: ", max_color)
    print("**MOST PLACED PIXEL LOCATION**:", max_coord)

if __name__ == "__main__":
    main()
