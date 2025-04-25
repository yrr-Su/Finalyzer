from __future__ import annotations

from numpy import nan
from pandas import DataFrame, to_numeric, to_datetime, read_csv, ExcelWriter
from openpyxl.styles import Font, Alignment
from pathlib import Path

from config.setting import CONFIG
from FinCrawler.core.base import ProcessorInterface
from FinCrawler.core.dto import (
    CarawlerResultDTO,
    ProcessorConfigDTO,
    ProcessorResultDTO
)
from FinCrawler.tool.excel import ExcelTool


class thefewProcessor(ProcessorInterface):
    name = 'thefew'

    def _init_setup(self,
                    crawler_DTO: CarawlerResultDTO,
                    process_config_DTO: ProcessorConfigDTO) -> None:
        self.rules = process_config_DTO.rules
        self.output = process_config_DTO.output

        self.selected_columns = [
            '名稱', '轉換價值', '百元報價', 'CBAS總價', 'CB 收盤價',
            '轉換溢價率 (%)', '轉換價','股票收盤價', '股價前高',
            '發債位階', '收盤位階', '已轉換 (%)', '到期日', '剩餘天數'
            ]

        self.numeric_columns = [
            '轉換價值', 'CB 收盤價', '轉換溢價率 (%)',
            '轉換價', '股票收盤價', '股價前高',
            '發債位階', '收盤位階', '已轉換 (%)', '剩餘天數'
            ]

        self.rename_columns = {
            '最新 CB 收盤價': 'CB 收盤價',
            '最新股票收盤價': '股票收盤價',
            '轉換比例': '已轉換 (%)',
            '轉換溢價率': '轉換溢價率 (%)',
            '目前轉換價': '轉換價',
            }

        self.df_init = DataFrame(crawler_DTO.result).T
        self.df_init.index = to_numeric(self.df_init.index, errors='coerce') # type: ignore
        self.df_init.index.name = 'ID'

        with (CONFIG.PATH_RESOURCE / 'thefew_highest.csv').open(
                'r', encoding='utf-8') as f:
            self.df_highest = read_csv(f, index_col='ID')
            self.df_highest['value'] = to_numeric(self.df_highest['value'],
                                                  errors='coerce').copy()

            self.df_highest = self.df_highest.reindex(self.df_init.index)


    def _init_process(self) -> DataFrame:
        self.df_init = self.df_init.copy()

        self.df_init['股價前高'] = self.df_highest.loc[self.df_init.index, 'value'].copy()
        self.df_init[['百元報價', 'CBAS總價', '發債位階', '收盤位階', '剩餘天數']] = nan
        self.df_init.rename(columns=self.rename_columns, inplace=True)

        df_init_process = self.df_init[self.selected_columns].copy()

        df_init_process['轉換溢價率 (%)'] = df_init_process['轉換溢價率 (%)'].str.replace('%', '')
        df_init_process['已轉換 (%)'] = df_init_process['已轉換 (%)'].str.replace('%', '')

        df_init_process[self.numeric_columns] = df_init_process[self.numeric_columns].apply(
                                                    to_numeric, errors='coerce'
                                                    )

        df_init_process['收盤位階'] = df_init_process['股票收盤價'] / df_init_process['股價前高'] * 100
        df_init_process['發債位階'] = df_init_process['轉換價'] / df_init_process['股價前高'] * 100

        df_init_process['到期日'] = to_datetime(df_init_process['到期日'], errors='coerce')
        df_init_process['剩餘天數'] = (df_init_process['到期日'] - to_datetime('today')).dt.days

        df_init_process = df_init_process.copy().round(2)
        df_init_process['到期日'] = df_init_process['到期日'].dt.strftime('%Y-%m-%d')

        return df_init_process


    def _process_filter(self, df_process: DataFrame) -> dict[str, DataFrame]:

        process_without_highest = (
            (df_process['剩餘天數'] >= self.rules['剩餘天數']) &
            (df_process['已轉換 (%)'] < self.rules['已轉換 (%)']) &
            (df_process['轉換價值'] >= self.rules['轉換價值'][0]) &
            (df_process['轉換價值'] <= self.rules['轉換價值'][1]) &
            (df_process['轉換溢價率 (%)'] > self.rules['轉換溢價率 (%)']) &
            (df_process['CB 收盤價'] >= self.rules['CB 收盤價'][0]) &
            (df_process['CB 收盤價'] <= self.rules['CB 收盤價'][1])
            )

        process_with_highest = (
            process_without_highest.copy() &
            (df_process['發債位階'] <= self.rules['發債位階']) &
            (df_process['收盤位階'] <= self.rules['收盤位階'])
            )

        df_with_highest = df_process[process_with_highest].reset_index().copy()
        df_without_highest = df_process.loc[self.df_highest.isna()['value'] & process_without_highest].reset_index().copy()
        df_process = df_process.reset_index().copy()

        return {
            'with_highest': df_with_highest,
            'without_highest': df_without_highest,
            'all': df_process
            }

    def _beautify_excel(self, dict_df_process: dict[str, DataFrame]) -> Path:

        output_file = self.output / f'{self.name}.xlsx'

        with ExcelWriter(output_file, mode='w') as writer:
            dict_df_process['all'].to_excel(writer, sheet_name='原始資料', index=False)
            dict_df_process['with_highest'].to_excel(writer, sheet_name='篩選後含前高', index=False)
            dict_df_process['without_highest'].to_excel(writer, sheet_name='篩選後無前高資料', index=False)

            not_formate_columns = ['ID', '剩餘天數']

            for worksheet in writer.sheets.values():

                for col_idx, col_name in enumerate(dict_df_process['all'].columns, start=1):
                    formated_status = (col_name not in not_formate_columns)

                    col_letter = worksheet.cell(row=1, column=col_idx).column_letter

                    cell_width = []
                    for cell in worksheet[col_letter]:
                        cell_value = str(cell.value) if cell.value is not None else ''

                        font_name = "標楷體" if ExcelTool.is_chinese(cell_value) else "Times New Roman"
                        cell.font = Font(name=font_name, size=14)
                        cell.alignment = Alignment(horizontal="center")

                        cell_width.append(ExcelTool.calculate_column_width(cell_value))

                        if ExcelTool.is_numeric(cell_value) & formated_status:
                            cell.number_format = "0.00"

                    worksheet.column_dimensions[col_letter].width = max(*cell_width) + 2

                worksheet.freeze_panes = "C2"

        return output_file

    def process(self,
                crawler_DTO: CarawlerResultDTO,
                process_config_DTO: ProcessorConfigDTO
                ) -> ProcessorResultDTO:

        self._init_setup(crawler_DTO, process_config_DTO)
        df_init_process = self._init_process()
        dict_df_process = self._process_filter(df_init_process.copy())
        output_file = self._beautify_excel(dict_df_process)

        return ProcessorResultDTO(result=output_file)


