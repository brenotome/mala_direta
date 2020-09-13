import sys
import csv
import smtplib
import ssl
import getpass
from email.message import EmailMessage

def main():
    if len(sys.argv) < 2:
        print('Uso "python3 maladireta.py arquivo.csv"')
        return
    filename = sys.argv[1]
    print(f'filename:{filename}')
    try:
        csv_file = open(filename)
        data = read_csv(csv_file)

        model = data[0]['modelo']
        subject = data[0]['assunto']
        tags = [row['tags'] for row in data]
        username = input('Insira seu email (é desse que será enviado):')
        password = getpass.getpass(prompt='Senha(ela não aparece aqui): ', stream=None)

        server = config_smtp(data, username, password)
        send_mails(server, username, data, model, subject, tags)
        server.quit()
    except Exception as e:
        print(f'Deu ruim, copia isso aqui e me passa plz:\n\n{e}')

def read_csv(csv_file):
    print('lendo arquivo de entrada')
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]
    return data

def config_smtp(data, username, password):
    print(f'Efetuando a conexão com o servidor')
    smtp = data[0]['smtp']
    port = data[0]['porta']
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp, port, context=context, timeout=60)
    server.ehlo()
    print('server criado')
    server.ehlo()
    server.login(username, password)
    
    return server

def send_mails(server, username, data, model, subject, tags):
    print('Iniciando envio')
    for row in data:
        try:
            message = EmailMessage()
            message['Subject'] = subject
            message['From'] = username
            message['To'] = row['email']

            print(f'enviando para {row["email"]}')
            message.set_content(format_mail(model,tags,row))
            server.send_message(message)
        except Exception as e:
            print(f'o email para {row["email"]} não foi enviado,\nerro:{e}')

def format_mail(model, tags, row):
    tags = [tag for tag in tags if tag!='']
    for tag in tags:
        model = model.replace(f'{{{{{tag}}}}}',row[tag])
    return model

if __name__ == "__main__":
    main()