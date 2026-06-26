resource "aws_cloudfront_distribution" "stocklive" {
  enabled             = true
  comment             = "StockLive CDN - HTTPS front"
  default_root_object = ""

  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "stocklive-alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "stocklive-alb-origin"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    forwarded_values {
      query_string = true
      headers      = ["*"]

      cookies {
        forward = "all"
      }
    }

    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}

output "cloudfront_url" {
  description = "URL HTTPS de l'application via CloudFront"
  value       = "https://${aws_cloudfront_distribution.stocklive.domain_name}"
}
