output "alb_dns_name" {
  description = "DNS name of the Load Balancer"
  value       = aws_lb.main.dns_name
}

output "db_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.mysql.endpoint
}

output "app_server_public_ip" {
  description = "Public IP of the application server"
  value       = aws_instance.app_server.public_ip
}

output "app_server_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "rds_password" {
  description = "The generated password for the RDS instance"
  value       = random_password.db_password.result
  sensitive   = true
}
