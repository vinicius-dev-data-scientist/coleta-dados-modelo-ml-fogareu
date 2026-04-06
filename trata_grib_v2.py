import xarray as xr
import cfgrib
import pandas as pd
import os

grib_file_path = r'C:\Users\gabriel.pereira\estagio-fogareu\all\1bf29a0a57e1c65073a4a24c65c45c99\data.grib'

dado_csv = r'C:\Users\gabriel.pereira\estagio-fogareu\unknown-data\teste_data.csv'


if not os.path.exists(grib_file_path):
    print(f"Erro: {grib_file_path} não encontrado.")
else:
    try:
        datasets =  cfgrib.open_datasets(grib_file_path)
        print(f"{len(datasets)} sub-dataset(s) encontrado(s) no arquivo.")
        dados_grib = xr.open_dataset(grib_file_path, engine='cfgrib')
        
        dfs = []
        
        for i, ds in enumerate(datasets):
            print(f"\n--- Sub-dataset {i} ---")
            print(ds)
           
            df = ds.to_dataframe().reset_index()
            df['_source_dataset'] = i
            dfs.append(df)
            
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(dado_csv, index=False)        
               
        print(f"Convertido com sucesso!")
        print(f"CSV salvo em: {os.path.abspath(dado_csv)}")
        print(f"Total de linhas: {len(df_final)}")
        print(f"Total de colunas: {list(df_final.columns)}")
        
    except Exception as e:
        print(f"Um erro ocorreu durante a conversão: {e}")

