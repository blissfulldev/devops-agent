resource "aws_db_subnet_group" "main" {
  name        = "aurora-subnet-group"
  description = "Subnet group for Aurora cluster"
  subnet_ids  = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  tags = merge(local.common_tags, {
    Name = "aurora-subnet-group"
  })
}

resource "aws_security_group" "rds" {
  name        = "rds-sg"
  description = "Security group for RDS Aurora cluster"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
    description = "Allow all outbound traffic within the VPC"
  }

  tags = merge(local.common_tags, {
    Name = "rds-sg"
  })
}

resource "aws_rds_cluster" "main" {
  cluster_identifier      = "aurora-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = "15.3"
  backup_retention_period = 7
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  storage_encrypted       = true
  skip_final_snapshot     = true
  tags                    = local.common_tags
}

resource "aws_rds_cluster_instance" "instance_1" {
  identifier                 = "aurora-instance-1"
  cluster_identifier         = aws_rds_cluster.main.id
  instance_class             = "db.t3.medium"
  engine                     = "aurora-postgresql"
  engine_version             = "15.3"
  publicly_accessible        = false
  auto_minor_version_upgrade = true
  db_subnet_group_name       = aws_db_subnet_group.main.id

  # Performance Insights for monitoring (WAF Operational Excellence)
  performance_insights_enabled = true

  tags = {
    Name = "aurora-instance-1"
  }
}
