output "db_endpoint" {
  value = aws_db_instance.rag.address
}

output "db_port" {
  value = aws_db_instance.rag.port
}

output "db_secret_arn" {
  value = aws_db_instance.rag.master_user_secret[0].secret_arn
}

output "api_url" {
  value = aws_apigatewayv2_api.rag.api_endpoint
}