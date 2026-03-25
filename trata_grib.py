import xarray as xr
import pandas as pd
import os

grib_file_path = r'C:\Users\gabriel.pereira\estagio-fogareu\9208fef7d40176813a94323f770c0b4f\data.grib'

dado_csv = 'teste_data.csv'


if not os.path.exists(grib_file_path):
    print(f"Erro: {grib_file_path} não encontrado.")
else:
    try:
        dados_grib = xr.open_dataset(grib_file_path, engine='cfgrib')
        
        df = dados_grib.to_dataframe()
        
        df.to_csv(dado_csv, index=True)
        
        print(f"Convertido com sucesso de {grib_file_path} para {dado_csv}")
        print(f"CSV salvo em: {os.path.abspath(dado_csv)}")
        
    except Exception as e:
        print(f"Um erro ocorreu durante a conversão: {e}")
