# Conexão SFTP 💻
![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)

<p align="center">
    <b>Este script automatiza a transferência de arquivos via SFTP, realizando o envio de arquivos `.ret` do diretório local para um servidor remoto, validando se o arquivo já foi enviado anteriormente.</b>
    <br><br>
    <b>Ele também registra logs e envia um e-mail consolidado com a lista de arquivos enviados com sucesso.</b> 
</p>

## 🚀 Funcionalidades

- **Conexão SFTP:** O script se conecta a um servidor remoto via SFTP, utilizando as credenciais definidas em um arquivo `config.yml`.
- **Verificação de Arquivos:** Valida se o arquivo já foi enviado anteriormente, evitando reenvios desnecessários.
- **Transferência de Arquivos:** Envia arquivos `.ret` do diretório local para o diretório remoto especificado no arquivo de configuração.
- **Registro de Logs:** Mantém um log com a data e hora de cada transferência realizada ou de eventuais erros.
- **Envio de E-mails:** Ao final do processo, um e-mail consolidado é enviado com a lista de todos os arquivos que foram transferidos com sucesso.
- **Execução em Loop:** O script é executado a cada 30 minutos, repetindo o processo de verificação e transferência.

## 🛠️ Como configurar

1. **Configurar o arquivo `config.yml`:** 
   - Defina as credenciais do servidor SFTP, diretórios remotos e locais, e configurações de e-mail.
   
    Exemplo de configuração:
    ```yaml
    login:
      hostname: "seu_servidor"
      username: "seu_usuario"
      password: "sua_senha"
      remote_directory_in: "/caminho/remoto/in"
      remote_directory_done: "/caminho/remoto/done"
    
    root:
      local_directory: "/caminho/local"
      log_directory: "/caminho/log"
    
    smtp:
      username: "seu_email"
      password: "sua_senha"
      receiver_email: "email_destinatario"
    ```

2. **Instalar as dependências:**  
   - Use o `pip` para instalar os pacotes necessários:

    ```bash
    pip install paramiko yagmail pyyaml
    ```

3. **Executar o script:**
   - Após configurar o `config.yml`, execute o script Python:

    ```bash
    python script_sftp.py
    ```

## 📝 Detalhes do Funcionamento

1. **Conexão SFTP:**  
   O script usa a biblioteca `paramiko` para estabelecer uma conexão SFTP com o servidor remoto, permitindo o envio seguro dos arquivos.

2. **Verificação de Arquivos:**  
   Antes de enviar qualquer arquivo, o script verifica se ele já foi enviado, conferindo o log e o servidor remoto para evitar duplicidade.

3. **Log de Atividades:**  
   Todas as ações realizadas, como transferências bem-sucedidas e erros, são registradas em um arquivo de log (`arquivos_enviados.txt`).

4. **Envio Consolidado de E-mails:**  
   No final de cada ciclo, um e-mail é enviado com uma lista de todos os arquivos que foram transferidos com sucesso.

5. **Execução Contínua:**  
   O script fica em loop, verificando o diretório local a cada 30 minutos para transferir novos arquivos.

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/69211741?v=4" width="200px;" alt="João Victtor Profile Picture"/><br>
        <sub>
          <b>João Victtor S. Melo</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

