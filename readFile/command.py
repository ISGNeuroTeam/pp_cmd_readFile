import pandas as pd
from pathlib import Path
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class ReadfileCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("filename", required=True, otl_type=OTLType.TEXT),
            Keyword("type", required=False, otl_type=OTLType.TEXT),
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        filename = self.get_arg("filename").value
        type = self.get_arg("type").value or filename.split('.')[-1]

        if 'storage' in self.config:
            storage = self.config['storage']['path']
        else:
            storage = '/opt/otp/lookups'
        full_file_path = Path(f'{storage}/{filename}')
        # check file exists
        if not full_file_path.exists():
            raise ValueError('File not exists')
        if type == 'json':
            df = pd.read_json(full_file_path, lines=True)
        elif type == 'parquet':
            df = pd.read_parquet(
                full_file_path, engine='pyarrow', use_pandas_metadata=True
            )
        elif type == 'csv':
            df = pd.read_csv(full_file_path)
        else:
            raise ValueError('Unknown type')
        return df
