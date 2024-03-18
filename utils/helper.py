import os
from datetime import datetime
from datetime import timedelta
from re import findall

import pandas as pd
import numpy as np

from .consts import (RENAME_COLUMNS, REORDER_LIST,
                     MESES, INPUT_TABLE, CEPS, CITIES,
                     ESTADOS
                    )


class DataReader:
    def __init__(self, delay: int=0) -> None:
        self.date = datetime.now() - timedelta(delay)

    def folder(self, nome_pasta):
        '''Cria uma pasta com o nome especificado e navega até ela'''
        try:
            # Converte o nome da pasta em uma string, caso ainda não seja uma
            nome_pasta = str(nome_pasta)
            # Cria o caminho completo da pasta, concatenando o diretório atual com o nome da pasta
            dir_destino = os.path.join(os.getcwd(), nome_pasta)
            # Verifica se a pasta já existe, se não existir, cria a pasta
            if not os.path.exists(dir_destino):
                # Cria a pasta com o nome especificado
                os.makedirs(dir_destino)
            # Navega para a pasta criada
            os.chdir(dir_destino)
            # Exibe mensagem de sucesso
            print(f"Foi para a pasta {nome_pasta}")
        except OSError as e:
            # Exibe mensagem de erro caso não seja possível criar a pasta
            print(f"Não foi possível criar a pasta {nome_pasta}: {e}")

    def create_folder(self, name_folder: str, informant_code: str, folder_prints: str = 'prints'):
        '''Cria as pastas necessárias para armazenar os arquivos da coleta e saída'''
        _, dt_prev_fim = self._intervalo_datas()

        # main_name = f"{informant_code}_{name_folder}"
        # self.folder(main_name)
        # Cria a pasta coleta_n, onde n é o ano da data prevista
        year_folder = f'coleta_{self.date.year}'
        self.folder(year_folder)

        # Cria a pasta coleta_mes, onde mes é o mês correspondente à data prevista
        month_folder = f'coleta_{MESES.get(str(self.date.month))}'
        self.folder(month_folder)

        self.folder(f"coleta{self.request_dec(day=self.date.day)}")

        # Cria a pasta saida_ano_mes_dia correspondente à data prevista
        self.folder(f"saida_{self.date.strftime('%Y_%m_%d')}")

        try:
            os.mkdir(folder_prints)
        except OSError as e:
            # Exibe mensagem de erro caso não seja possível criar a pasta
            print(f"Não foi possível criar a pasta {folder_prints}: {e}")
            
            
            
    @staticmethod
    def request_dec(day: int) -> str:
        """
        Conditional insert DEC for directory based on current date

        Args:
            day [int]
        Return:
            dec [str]
        """
        print("Defining DEC to export information")
        if day <= 10:
            return "_1_dec"
        if 10 < day <= 20:
            return "_2_dec"
        if 20 < day <= 31:
            return "_3_dec"

            
    def _intervalo_datas(self):
        '''Retorna o primeiro e ultimo dia do dec referente a data passada'''
        if self.date.day <= 10:
            dt_prev_inicio = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=1)
            dt_prev_fim = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=10)
        elif 10 < self.date.day <= 20:
            dt_prev_inicio = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=11)
            dt_prev_fim = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=20)
        else:
            dt_prev_inicio = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=21)
            dt_prev_fim = pd.Timestamp(
                year=self.date.year, month=self.date.month, day=30)
        return dt_prev_inicio, dt_prev_fim

    def _regex(self, msg: str, pattern='()'):
        match pattern:
            case '()':
                try:
                    return findall(r'\((\d+)\)', msg)[0]
                except:
                    return '1'
            
            case '[]':
                try:
                    return findall(r'\[(\d+)\]', msg)[0]
                except: 
                    return ''

    def read_table(self,
                   informant_code: str,
                   input_sheet: str = INPUT_TABLE, date_filter=True):

        print('datetime now', self.date)
        self.dt_prev_ini, self.dt_prev_fim = self._intervalo_datas()
        #file = self.date.strftime("encomenda_%Y%m%d.xls")
        file = "encomenda_20240209.xls"
        #file = "Pasta1.csv"
        # sheet = pd.read_excel(f'{input_sheet}/{file}')
        sheet = pd.read_csv(f'{input_sheet}/{file}',
                            delimiter='\t',
                            encoding="ISO-8859-1",
                            dtype={'CD_INFORM': str,
                                   'DATA_PREVISTA': str,
                                   'NR_SEQ_INSINF': str
                                   }
                            )

        sheet = sheet[sheet.CD_INFORM == informant_code]
        for i in range(len(sheet)):
            data = sheet.iloc[i, 1].split('/')
            try:
                sheet.iloc[i, 1] = pd.Timestamp(
                    year=int('20' + data[-1]), month=int(data[1]), day=int(data[0]))
            except:
                sheet.iloc[i, 1] = pd.Timestamp(
                    year=int(data[-1]), month=int(data[1]), day=int(data[0]))

        if date_filter:
            dt_prev_inicio, dt_prev_fim = self._intervalo_datas()
            print(dt_prev_inicio, dt_prev_fim)
            sheet = sheet[sheet.DATA_PREVISTA <= dt_prev_fim]
            sheet = sheet[sheet.DATA_PREVISTA > dt_prev_inicio]
        sheet['DATA_PREVISTA'] = [
            '{}/{}/{}'.format(x.day, x.month, x.year) for x in sheet['DATA_PREVISTA']]

        sheet['CEP'] = [CEPS[x] for x in sheet['CD_UF_REGIAO']]
        sheet['CIDADES'] = [CITIES[x] for x in sheet['CD_UF_REGIAO']]
        sheet['ESTADOS'] = [ESTADOS[x] for x in sheet['CD_UF_REGIAO']]
        sheet['QTD'] = [self._regex(x, '()') for x in sheet['DS_SINO_NOME_INS_INSINF']]

        sheet = sheet.fillna('')
        return sheet


