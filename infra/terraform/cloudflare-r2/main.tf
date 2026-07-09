terraform {
  required_version = ">= 1.6.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_r2_bucket" "media" {
  account_id = var.cloudflare_account_id
  name       = var.r2_bucket_name
}

output "r2_bucket_name" {
  value = cloudflare_r2_bucket.media.name
}
