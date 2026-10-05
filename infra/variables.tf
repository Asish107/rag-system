variable "my_ip" {
  description = "Your public IP address in CIDR form, like 1.2.3.4/32."
  type        = string
}

variable "claude_model_id" {
  description = "OpenRouter model ID used for answer generation."
  type        = string
  default     = "anthropic/claude-sonnet-5.5"
}