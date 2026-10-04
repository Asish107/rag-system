import {
  to = aws_secretsmanager_secret.openrouter
  id = "arn:aws:secretsmanager:us-east-1:702872201875:secret:rag/openrouter-api-key-vjsXyu"
}

resource "aws_secretsmanager_secret" "openrouter" {
  name = "rag/openrouter-api-key"

  lifecycle {
    prevent_destroy = true
  }
}