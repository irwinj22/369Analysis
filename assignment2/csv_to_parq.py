import polars as pl
import constants

# scan in the data from CSV 
lf = pl.scan_csv("../2022_place_canvas_history.csv")

# convert string time to timestamp
lf = lf.with_columns(
    pl.coalesce(
        pl.col("timestamp").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S%.f UTC", strict=False), 
        pl.col("timestamp").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S UTC", strict=False)
))

# write to parquet file
lf.collect(streaming=True).write_parquet(file="rplace.parquet", compression="snappy", row_group_size=constants.CHUNK_SIZE)