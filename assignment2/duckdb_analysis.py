import time
import sys
import duckdb
from input_validation import validate_input

def main():
    start_time = time.perf_counter_ns()

    time1, time2 = validate_input()

    print(duckdb.sql(f'''
    SELECT pixel_color
    FROM'../rplace.parquet'
    WHERE timestamp BETWEEN '{time1}' and '{time2}'
    GROUP BY pixel_color 
    ORDER BY count(*) DESC
    LIMIT 1
    ''').df())

    print(duckdb.sql(f'''
    SELECT coordinate
    FROM'../rplace.parquet'
    WHERE timestamp BETWEEN '{time1}' and '{time2}'
    GROUP BY coordinate 
    ORDER BY count(*) DESC
    LIMIT 1
    ''').df())
    
    end_time = time.perf_counter_ns()
    elapsed_time = end_time - start_time
        
    print("**TIMEFRAME**: ", sys.argv[1], " to ", sys.argv[2])
    print("**EXECUTION TIME:** ", round(elapsed_time / 1000000, 2), " milliseconds")
    # print("**MOST PLACED COLOR**: ", mode_color)
    # print("**MOST PLACED PIXEL LOCATION**:", mode_coord)

if __name__ == "__main__":
    main()
