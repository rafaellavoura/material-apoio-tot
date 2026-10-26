import os
import time
import boto3
from botocore.exceptions import ClientError

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)

FILA_ENTRADA = "livros-entrada.fifo"
FILA_SAIDA = "livros-saida.fifo"

def obter_url_fila(nome_fila):
    while True:
        try:
            resposta = sqs.get_queue_url(QueueName=nome_fila)
            return resposta["QueueUrl"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
                print(f"Fila '{nome_fila}' ainda não existe. A tentar novamente em 2 segundos")
                time.sleep(2)
            else:
                raise

def main():
    print("A aguardar pela criação das filas SQS...")
    url_entrada = obter_url_fila(FILA_ENTRADA)
    print(f"Worker iniciado e à escuta de mensagens na fila: {url_entrada}")
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()