resource "aws_db_instance" "rag" {
  identifier = "rag-db"

  engine         = "postgres"
  engine_version = "17"

  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  storage_type            = "gp2"
  storage_encrypted       = true
  backup_retention_period = 1

  publicly_accessible = true
  skip_final_snapshot = true
  deletion_protection = false

  db_name  = "rag"
  username = "rag"

  manage_master_user_password         = true
  iam_database_authentication_enabled = true
  vpc_security_group_ids = [
    aws_security_group.rag_db_sg.id
  ]
}

