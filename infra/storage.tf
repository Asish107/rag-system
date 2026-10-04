import {
  to = aws_s3_bucket.docs
  id = "rag-system-docs-10ks"
}

resource "aws_s3_bucket" "docs" {
  bucket = "rag-system-docs-10ks"

  lifecycle {
    prevent_destroy = true
  }
}

import {
  to = aws_s3_bucket_public_access_block.docs
  id = "rag-system-docs-10ks"
}

resource "aws_s3_bucket_public_access_block" "docs" {
  bucket = aws_s3_bucket.docs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}