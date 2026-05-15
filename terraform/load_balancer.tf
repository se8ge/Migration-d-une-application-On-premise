resource "aws_lb" "main" {
  name               = "${var.project_name}-alb-${random_id.infra_suffix.hex}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]

  tags = {
    Name = "${var.project_name}-alb"
  }
}

resource "aws_lb_target_group" "api" {
  name     = "${var.project_name}-api-tg-${random_id.infra_suffix.hex}"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/api"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

resource "aws_lb_target_group_attachment" "api_attach" {
  target_group_arn = aws_lb_target_group.api.arn
  target_id        = aws_instance.app_server.id
  port             = 8000
}
