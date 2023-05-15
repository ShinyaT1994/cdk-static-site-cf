from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cf,
    aws_cloudfront_origins as cf_origins,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct


class CdkStaticSiteCfStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 Bucket
        bucket = s3.Bucket(
            self, 
            "MyStaticSiteBucket"
        )

        # CloudFront
        distribution = cf.Distribution(
            self,
            'Distribution',
            default_behavior=cf.BehaviorOptions(
                origin=cf_origins.S3Origin(bucket)
            ),
            default_root_object='index.html',
        )

        # Deploy site contents to S3 Bucket
        s3deploy.BucketDeployment(
            self, 
            "DeployWithInvalidation",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )

