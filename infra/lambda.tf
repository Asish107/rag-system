data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_iam_role" "rag_search_lambda" {
  name = "rag-search-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rag_search_lambda_vpc" {
  role       = aws_iam_role.rag_search_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "rag_search_lambda_rds" {
  name = "rag-search-lambda-rds"
  role = aws_iam_role.rag_search_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "rds-db:connect"
        ]

        Resource = format(
          "arn:aws:rds-db:%s:%s:dbuser:%s/rag_reader",
          data.aws_region.current.name,
          data.aws_caller_identity.current.account_id,
          aws_db_instance.rag.resource_id
        )
      }
    ]
  })
}

data "archive_file" "rag_search_lambda" {
  type = "zip"

  source_dir = "${path.module}/../lambda/search"

  output_path = "${path.module}/../lambda/search.zip"
}

resource "aws_lambda_function" "rag_search" {
  function_name = "rag-search"

  role = aws_iam_role.rag_search_lambda.arn

  runtime = "python3.12"
  handler = "rag.handlers.search.handler"

  architectures = ["x86_64"]

  filename         = data.archive_file.rag_search_lambda.output_path
  source_code_hash = data.archive_file.rag_search_lambda.output_base64sha256

  timeout     = 30
  memory_size = 512

  environment {
    variables = {
      DB_HOST = aws_db_instance.rag.address
    }
  }

  vpc_config {
    subnet_ids = data.aws_subnets.default.ids

    security_group_ids = [
      aws_security_group.rag_lambda_sg.id
    ]
  }
}