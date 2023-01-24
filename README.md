# pp_cmd_readFile
Postprocessing commands "readFile" and "writeFile"

Usage example:
`... | readFile books.csv type=csv`
`... | writeFile some_folder/books.csv type=csv`

Supported types:
- csv
- json
- parquet

## Deploy
1. Unpack archive in postprocessing commands directory
2. Configure `config.ini` with path to storage (default is `/opt/otp/shared_storage/persistent_storage`)

