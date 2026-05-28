resource "aws_db_subnet_group" "db_subnets" {
  name       = "stocklive-db-subnet-group"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "_%-" # Caractères sûrs pour une URL de connexion
}

resource "aws_db_instance" "mysql" {
  identifier           = "${var.project_name}-db"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  db_name              = "stocklive_db"
  username             = "admin"
  password             = random_password.db_password.result
  parameter_group_name = "default.mysql8.0"
  db_subnet_group_name = aws_db_subnet_group.db_subnets.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot  = true
  publicly_accessible  = false

  tags = {
    Name = "${var.project_name}-db"
  }
}
