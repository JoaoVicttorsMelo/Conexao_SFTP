import os
import time
import paramiko
import yagmail
from datetime import datetime
import yaml

# Nome do arquivo YAML na mesma pasta
arquivo_yml = 'config.yml'

# Abrir e ler o arquivo YAML
with open(arquivo_yml, 'r') as arquivo:
    dados = yaml.safe_load(arquivo)

# Configurações do servidor SFTP
hostname = dados['login']['hostname']
port = 22
username = dados['login']['username']
password = dados['login']['password']
remote_directory_in = dados['login']['remote_directory_in']
remote_directory_done = dados['login']['remote_directory_done']

# Diretório local onde estão os arquivos .ret
local_directory = dados['root']['local_directory']
log_directory = dados['root']['log_directory']
log_file_path = os.path.join(log_directory, 'arquivos_enviados.txt')

# Configuração do e-mail
sender_email = dados['smtp']['username']
receiver_email = dados['smtp']['receiver_email']
smtp_username = dados['smtp']['username']
smtp_password = dados['smtp']['password']

while True:

    # Conexão SFTP
    def conectar_sftp():
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        return ssh.open_sftp()

    # Função para verificar se o nome do arquivo já está no log
    def verificar_arquivo_no_log(nome_arquivo):
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                linhas = log_file.readlines()
                for linha in linhas:
                    # Verificar se o nome do arquivo e a mensagem "enviado com sucesso" estão presentes
                    if nome_arquivo in linha and 'enviado com sucesso' in linha:
                        return True
        return False

    # Função para verificar se o arquivo já existe no servidor SFTP
    def verificar_arquivo_existe(sftp, nome_arquivo, diretorio):
        try:
            sftp.stat(os.path.join(diretorio, nome_arquivo))
            return True
        except FileNotFoundError:
            return False

    # Função para registrar mensagens no log
    def registrar_log(mensagem):
        with open(log_file_path, 'a') as log_file:
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"[{data_hora}] {mensagem}\n")

    # Função para enviar um e-mail consolidado com todos os arquivos enviados
    def enviar_email_consolidado(arquivos_enviados):
        try:
            yag = yagmail.SMTP(smtp_username, smtp_password)
            assunto = "Arquivos enviados com sucesso"
            contents = "<div style='text-align: center;'>"
            contents += "<p><strong style='color: green;'>Arquivos enviados:</strong></p>"
            contents += "<ul>"

            for arquivo in arquivos_enviados:
                contents += f"<li>{arquivo}</li>"

            contents += "</ul>"
            contents += "<br><br><br></div>"

            yag.send(
                to=receiver_email,
                subject=assunto,
                contents=contents,
                headers={'X-Priority': '1'}
            )
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")
            registrar_log(f"Erro ao enviar o e-mail: {e}")

    # Função principal
    def listar_e_transferir_arquivos():
        try:
            # Conectando ao servidor SFTP
            sftp = conectar_sftp()

            # Listando os arquivos .ret
            arquivos_para_transferir = []
            arquivos_enviados = []
            for arquivo in os.listdir(local_directory):
                if arquivo.endswith('.ret'):
                    # Verificar se o arquivo já foi enviado pelo log
                    if verificar_arquivo_no_log(arquivo):
                        print(f"O arquivo {arquivo} já foi enviado anteriormente. Não será transferido novamente.")
                        registrar_log(f"Arquivo {arquivo} já existe no log. Transferência não realizada.")
                    else:
                        arquivos_para_transferir.append(arquivo)

            # Listando arquivos encontrados
            if arquivos_para_transferir:
                print("Arquivos encontrados:")
                for arquivo in arquivos_para_transferir:
                    print(f"- {arquivo}")

                for arquivo in arquivos_para_transferir:
                    try:
                        # Verificar se o arquivo já existe no SFTP
                        if not verificar_arquivo_existe(sftp, arquivo, remote_directory_in) and \
                                not verificar_arquivo_existe(sftp, arquivo, remote_directory_done):
                            sftp.put(os.path.join(local_directory, arquivo),
                                        os.path.join(remote_directory_in, arquivo))
                            print(f"Arquivo {arquivo} transferido com sucesso para {remote_directory_in}")

                            # Registrar envio no arquivo de log
                            registrar_log(f"Arquivo {arquivo} enviado com sucesso.")
                            arquivos_enviados.append(arquivo)
                        else:
                            print(f"Arquivo {arquivo} já existe em {remote_directory_in} ou {remote_directory_done}, não foi transferido.")
                            registrar_log(f"Arquivo {arquivo} já existe em {remote_directory_in} ou {remote_directory_done}, não foi transferido.")
                    except Exception as e:
                        print(f"Erro ao transferir o arquivo {arquivo}: {e}")
                        registrar_log(f"Erro ao transferir o arquivo {arquivo}: {e}")

                # Enviar um único e-mail consolidado com os arquivos enviados
                if arquivos_enviados:
                    enviar_email_consolidado(arquivos_enviados)
            else:
                print("Nenhum arquivo .ret foi encontrado.")
                registrar_log("Nenhum arquivo .ret foi encontrado.")

            # Fechando a conexão SFTP
            sftp.close()

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            registrar_log(f"Ocorreu um erro geral: {e}")

    # Executar a função
    listar_e_transferir_arquivos()
    # programa espera 30 min para rodar novamente
    time.sleep(1800)
