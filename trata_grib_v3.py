import xarray as xr
import pandas as pd
import cfgrib
import os

grib_file_path = r'C:\Users\gabriel.pereira\estagio-fogareu\all\a231ddc35f32ba0f6ea1b3f6fb0136b1\data.grib'
dado_csv = r'C:\Users\gabriel.pereira\estagio-fogareu\unknown-data\teste_data.csv'

if not os.path.exists(grib_file_path):
    print(f"Erro: {grib_file_path} não encontrado.")
else:
    dfs = []

    # Try each GRIB edition separately
    for edition in [1, 2]:
        for step_type in ['instant', 'accum', 'avg', 'max', 'min']:
            try:
                ds = xr.open_dataset(
                    grib_file_path,
                    engine='cfgrib',
                    backend_kwargs={'indexing_time': 'validtime'},
                    filter_by_keys={
                        'edition': edition,
                        'stepType': step_type
                    },
                    errors='ignore'
                )
                df = ds.to_dataframe().reset_index()
                df['_edition'] = edition
                df['_stepType'] = step_type
                dfs.append(df)
                print(f"OK — edition={edition}, stepType={step_type}, shape={df.shape}, vars={list(ds.data_vars)}")
            except Exception as e:
                # Most combinations won't exist — that's fine
                pass

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(dado_csv, index=False)
        print(f"\nCSV salvo em: {os.path.abspath(dado_csv)}")
        print(f"Total de linhas: {len(df_final)}, Colunas: {list(df_final.columns)}")
    else:
        # Last resort: read raw messages with eccodes
        print("Tentando leitura mensagem por mensagem com eccodes...")
        try:
            import eccodes
            records = []
            with open(grib_file_path, 'rb') as f:
                while True:
                    msg = eccodes.codes_grib_new_from_file(f)
                    if msg is None:
                        break
                    try:
                        record = {
                            'shortName':  eccodes.codes_get(msg, 'shortName'),
                            'edition':    eccodes.codes_get(msg, 'edition'),
                            'stepType':   eccodes.codes_get(msg, 'stepType'),
                            'validTime':  eccodes.codes_get(msg, 'validityTime'),
                            'validDate':  eccodes.codes_get(msg, 'validityDate'),
                            'level':      eccodes.codes_get(msg, 'level'),
                            'values_mean': eccodes.codes_get_values(msg).mean(),
                        }
                        records.append(record)
                    finally:
                        eccodes.codes_release(msg)

            df_final = pd.DataFrame(records)
            df_final.to_csv(dado_csv, index=False)
            print(f"CSV salvo via eccodes: {os.path.abspath(dado_csv)}")
            print(df_final.head())
        except ImportError:
            print("eccodes não instalado. Instale com: conda install -c conda-forge eccodes python-eccodes")
        except Exception as e:
            print(f"Erro no fallback eccodes: {e}")
