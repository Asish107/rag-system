# -----------------------------------------------------------------------------
# API Gateway HTTP API
# Public HTTPS entry point for rag-api.
# -----------------------------------------------------------------------------

resource "aws_apigatewayv2_api" "rag" {
  name          = "rag-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "rag_api" {
  api_id = aws_apigatewayv2_api.rag.id

  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.rag_api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "ask" {
  api_id = aws_apigatewayv2_api.rag.id

  route_key          = "POST /ask"
  authorization_type = "AWS_IAM"
  target             = "integrations/${aws_apigatewayv2_integration.rag_api.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.rag.id

  name        = "$default"
  auto_deploy = true

  default_route_settings {
    throttling_rate_limit  = 1
    throttling_burst_limit = 5
  }
}

# Allow only this API Gateway /ask route to invoke Lambda A.
resource "aws_lambda_permission" "api_gateway" {
  statement_id = "AllowApiGatewayInvoke"

  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rag_api.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.rag.execution_arn}/*/*/ask"
}