import pandas as pd
from sqlalchemy import create_engine, inspect
from tqdm.auto import tqdm
import click


zone_lookup_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

zone_dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

def load_zones(engine, target_table):
    zones = pd.read_csv(zone_lookup_url, dtype=zone_dtype)

    if not inspect(engine).has_table(target_table):
        zones.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="fail",
            index=False,
        )

    zones.to_sql(
        name=target_table,
        con=engine,
        if_exists="append",
        index=False,
    )
    print("Inserted zones:", len(zones))



dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"]

chunksize = 100000

   
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of data')
@click.option('--month', default=1, type=int, help='Month of data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--zones-table', default='taxi_zones', help='Zones lookup table name')
@click.option('--chunksize', default=100000, type=int, help='Rows per chunk')


def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, zones_table, chunksize):

# pg_user = 'root'
# pg_pass = 'root'
# pg_host = 'pgdatabase'
# pg_port = 5432
# pg_db = 'ny_taxi'
# year = 2021
# month = 1
# target_table = 'yellow_taxi_trips'
# zones_table = 'taxi_zones'   

# def run():
    
    
# Read a sample of the data
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    load_zones(engine, zones_table)

    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
        )
    
    first = True
    
    for df_chunk in df_iter:
        if first:
        # Create table schema (no data)
            df_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
            )
            
        first = False
        print("Table created")
        
        
        df_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append"
        )
        
        print("Inserted:", len(df_chunk))
            
          
if __name__ == '__main__' : 
    run() 