---
layout: post
title: Cloudwatch Custom Metrics in a Python Lambda
date: 2021-10-23
---

My team is responsible for developing, maintaining, and operating several web services that host our machine learning models. Periodically we need quick ways to check that our code is operating correctly. For example, a user may tell us that the software did something weird and we need to figure out whether it's an ordinary fluctuation or something more serious.

We're looking into [Cloudwatch Custom Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) for this. In the past, we've found that some metrics systems can add unacceptable latency so I'm being more deliberate about comparing options and measuring latency impact in a controlled way. This post compares custom metrics in [boto3](https://aws.amazon.com/sdk-for-python/) vs [Embedded Metric Format (EMF)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html).

> Summary: EMF is lower latency and gives more options.

Let's start from the results:

Recording a custom metric in boto3 added about 20 ms latency compared to no metrics. Recording a metric in EMF didn't add latency beyond the base service.

Also note, EMF showed abnormally good results on Sunday that I'm ignoring.

### How I tested

I modified [this example MLops lambda](https://github.com/ktrnka/mlops_example_lambda), which hosts a scikit-learn machine learning model on lambda using Docker. I tested three versions of the code: One without any custom metrics, one with custom metrics in EMF using [aws_embedded_metrics](https://github.com/awslabs/aws-embedded-metrics-python), and one with custom metrics using boto3.

I used [Locust](https://locust.io/) to test the services, ramping up to 50 users with a spawn rate of 0.2. The [locust file is in the repo](https://github.com/ktrnka/mlops_example_lambda/blob/main/serving/tests/locust_file.py) if you'd like to see the randomness involved in the actual calls. I did a fresh deployment each time and continued the test until 50 concurrent users and it passed 4,000 total requests.

I'm reporting p50 and p90 rather than averages because those are minimally affected by cold starts at the beginning of the test.

### boto3

[boto3](https://aws.amazon.com/sdk-for-python/) is the standard Python wrapper for AWS API calls. It's also already included with your lambda, so if you're uncomfortable with packaging Python dependencies for lambda it's already there.

The additional latency (20 ms) is the major downside. It's also a little trickier than EMF if you have unit tests; the boto3 calls will crash if your unit test runner doesn't have AWS credentials. I avoided that by disabling the metrics calls in the test environment but I'm not happy with the way I implemented it.

Originally, I was worried that boto3 might be asynchronous and that I'd potentially lose metrics data. That wasn't an issue. In the first test I double-checked that the count of metrics was equal to the number of requests.

### Embedded Metric Format (EMF)

EMF automatically creates Cloudwatch Custom Metrics if you format log statements in a special way. I used [aws_embedded_metrics](https://github.com/awslabs/aws-embedded-metrics-python) to write log statements in the right format.

The main advantage over boto3 is low latency. It also provides sensible default metrics dimensions out of the box. Here's an example of what it generated in an early test to log the string length of the input to the API. It sets default dimensions for the LogGroup, ServiceName, and ServiceType.

```json
{
    "LogGroup": "ExampleTextClassifierStac-ExampleTextClassifierHan-PZQ8yd6C6x3R",
    "ServiceName": "ExampleTextClassifierStac-ExampleTextClassifierHan-PZQ8yd6C6x3R",
    "ServiceType": "AWS::Lambda::Function",
    "executionEnvironment": "AWS_Lambda_python3.8",
    "memorySize": "3008",
    "functionVersion": "$LATEST",
    "logStreamId": "2021/10/16/[$LATEST]f35168a9ad9e40e39422fb6be26a5800",
    "_aws": {
        "Timestamp": 1634401767050,
        "CloudWatchMetrics": [
            {
                "Dimensions": [
                    [
                        "LogGroup",
                        "ServiceName",
                        "ServiceType"
                    ]
                ],
                "Metrics": [
                    {
                        "Name": "input.num_chars",
                        "Unit": "Count"
                    }
                ],
                "Namespace": "aws-embedded-metrics"
            }
        ]
    },
    "input.num_chars": 66
}
```

The main downside is that it slows down unit tests. That can be fixed by setting the environment to "local" on the metrics configuration. It happens because it's inspecting the execution environment to see how it should log, and one of the options it tries is to connect to various ports in the execution environment.

Also, I was surprised to find that it doesn't require IAM permissions for `cloudwatch:PutMetricData`. I'm not too worried about the security there, just surprised.

### I wish I'd had the time to test

#### EMF properties

There's another great feature of EMF supported by aws_embedded_metrics that I haven't tried yet: properties. These are like dimensions, except that they can store high-cardinality variables.

For example, say you want to log the user ID for each custom metric. Properties are the way to do it. If you tried the same thing in dimensions you'd end up with a big bill at the end of the month.

#### Lambda Powertools

Lambda Powertools Python also has [an EMF wrapper](https://awslabs.github.io/aws-lambda-powertools-python/latest/core/metrics/). It provides all the benefits of aws_embedded_metrics *and* it also batches metric data in log statements so that your logs aren't too spammy.

#### Async boto3 wrapper

There are also libraries that make boto3 calls asynchronous, like [aioboto3](https://pypi.org/project/aioboto3/).

#### Cost

As far as I know, Cloudwatch Logs are very cheap. So adding a few more log lines won't change my bill much.

I also would've liked to get hard evidence that high-cardinality dimensions can run up your bill. I've read that it's bad, but haven't confirmed.

### See also

- [Introducing a better way to record custom metrics](https://hackernoon.com/introducing-a-better-way-to-record-custom-metrics-hj3dn3q6r)
- [Lowering costs and focusing on our customers with Amazon CloudWatch embedded custom metrics](https://awsfeed.com/whats-new/management-tools/lowering-costs-and-focusing-on-our-customers-with-amazon-cloudwatch-embedded-custom-metrics)