class DataBuilder:

    def load_creator(self,
                     sheet: pd.DataFrame,
                     name_website: str,
                     informant_code: str,
                     rename_columns: list=RENAME_COLUMNS,
                     reorder_list: list=REORDER_LIST,
                     delay: int=0,
                ) -> pd.DataFrame:
        
        self.date = datetime.now() - timedelta(delay)

        sheet["data_coleta"] = self.date.strftime('%d/%m/%Y')  # criando outra coluna
        # sheet.to_excel("carga_prep_teste.xls")
        sheet = sheet.rename(columns=rename_columns)
        sheet = sheet.reindex(columns=reorder_list)
        sheet = sheet.fillna("")

        print('encomenda', sheet.shape)
        dataframe = sheet[reorder_list].copy()
        print('carga', sheet.shape)
        dataframe['FT'] = np.where(dataframe['Valor do Preço'] == "", "S", "")
        dataframe['Justificativa Livre'] = np.where(dataframe['Valor do Preço'] == '',
                                                    'ITEM EM FALTA NO SITE/BOLETIM/TABELA', 'PREÇO CONFORME SITE/BOLETIM/TABELA')
        dataframe['Moeda'] = 'R$'
        # dataframe['Valor do Preço'] = dataframe['Valor do Preço'].replace(
        #     '.', '')
        dataframe['Frete Incluso'] = ''
        dataframe['Frete Nao Declarado'] = ''
        # dataframe['Valor do Frete'] = np.where(dataframe['Tipo de Preço']=='AV', '', dataframe['Valor do Frete'])
        dataframe['Data Prevista'] = sheet['Data Prevista']
        dataframe['URL Insumo Informado'] = sheet['URL Insumo Informado'].replace('nan', '')
        file_name = f"carga_{name_website}_BP{informant_code}_{self.date.strftime('%d_%m_%Y')}.xls"

        dataframe.to_excel(file_name, sheet_name='Carga BP', index=False)