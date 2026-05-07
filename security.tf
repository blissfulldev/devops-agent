resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for the internal ALB"
  vpc_id      = aws_vpc.main.id

  # Egress rule to allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # tfsec:ignore:aws-vpc-no-public-egress-sgr
  }

  tags = merge(local.common_tags, {
    Name = "alb-sg"
  })
}

resource "aws_security_group" "ecs" {
  name        = "ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id
  tags        = local.common_tags
}

resource "aws_vpc_security_group_ingress_rule" "rds_ingress" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  description                  = "Allow PostgreSQL traffic from ECS tasks"
}
