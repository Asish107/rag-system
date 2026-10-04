data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "rag_db_sg" {
  name   = "rag-db-sg"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "postgres" {
  security_group_id = aws_security_group.rag_db_sg.id

  cidr_ipv4   = var.my_ip
  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}