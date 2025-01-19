# this is where I am going to do the polars analysis and what not and all of that jazz
import time
import sys
import constants
import polars as pl
from input_validation import validate_input

def main():
    start_time = time.perf_counter_ns()

    time1, time2 = validate_input()

    # read data from parquet file into pandas dataframe
    #df = pd.read_parquet('../rplace.parquet', filters=[("timestamp", '>=', time1), ("timestamp", '<=', time2)])
    df = pl.read_parquet("../rplace.parquet", columns=constants.FIELDS).filter((pl.col("timestamp") >= time1) & (pl.col("timestamp") <= time2))
    # print(df.head(10))

    mode_color = df["pixel_color"].mode()
    mode_coord = df["coordinate"].mode()

    end_time = time.perf_counter_ns()
    elapsed_time = end_time - start_time
        
    print("**TIMEFRAME**: ", sys.argv[1], " to ", sys.argv[2])
    print("**EXECUTION TIME:** ", round(elapsed_time / 1000000, 2), " milliseconds")
    print("**MOST PLACED COLOR**: ", mode_color)
    print("**MOST PLACED PIXEL LOCATION**:", mode_coord)

if __name__ == "__main__":
    main()
