import pyarrow.csv as pv
import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa
import polars as pl
import duckdb
import time
import sys

def validate_input(): 
    if len(sys.argv) != 3: 
        raise ValueError("Incorrect Number of Command Line Arguments. Expected 3, received: ", len(sys.argv))

    try: 
        time1 = pd.to_datetime(sys.argv[1], format="%Y-%m-%d %H")
    except: 
        raise ValueError("First Argument Should be Date String Formatted as YYYY-MM-DD HH, Recieved: ", sys.argv[1])

    try: 
        time2 =  pd.to_datetime(sys.argv[2], format="%Y-%m-%d %H")
    except: 
        raise ValueError("Second Argument Should be Date String Formatted as YYYY-MM-DD HH. Received: ", sys.argv[2])

    if time1 >= time2: 
        raise ValueError("End Hour Should be After Start Hour. Provided Start Hour: ", sys.argv[1], ". Provded End Hour: ", sys.argv[2])
    
    return time1, time2

def main():
    start_time = time.perf_counter_ns()

    time1, time2 = validate_input()

    # PART 1 - RANK COLORS BY DISTINCT USERS 
    print(duckdb.sql(f'''
    WITH grouped AS (                 
        SELECT pixel_color, count(DISTINCT user_id) AS "unique users"
        FROM 'rplace.parquet'
        WHERE timestamp BETWEEN '{time1}' and '{time2}'
        GROUP BY pixel_color
    )
    SELECT *
    FROM grouped
    ORDER BY "unique users" 
    ''').df())

    # PART 2 - CALCULATE AVERAGE SESSION LENGTH
    print(duckdb.sql(f'''
    WITH in_timeframe AS (
        SELECT user_id, timestamp
        FROM "rplace.parquet"
        WHERE timestamp BETWEEN '{time1}' and '{time2}'
        ORDER BY user_id, timestamp             
    ),
    lag_time AS (
        SELECT *, 
        COALESCE(timestamp - LAG(timestamp) OVER (PARTITION BY user_id), INTERVAL 0 HOUR) AS "time_diff"
        FROM in_timeframe
        ORDER BY user_id, timestamp
    ),
    start_sessions AS (
        SELECT *, 
        CASE 
            WHEN time_diff = INTERVAL 0 MINUTE THEN 1
            WHEN time_diff <= INTERVAL 15 MINUTE THEN 0
            WHEN time_diff > INTERVAL 15 MINUTE THEN 1
        END AS start_session
        FROM lag_time
    ), 
    grouped AS (
        SELECT *,
        SUM(CASE 
                WHEN start_session = 1 THEN 1 
                ELSE 0 
                END
        ) OVER (ORDER BY user_id, timestamp) AS "group_id" 
        FROM start_sessions
    ),
    session_times AS (
        SELECT group_id, epoch(max(timestamp) - min(timestamp)) AS "session_time_sec", count(*) AS "session_num"
        FROM grouped
        GROUP BY group_id
        HAVING session_num > 1
        ORDER BY group_id
    )
    SELECT avg(session_time_sec)
    FROM session_times
    ''').df())

    # PART 3 - PIXEL PLACEMENT PERCENTILES
    print(duckdb.sql(f'''
    WITH pixels AS (
        SELECT user_id, COUNT(*) AS "pixel_count"
        FROM 'rplace.parquet'
        WHERE timestamp BETWEEN '{time1}' and '{time2}'
        GROUP BY user_id
    )
    SELECT percentile_cont(0.01) WITHIN GROUP (ORDER BY pixel_count DESC) AS "99_percentile", 
    percentile_cont(0.10) WITHIN GROUP (ORDER BY pixel_count DESC) AS "90_percentile", 
    percentile_cont(0.25) WITHIN GROUP (ORDER BY pixel_count DESC) AS "75_percentile", 
    percentile_cont(0.50) WITHIN GROUP (ORDER BY pixel_count DESC) AS "50_percentile" 
    FROM pixels        
    ''').df())

    # PART 4 - COUNT FIRST-TIME USERS
    print(duckdb.sql(f'''
    WITH in_time_frame AS (
        SELECT * 
        FROM "rplace.parquet"
        WHERE timestamp BETWEEN '{time1}' and '{time2}'
    )
    SELECT count (DISTINCT user_id)
    FROM in_time_Frame
    WHERE user_id >= (
        SELECT min(user_id)
        FROM in_time_frame
    )
    ''').df()) 

    end_time = time.perf_counter_ns()
    elapsed_time = (end_time - start_time)

    print("**EXECUTION TIME:** ", round(elapsed_time / 1000000, 2), " milliseconds")

if __name__ == "__main__": 
    main()
