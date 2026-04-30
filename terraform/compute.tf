resource "aws_instance" "app_server" {
  ami           = "ami-05b5a865c3579bbc4" # Ubuntu 22.04 LTS in eu-west-3
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io docker-compose
              systemctl start docker
              systemctl enable docker
              EOF

  tags = {
    Name = "${var.project_name}-app-server"
  }
}
