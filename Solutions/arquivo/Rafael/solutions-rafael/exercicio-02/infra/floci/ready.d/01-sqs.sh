#!/bin/sh
echo "Criando filas SQS FIFO..."

aws --endpoint-url=http://localhost:4566 sqs create-queue \
  --queue-name InputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false

aws --endpoint-url=http://localhost:4566 sqs create-queue \
  --queue-name OutputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false

echo "Filas SQS criadas"