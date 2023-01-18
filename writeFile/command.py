import pandas as pd
from pathlib import Path

from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class WritefileCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("filename", required=True, otl_type=OTLType.TEXT),
            Keyword("type", required=False, otl_type=OTLType.TEXT),
        ],
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        filename = self.get_arg("filename").value
        type = self.get_arg("type").value or filename.split('.')[-1]

        if 'storage' in self.config:
            storage = self.config['storage']['path']
        else:
            storage = '/opt/otp/shared_storage/persistent_storage'
        Path(storage).mkdir(exist_ok=True, parents=True)
        full_file_path = Path(f'{storage}/{filename}')

        if df is None:
            df = pd.DataFrame()

        self.log_progress(f'Start writing to {storage}/{filename}', stage=1, total_stages=2)
        if type == 'parquet':
            df.to_parquet(
                full_file_path, engine='pyarrow', compression=None
            )
        elif type == 'json':
            df.to_json(
                full_file_path, orient='records', lines=True
            )
        elif type == 'csv':
            df.to_csv(
                full_file_path
            )
        else:
            raise ValueError('Unknown type')
        self.log_progress(f'Writing is done {storage}/{filename}', stage=2, total_stages=2)
        return df
