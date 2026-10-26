import time
import json
import logging
import os
import boto3

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

endpoint_url = os.getenv("AWS_ENDPOINT_URL", "http://floci:4566")
sqs = boto3.client("sqs", endpoint_url=endpoint_url)
s3 = boto3.client("s3", endpoint_url=endpoint_url)

FILA_ENTRADA = "livros-entrada.fifo"
FILA_SAIDA = "livros-saida.fifo"

def obter_url_fila(nome_fila: str) -> str:
    resposta = sqs.get_queue_url(QueueName=nome_fila)
    return resposta["QueueUrl"]

def escolher_bucket(genero: str) -> str:
    genero_limpo = str(genero).strip().lower()
    if genero_limpo == "romance":
        return "romance"
    elif genero_limpo == "ficcao":
        return "ficcao"
    return "outros"

def salvar_livro(livro: dict) -> str:
    bucket = escolher_bucket(livro.get("genero", ""))
    titulo = livro.get("titulo", "sem-titulo").replace(" ", "_")
    nome_arquivo = f"{titulo}.json"
    caminho_s3 = f"s3://{bucket}/{nome_arquivo}"

    s3.put_object(
        Bucket=bucket,
        Key=nome_arquivo,
        Body=json.dumps(livro),
        ContentType="application/json"
    )
    return caminho_s3

def processar(mensagem: dict) -> bool:
    try:
        corpo = json.loads(mensagem["Body"])
    except json.JSONDecodeError:
        logger.error("JSON inválido recebido. A ignorar mensagem para não travar o worker.")
        return True

    livro_id = corpo.get("id")
    if not livro_id:
        logger.error("Mensagem sem ID. A ignorar.")
        return True

    # 1. Guarda no S3
    caminho_s3 = salvar_livro(corpo)
    logger.info(f"Livro {livro_id} guardado em {caminho_s3}")

    mensagem_saida = {
        "id": livro_id,
        "arquivo": caminho_s3
    }
    sqs.send_message(
        QueueUrl=obter_url_fila(FILA_SAIDA),
        MessageBody=json.dumps(mensagem_saida),
        MessageGroupId="processados",
        MessageDeduplicationId=str(livro_id)
    )
    logger.info(f"Aviso enviado para a fila de saída (Livro ID: {livro_id})")
    
    return True

def main():
    logger.info("Worker iniciado e à escuta de mensagens...")
    url_entrada = obter_url_fila(FILA_ENTRADA)

    while True:
        resposta = sqs.receive_message(
            QueueUrl=url_entrada,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        mensagens = resposta.get("Messages", [])
        if not mensagens:
            continue

        for msg in mensagens:
            recibo = msg["ReceiptHandle"]
            sucesso = False
            
            try:
                sucesso = processar(msg)
            except Exception as erro:
                logger.error(f"Erro inesperado ao processar mensagem: {erro}")

            if sucesso:
                sqs.delete_message(
                    QueueUrl=url_entrada,
                    ReceiptHandle=recibo
                )
                logger.info("Mensagem eliminada da fila de entrada com sucesso.\n")

if __name__ == "__main__":
    main()