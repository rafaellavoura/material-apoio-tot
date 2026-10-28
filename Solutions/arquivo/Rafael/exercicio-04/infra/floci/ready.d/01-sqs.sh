#!/bin/sh
set -eu

echo "A criar infraestrutura"

awslocal sqs create-queue --queue-name livros-entrada.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false
awslocal sqs create-queue --queue-name livros-saida.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false

awslocal s3 mb s3://romance
awslocal s3 mb s3://ficcao
awslocal s3 mb s3://outros

echo "Infraestrutura pronta"