terraform {
  cloud {
    organization = "PavloFesenko"

    workspaces {
      tags = ["gif_analyzer"]
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}

variable "project" {
  type = string
}

variable "env" {
  type = string
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name              = "${var.project}_${var.env}"
  source_path                = "scripts"
  handler                    = "app.handler"
  runtime                    = "python3.10"
  timeout                    = 30
  memory_size                = 1024
  create_lambda_function_url = true
  environment_variables = {
    ENV = "aws"
  }

  layers = [
    module.layer_api.lambda_layer_arn,
    module.layer_core.lambda_layer_arn,
    module.layer_model.lambda_layer_arn
  ]
}

module "layer_api" {
  source = "terraform-aws-modules/lambda/aws"

  create_function = false
  create_layer    = true

  layer_name          = "${var.project}_${var.env}_api"
  compatible_runtimes = ["python3.10"]

  build_in_docker = true
  runtime         = "python3.10"

  source_path = [
    {
      path             = "layers/api"
      pip_requirements = true
      prefix_in_zip    = "python"
    }
  ]
}

module "layer_core" {
  source = "terraform-aws-modules/lambda/aws"

  create_function = false
  create_layer    = true

  layer_name          = "${var.project}_${var.env}_core"
  compatible_runtimes = ["python3.10"]

  build_in_docker = true
  runtime         = "python3.10"

  source_path = [
    {
      path             = "layers/core"
      pip_requirements = true
      prefix_in_zip    = "python"
    }
  ]
}

module "layer_model" {
  source = "terraform-aws-modules/lambda/aws"

  create_function = false
  create_layer    = true

  layer_name          = "${var.project}_${var.env}_model"
  compatible_runtimes = ["python3.10"]

  source_path = "layers/model"
}