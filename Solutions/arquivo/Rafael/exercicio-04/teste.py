import boto3
import json

sqs = boto3.client("sqs", endpoint_url="http://localhost:4566", region_name="us-east-1", aws_access_key_id="test", aws_secret_access_key="test")
url = sqs.get_queue_url(QueueName="livros-entrada.fifo")["QueueUrl"]

# Vamos testar enviar um livro de ficção
livro = {"id": 101, "titulo": "Fundação", "autor": "Isaac Asimov", "categoria": "ficcao"}

sqs.send_message(
    QueueUrl=url, 
    MessageBody=json.dumps(livro), 
    MessageGroupId="grupo-livros", 
    MessageDeduplicationId="101"
)
print("Livro de teste enviado para a fila")