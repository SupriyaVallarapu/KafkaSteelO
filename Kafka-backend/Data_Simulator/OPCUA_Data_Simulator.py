from opcua import ua, Server
import time
import pandas as pd
from datetime import datetime

def get_parquet_file_path():
    # Get file path from user
    file_path = input("Enter the full path of the parquet file: ")
    return file_path

# Load the parquet file into a pandas DataFrame
while True:
    try:
        df = pd.read_parquet(get_parquet_file_path())
        break
    except FileNotFoundError:
        print("File not found. Please try again.")
    except pd.errors.ParquetError:
        print("Invalid parquet file. Please try again.")

# Convert the 'Time' column to datetime if it's not already
df['Time'] = pd.to_datetime(df['Time'])

# Setup OPC-UA Server
server = Server()
url = "opc.tcp://localhost:4840"
server.set_endpoint(url)

# Setup our own namespace
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

# Get Objects node, this is where we should put our custom stuff
objects = server.get_objects_node()

# Add a timestamp variable
myobj = objects.add_object(addspace, "MyParquetObject")
timestamp_variable = myobj.add_variable(addspace, "Time", datetime.utcnow(), ua.VariantType.DateTime)
timestamp_variable.set_writable()

# A basic mapping from pandas to OPC UA types
dtype_map = {
    'float64': ua.VariantType.Double,
    'float32': ua.VariantType.Double,
    'int64': ua.VariantType.Int64,
    'bool': ua.VariantType.Boolean,
    'datetime64[ns]': ua.VariantType.DateTime,
    'object': ua.VariantType.Int64,
    # Add other mappings as needed
}

# Generate the OPC UA variables from the DataFrame columns
opcua_variables = {}
for column in df.columns:
    if column != 'Time':  # We're already handling 'Time' separately
        variable_name = column
        # Get the data type of the column from the DataFrame
        pandas_dtype = df[column].dtype
    
        # Map the pandas data type to the corresponding OPC UA data type
        opcua_dtype = dtype_map[str(pandas_dtype)]
    
        # Add the variable to the OPC UA server
        opcua_variables[variable_name] = myobj.add_variable(addspace, variable_name, df[column][0], opcua_dtype)

        # Set the variable to be writable by clients
        opcua_variables[variable_name].set_writable()

# Starting!
server.start()

try:
    while True:
        for _, row in df.iterrows():
            timestamp = row['Time']
            for column, variable in opcua_variables.items():
                value = row[column]
                data_value = ua.DataValue(ua.Variant(value))
                data_value.SourceTimestamp = timestamp
                variable.set_data_value(data_value)

                # Print variable name, value and timestamp
                # print(f'Timestamp: {row["Time"]}, Variable: {column}, Value: {value}')

        time.sleep(3)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close connection, remove subscriptions, etc
    server.stop()