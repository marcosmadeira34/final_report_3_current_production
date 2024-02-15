from controllers import *
from database import *
from check_orders import *
from colorama import Fore
from termcolor import cprint
import art
from time import sleep
import schedule
import functools
import logging


# configuração do logger
logging.basicConfig(filename=r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/04 - EXTRATORES PROCESSADOS/logs.log',                    
                    format='%(asctime)s:%(levelname)s:%(message)s')


ascii_banner = art.text2art("Relatorio Final")
colored_banner = cprint(ascii_banner, 'green')


# DIRETORIO DE ENTRADA EXTRATOR TOTVS
extractor_file_path = r"/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/01-EXTRATOR_PEDIDOS_DE_CLIENTES"

# DIRETORIO DE SAIDA DOS ARQUIVOS
batch_totvs_path = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/02-SAÍDA_EXTRATOR'
target_directory = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS'

# DIRETORIO DE JA PEDIDOS FATURADOS
invoiced_orders = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/PEDIDOS_FATURADOS'

# DIRETORIO DE NOVOS PEDIDOS IDENTIFICADOS NO EXTRATOR
news_orders = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/03 - DATA_RAW'
source_directory = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/03 - DATA_RAW'
news_orders = r'/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/03 - DATA_RAW'

# DIRETORIO DE EXTRATORES JÁ FINALIZADOS
processed_extrator_path = r"/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/04 - EXTRATORES PROCESSADOS"

# DIRETORIO DE RELATORIOS MESCLADOS(funcao inativada)
output_merge_path = r"/home/administrator/WindowsShare/01 - FATURAMENTO/01 - CLIENTES - CONTROLE - 2024 TOTVS/MERGE_RELATORIO_FINAL"



file_processor = FileProcessor(extractor_file_path, invoiced_orders, news_orders, output_merge_path)
host_postgres = 'postgresql://postgres:123456789@localhost:5432/postgres'
sql = ConnectPostgresQL(host_postgres)
final_report = FinalReport(host_postgres)
#sql.create_database()



if __name__ == "__main__":
    while True:
        #sql.create_database()
        #file_processor.delete_xml(files_path=extractor_file_path)
        sleep(0.5)
        print(Fore.LIGHTYELLOW_EX + 'CHECANDO NOVOS PEDIDOS ...' + Fore.RESET)
        final_report.check_and_update_orders(extractor_file_path, 'pedido_faturamento')
        sleep(0.5)
        print(Fore.LIGHTYELLOW_EX + 'PEDIDOS CHECADOS COM SUCESSO!\n' + Fore.RESET)
        print(Fore.GREEN + 'PROCESSANDO E TRATANDO DADOS NOS ARQUIVOS' + Fore.RESET)
        final_report.rename_format_columns(news_orders)
        sleep(0.5)
        
        file_processor.move_files_to_month_subfolder(
            directory_origin=news_orders,
            target_directory=target_directory)
        
        print(Fore.GREEN + 'MOVENDO ARQUIVOS PARA DIRETÓRIO DE SAÍDA' + Fore.RESET)
        sleep(0.5)
        # formata dia e hora para nomear o arquivo
        
        print(Fore.GREEN + 'AUTOMAÇÃO CONCLUÍDA : ' + Fore.RESET + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S\n')))
        logging.info('ÚLTIMA EXECUÇÃO : ' + str(datetime.now()))        

        # Agendar a execução para mover arquivos para pasta de processados a cada 1 hora
        schedule_function = functools.partial(file_processor.move_files_to_month_subfolder, 
                                      directory_origin=extractor_file_path,
                                      target_directory=processed_extrator_path)

        schedule.every(59).minutes.do(schedule_function)
                                              
        schedule.run_pending()
        sleep(0.5)

        #print(Fore.LIGHTYELLOW_EX + 'DELETANDO ARQUIVOS XLSX' + Fore.RESET)

        





