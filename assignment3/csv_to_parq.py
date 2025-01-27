import pyarrow.csv as pv
import pyarrow.parquet as pq
import pyarrow as pa
import polars as pl

csv_file = "../2022_place_canvas_history.csv"
parquet_file = "HAHA_BREAK"

DATESTRING_FORMAT = "%Y-%m-%d %H:%M:%S"
BLOCK_SIZE = 75_000_000

read_options = pv.ReadOptions(block_size=BLOCK_SIZE)
csv_reader = pv.open_csv(csv_file, read_options=read_options)

parquet_writer = None
num_times = 0

id_dict = {}
id_count = 0

# TODO: just apply a function -- will this take too long? 
def add_id_to_dict(id):
    global id_count
    if id not in id_dict:
        id_dict[id] = id_count
        id_count += 1
    return id_dict[id]

try:
    for record_batch in csv_reader:
        '''if num_times == 1:
            break
        num_times += 1'''
        print(f"Processing batch with {record_batch.num_rows} rows...")

        df = pl.from_arrow(record_batch)

        df = df.with_columns(
            pl.col("timestamp")
            .str.replace(r" UTC$", "")  
            .str.strptime(
                pl.Datetime, 
                format="%Y-%m-%d %H:%M:%S%.f",
                strict=False
            )
            .alias("timestamp")
        )

        df = (
            df.filter(
                pl.col("coordinate").str.count_matches(",") == 1
            )
            .with_columns(
                pl.col("coordinate")
                .str.split_exact(",", 1)
                .struct.field("field_0")
                .cast(pl.Int64)
                .alias("x"),
                pl.col("coordinate")
                .str.split_exact(",", 1)
                .struct.field("field_1")
                .cast(pl.Int64)
                .alias("y"),
                pl.col("user_id").map_elements(lambda x: add_id_to_dict(x), return_dtype=pl.Int64)
            )
            .drop("coordinate")
        )

        # print(df.head(n=40))

        table = df.to_arrow()

        if parquet_writer is None:
            parquet_writer = pq.ParquetWriter(
                parquet_file, 
                schema=table.schema, 
                compression="zstd"
            )
        parquet_writer.write_table(table)

finally:
    if parquet_writer:
        parquet_writer.close()

print(f"Successfully converted {csv_file} to {parquet_file}")