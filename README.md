# pp_cmd_readFile
Postprocessing commands "readFile" and "writeFile"

Usage example:
`... | readFile books.csv type=csv`
`... | writeFile "some_folder/books.csv" type=csv`

Arguments:  
- type - keyword argument, file type. Supported types: csv, json, parquet
- storage - keyword argument, storage to save(read), default is lookups.
- private - keyword argument, save to (read from) user directory in storage. 

## Deploy
1. Unpack archive in postprocessing commands directory
2. Configure `config.ini` with path to storages (default is `loolups` in `/opt/otp/lookups`)
```
cp /opt/otp/python_computing_node/commands/readFile/config.example.ini /opt/otp/python_computing_node/commands/readFile/config.ini 
```
