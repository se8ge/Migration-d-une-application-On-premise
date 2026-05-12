resource "aws_key_pair" "deployer" {
  key_name   = "stocklive-deployer-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC/USR7yoCOtads8O4zfwty60WnAl4YvKN/HCwSgjHpAwoWeFSgGE7sa99L19qZeEDiMqPcuisrBIpZvU+lkikS8HJd+BL4SmdertFqc8278r9piUrTxVrOK6PHomaxbZecibeCy0Nc//h8rkMEeMDcg63lzsH7CAWyPXWiNbNV8kAO/62a6PVpWba0gqeWBDvX5kRxJ9n07ep9k1BA1IidrKaIh5bgewQlCmvIshVP5BoAwaUq3FyujPOAhERtBEyrBQdctf1feqLSjEJZBlhteBxEVxgmT3xdMS93C+lOgtqhebxgiI6qXi9X4sPNU19O4KvGk6ZCs58htSIdxmofcIYUW8L1urhAbE1hnC0eEIFsfSn1NJoUgfncx1P+DaZYmg8L1rZjAZ6JjUTJ2GedD9cIniW2crb5eZ7h8HvPnBggMwByxE7UnqgXHDWf8qWn3FpWQbn4m6k1DCqd8W04tGgqFz8bSzftVJM0FJa+G9cs00BsWzw1PKCG9HSqDn8c0d7DNbtegEpo9eh/L7KX5eBOWhevv3FG0fzGTaOus2exJuop71PxyQg7Yi7yxOJTMlpN7rcdHkpfwY09Y0WnoR1zOuoxGu5gUAaHK4djYHKgYMe7Cy/vf/VKsVVdNVlP1eJC2eLojN20xZA4B54c1sZqRa+OINPUJcvSxUXCEw=="
}

resource "aws_instance" "app_server" {
  ami           = "ami-05b5a865c3579bbc4" # Ubuntu 22.04 LTS in eu-west-3
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ssm_profile.name
  key_name      = aws_key_pair.deployer.key_name

  user_data = <<-EOF
              #!/bin/bash
              # S'assurer que l'agent SSM est démarré (déjà présent sur Ubuntu 22.04)
              systemctl enable amazon-ssm-agent
              systemctl start amazon-ssm-agent

              # Installation de Docker en arrière-plan pour ne pas bloquer le boot
              (
                curl -fsSL https://get.docker.com -o get-docker.sh
                sh get-docker.sh
                systemctl start docker
                systemctl enable docker
                usermod -aG docker ubuntu
              ) &
              EOF

  tags = {
    Name = "${var.project_name}-app-server-v3"
  }
}
