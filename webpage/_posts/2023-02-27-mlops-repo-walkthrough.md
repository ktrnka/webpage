---
layout: post
title: MLOps repo walkthrough
date: 2023-02-27
---

There's a big difference between building a machine learning model that works on your computer, and making that model available for others to use. If implemented poorly, your users will be frustrated that your software isn't reliable. And it can take months to implement it well!

[My previous article shared the principles I've learned over the years](https://medium.com/@keith.trnka/mlops-design-principles-e30cc40442a1). This one walks through example code and critiques the approach. When I started deploying machine learning models into web services I found the complexity bewildering, and I hope this walkthrough will help readers in similar situations.

------------------------------------------------------------------------

I built a series of prototypes to explore different tools and ideas in MLOps for a basic text classifier. This post will focus on the most recent prototype. It has automated training, testing, and deployment of models to a web service with AWS Lambda.

I limited the number of ML-specific tools for two reasons: 1) I wanted to use similar infrastructure to traditional software projects and 2) at work it was often easier to meet compliance needs this way.

*Side note: You may notice that some of these repos are a couple years old. Originally I did these just for myself. Over the years I've found that I've often used them as examples for others and that's motivated me to finally write it up.*

### The basics

I sometimes miss the old days when you'd host your code on a server under a desk somewhere! In those days, getting our code or models on a server just meant copying files and restarting the web daemon.

There are many issues with that approach though. These are a few of those problems:

- It means we'll need to spend much more of our time just managing servers, like applying security patches, ensuring that the internet and power don't go out, or fixing it when a hardware component breaks.
- The process is prone to mistakes and bugs, such as code that works on your computer but not the server. Or you might forget to run tests.
- The under-desk service can only handle so many requests per second. If your site becomes suddenly popular it may not be able to keep up with the surge of users.

Modern tools are designed to address these problems, but they can make it more difficult to learn a new code base.

### Deploying models to Lambda

[This repo](https://github.com/ktrnka/mlops_example_lambda) has training and serving for a news classification scikit-learn model but it should work for PyTorch and other libraries.

Let's say hypothetically that we're building a backend service for Medium to recommend appropriate categories for new posts. The Medium frontend will send the text of the article to our backend and receive the predicted category.

As I go through the repo I'll summarize terminology at the end of each section.

#### API Gateway and Lambda

The HTTP request is received by API gateway and forwarded to Lambda. If there's a Lambda worker available, it forwards the request to the worker. If there isn't, it starts a new worker which will load the code, load the model, and execute the request. If it takes more than 30 seconds to load the code and model, the request will fail but eventually it'll boot and then requests will work.

For testing I used a POST request with a simple payload like this:

```json
{
    "text": "The Seattle Seahawks crushed the Cleveland Browns on Thursday 52-7"
}
```

API gateway receives the request and calls our Lambda handler with request info in the parameters.

In the Lambda code, API gateway sends this information in two dicts *event* and *context.* From serving/app/app.py:

```python
def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    prediction = model.predict([request_body["text"]])[0]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": prediction,
            "request": request_body
        })
    }
```

API gateway sends the POST request body in event\["body"\] as a plain string so we need to parse the JSON in it. Then we run the text field through the model. Note that we need to make it into a list of inputs (with one element) and then take the first prediction from the output. That's because scikit-learn predict methods are designed for batches of data. Then API gateway needs the response in a particular shape dict including the HTTP status code (200). Out of habit, I like to also return the request data to make debugging easier.

**New terminology**

- [AWS Lambda](https://aws.amazon.com/lambda/): This runs our code on a server and handles scaling up the number of workers automatically.
- [AWS API Gateway](https://aws.amazon.com/api-gateway/): This serves as a bridge between our Lambda and requests coming from the Internet.
- HTTP POST: This is the [HTTP method](https://www.restapitutorial.com/lessons/httpmethods.html) that we're using. Although GET would be a more semantically-appropriate method, sending JSON generally isn't supported with GET. POST is more common in my experience because the input data structure is often complex.

#### Docker and Python, called by Lambda

From serving/app/Dockerfile:

```dockerfile
CMD ["app.lambda_handler"]
```

This is the last line of the Dockerfile, and it tells Lambda to call the lambda_handler function in app.py*.*

When the Lambda starts, it imports the app.py file which causes everything outside of a function to be run, such as loading the model in our case. With Lambdas we call this a cold start. Then it's available until the worker is shut down. The model is baked into the same Docker image as the code and loaded just like any other file. The Docker image is built and deployed from Github Actions when code is merged to main that changes anything in the *serving* folder. Likewise, the configuration of API gateway and Lambda can be updated at the same time. One of the files under *serving* is the model file itself, which is stored using [data version control (DVC)](https://dvc.org/). If the model changes when merging to *main*, the Docker image will be rebuilt and redeployed with the new model.

Here's where the model is loaded in serving/app/app.py with timing and metrics omitted:

```python
def load_model():
    ...
    model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
    model = joblib.load(model_path)

    ...

    return model

model = load_model()
```

All we're doing is calling joblib.load on the file path. This works because the model was saved with joblib and because the serving code has all the dependencies needed for the model from scikit-learn.

The first line is making sure that the file path is relative to app.py, not relative to where app.py is being run from, because I don't know if Lambda makes that consistent. I do that out of habit because I've been burned in the past when code was run from an unexpected directory.

That model file is baked into the Docker image in serving/app/Dockerfile:

```dockerfile
COPY data ./data
```

It's just copying the serving/app/data folder into the Docker image from the machine that's building the Docker image. If for some reason we needed another model, we'd just put it in that folder and it'd be available inside of Docker too.

**New terms**

- Cold start: When there are no Lambda workers immediately available, Lambda must start one up.
- [Docker](https://www.docker.com/): Docker is a way of packaging code, data, and dependencies together in a way that can be run the same way on any computer.
- [Data Version Control (DVC)](https://dvc.org/): I use DVC to version large files such as models, because git doesn't work well with large files.
- [Github Actions](https://github.com/features/actions): Github that will run our code on their servers for a short time, triggered by changes in Github or on a timer. It's free for small-scale usage.
- main branch: In Github development, it's common to put the current version of code in a branch named "main" and create other branches while writing new code.
- merged: When changes from one git branch are included into another branch. In this case, I'm talking about merging code from a development branch into the main branch.

**Additional reading**

- [Operating Lambda: Performance optimization -- Part 1 (AWS)](https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/): This covers cold starts and how to address them.
- [Docker overview (Docker)](https://docs.docker.com/get-started/overview/)
- [What is Docker? (AWS)](https://aws.amazon.com/docker/)

#### Building and deploying with CDK from Github Actions

The Docker image is built and uploaded to AWS Elastic Container Registry (ECR) in CDK in serving/deployment/stacks/lambda_service.py:

```python
handler = lambda_.DockerImageFunction(
    self,
    "ExampleTextClassifierHandler",
    code=lambda_.DockerImageCode.from_image_asset("../app"),
    timeout=cdk.Duration.seconds(60),
    memory_size=3008
)
```

The *from_image_asset* function builds the Docker image for us, which takes as a parameter a directory containing the *Dockerfile* you want to build. I'm setting the memory size to 3 GB which is probably more than strictly needed but it'll help with latency because Lambda scales the CPU with more RAM. The 60-second timeout is at the Lambda layer. Keep in mind that API gateway has an *independent timeout* with a maximum of 30 seconds.

The Docker image is necessary with Lambda due to the model size and the Python dependency size. Otherwise I would've used Lambda's zip-file deployment which is faster.

CDK is a framework for infrastructure as code (IaC). This means that we're defining our AWS configuration in code. It helps us standardize configuration and deployments which helps reduce accidents. Because it's stored in the repo, it also means that we can use the pull request process to have peer review for our configuration. It also means that we're updating our service code and infrastructure at the same time, so we can bundle together a new model with increased memory for example. And it also means that we can revert configuration changes more easily. Also, as one final benefit, CDK is implemented so that most deployments are done with little or no downtime.

The CDK stack is run from .github/workflows/deploy_service.yml:

```yaml
    - run: cdk deploy --require-approval never
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_DEFAULT_REGION: us-west-2
```

This runs *cdk deploy.* We have to turn off interactive approval questions otherwise it'll hang. The other parts are setting environment variables for the AWS IAM user, copied from the Github Actions Secrets set on this repo (I set those manually). Then when CDK creates your API gateway it'll show the auto-generated URL in Github Actions.

Further up in deploy_service.yaml, we install DVC and fetch the model:

```yaml
    - run: pip install dvc[s3]
    - run: dvc pull
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

This also needs AWS credentials to read from the S3 bucket.

At the very top of the file, we can see when the Github Action workflow is triggered:

```yaml
on:
  push:
    branches:
      - main
    paths:
    - 'serving/**'
    - '.github/workflows/deploy_service.yml'
```

This runs the deploy_service.yaml action when *main* is updated (which happens on PR merge) AND when anything under serving/ is changed, or deploy_service.yaml itself is changed.

**New terms**

- [AWS Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/): The place to upload Docker images in AWS to be used in Lambda and other AWS services.
- Infrastructure as code (IaC): Defining your infrastructure with code rather than clicking buttons in a user interface.
- [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/): AWS tools and libraries for infrastructure as code that can be defined in Javascript or Python.
- [AWS S3](https://aws.amazon.com/s3/): File storage in AWS.
- [AWS IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html): An account for a computer or person that can take action in your AWS account according to the associated permissions. Typically accessed via an access key and secret. The access key and secret are analogous to a username and password but for programmatic access.
- [Github Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets): Sensitive configuration that is stored on Github associated with a repo, and available to the Github Action, such as an access key or password.
- Github Action workflow: A series of steps for Github Actions to run, associated with a trigger like a branch change. There's one yaml file per workflow.
- [Pull request (PR)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests): In Github, it's common to do development on a new branch, then submit a pull request (PR) which is a request to merge the code into another branch (typically main). It's common for a peer to review the modified code in the PR before approving or requesting changes. It's also common for companies to restrict their Github repos so that pull requests cannot be merged until someone has approved it.

**Additional reading**

- [Business Benefits of Infrastructure as Code (Spacelift, 2021)](https://spacelift.io/blog/business-benefits-of-iac)
- [AWS IAM: Working, Components, and Features Explained (simplilearn, 2022)](https://www.simplilearn.com/tutorials/aws-tutorial/aws-iam)

#### Automated service testing run from Github Actions

We don't want to deploy bad code, so we also have automated testing.

The tests I have are very basic: 1) Test that the endpoint can run without crashing 2) Test that the endpoint crashes as expected if the input text is missing. Those are in serving/tests/test_lambda_handler.py:

```python
class BasicTests(unittest.TestCase):
    def test_basic_path(self):
        lambda_handler({"body": json.dumps({"text": "example input"})}, None)

    def test_crash(self):
        self.assertRaises(BaseException, lambda_handler, {"body": json.dumps({"not_the_right_one": "example input"})}, None)
```

In these tests I'm calling the lambda_handler directly without the *context* set, because the function doesn't use it anyway.

They're triggered from .github/workflows/test_service.yml:

```yaml
      - name: Run tests
        run: make test-service
```

"make test-service" is defined in Makefile at the root of the repo:

```makefile
test-service:
   PYTHONPATH=serving/app/ python serving/tests/test_lambda_handler.py
```

This just runs the python command to run the tests and ensures that the app code can be imported into the test code. It's not strictly needed to have a Makefile rule for it, but I like to do that so that I'm running the exact same test command everywhere: Both in Github Actions for automated testing and also on my computer for local testing.

The Github Action is triggered at the top of test_service.yml:

```yaml
on:
  push:
    branches-ignore:
      - main
    paths:
    - 'serving/**'
    - '.github/workflows/test_service.yml'
```

This translates to "run this action anytime code is pushed to a branch except main, that has a change under serving or a chance to test_service.yml". This will run on pull requests and also non-PR branches. Github is configured so that if the tests fail, it'll block any PRs for that branch.

Tests are run if anything under *serving* changes in a pull request. That includes changes to the model file!

#### Re-training the model from Github Actions

Now let's look at how the model is trained. The key parts of training are in training/src/main.py:

```python
model = make_pipeline(
    TfidfVectorizer(min_df=30, ngram_range=(1, 2), sublinear_tf=True),
    LogisticRegressionCV()
)

model.fit(training_data.data, training_data.target)

joblib.dump(model, os.path.join(args.output_dir, "model.joblib.gz"), compress=9)
```

This is a bigram model using logistic regression with cross-validation to optimize the regularization weight. The min_df setting ignores infrequent ngrams which helps us keep the model small-ish without losing much accuracy. Sublinear_tf reduces the impact of repetitions of the same ngram, and I find that makes models slightly more robust against weird input.

I'm using the make_pipeline helper from scikit-learn to build the Pipeline object. I find that scikit-learn pipelines 1) make loading and saving easier 2) make hyperparameter tuning more effective 3) reduce accidental leaks of testing data into training.

If you look at main.py you'll also see evaluation of the model and comparison against a baseline as well.

main.py is called from the Makefile from a DVC command:

```makefile
train:
   dvc repro train
```

As before, I like to use Makefile to ensure that I'm running the same commands on my local machine and on the server. In this example, it's calling DVC to reproduce the "train" pipeline, which is defined in dvc.yaml:

```yaml
stages:
  train:
    cmd: python training/src/main.py serving/app/data/ serving/app/requirements.txt
    deps:
    - training/
    outs:
    - serving/app/data/model.joblib.gz
    metrics:
    - serving/app/data/metrics.json
```

This is the [pipeline feature of DVC](https://dvc.org/doc/start/data-management/data-pipelines) and it's similar to *make* except that it also automatically runs *dvc add* on our output files to ensure that they're pushed to S3 on *dvc push*. The metrics part saves metrics in the specified file and the repro command will show the updated values to us.

Training is triggered from Github Actions in .github/workflows/train_model.yml:

```yaml
# build when a branch other than main changes training or this file:
on:
  push:
    branches-ignore:
      - main
    paths:
    - 'training/**'
    - '.github/workflows/train_model.yml'

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      # ... for full steps see github ...
      # train the model
      - name: Train model
        run: make train
      # run the web service tests to make sure it still works!
      - run: pip install -r serving/app/requirements.txt
      - name: Run web service tests
        run: make test-service
      # commit the model, which needs the IAM user to access S3 on dvc push
      - name: Commit model
        # email address from https://github.community/t/github-actions-bot-email-address/17204/5
        run: |
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git commit -am "Automated model build"
          dvc push
          git push
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

In this example I commented inline and cut some boilerplate code. I'm running the web service tests *before* committing the model to the repo because 1) This action can't trigger the test_service action and 2) I don't want to commit models that fail the tests.

#### Configuring AWS for DVC and Github Actions

I setup DVC to use an S3 bucket for storage, which is managed by the Terraform code under *infrastructure*. It creates the S3 bucket for DVC to use as well as an IAM user for Github Actions to use to access DVC and deploy CDK.

The code is verbose in parts but I'll give an overview of infrastructure/resources.tf with comments added:

```hcl
// create the bucket. In this file it's referenced as aws_s3_bucket.b.bucket
resource "aws_s3_bucket" "b" {
  bucket_prefix = "trnka-dvc-"
  acl = "private"
}

// create the IAM user for Github Actions to use
resource "aws_iam_user" "github_actions" {
  name = "github_actions_lambda_ml"
  force_destroy = true
}

// give the IAM user permissions to list files in the bucket and read/write/delete files
resource "aws_iam_user_policy" "dvc_policy" {
  name = "dvc_policy"
  user = aws_iam_user.github_actions.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::${aws_s3_bucket.b.bucket}"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::${aws_s3_bucket.b.bucket}/*"]
    }
  ]
}
EOF
}

// this policy is long but ensures the IAM user can run CDK and upload ECR images
resource "aws_iam_user_policy" "cdk_policy" {
  name = "cdk_policy"
  user = aws_iam_user.github_actions.name

  // ...
}

// make sure there's an access key
resource "aws_iam_access_key" "github_actions" {
  user = aws_iam_user.github_actions.name
}

// when we run terraform apply, it'll show the secret on the command line
// which we can copy into Github Actions Secrets
output "secret" {
  value = aws_iam_access_key.github_actions.secret
}
```

This code creates the S3 bucket for DVC, the IAM user for Github Actions, gives the IAM user appropriate permissions, and makes the access key so that Github Actions can "log in" to AWS.

One benefit of infrastructure as code is that we can ask experts to review it before we run it.

**New terms**

- [Terraform](https://www.terraform.io/): Terraform is a tool for infrastructure as code that works with many popular cloud providers.
- AWS IAM policy: I'm not the best at explaining this, but it's a list of permissions that can be attached to an IAM user or role.
- AWS IAM role: This is like an IAM user but you can't log in as it. It's only there for services to use. If you're a similar age as me, you might think of this as a service user with better security.

### What could possibly go wrong? A critique

It's tough to review your own work, but I'll give it a fair shot! I have three sections:

1.  A review of **general principles**
2.  An overview of **industry needs** that weren't otherwise mentioned
3.  A discussion of **priorities to fix**

#### General principles

**Does the service manage latency vs cost well?**

- AWS Lambda scales up and down automatically, so if there's a surge of users it'll handle that and then scale down to save cost afterwards. It doesn't require any special configuration to do this.
- When Lambda scales up and warms up a new "instance", it needs to download the Docker image and load the model. We call this a cold start. If the image and model are even moderately large, the API request will time out while it loads. This is especially bad in our repo because there are no active users, so it'll sit at 0 concurrency until a request is made during testing, then time out while loading the model until there's a warm Lambda.
- On the topic of cost, Lambda will scale up as needed with incoming requests up until a region-wide concurrency limit. So someone could spam your API to scale up your Lambda and increase your AWS bill significantly.
- The repo is implemented entirely in us-west-2. If the API is being called from around the world or even around the US, many users will have slow responses simply because they're far away from the server. On the other hand, if it's only called by servers or users near us-west-2 that's fine.

**Is the service highly available?**

- Due to cold starts, when the service deploys it causes a full outage until the new model is loaded. In a professional situation that's unacceptable but may be acceptable for hobbyist work.
- Can we quickly and safely revert if a bug makes it to production? Yes, in this repo we'd revert by merging a PR in Github. The deployment pipeline takes 4-5 minutes. It'll probably take longer to get your PR approved.
- Can we quickly detect production issues? No, there aren't any alarms implemented in this repo so if it goes down we probably won't find out right away. AWS provides some default dashboards for API gateway and Lambda though.
- Can we switch to PyTorch without downtime? Yes, this repo is implemented so that we could make a major machine learning change like switching frameworks, test it, and deploy without downtime and with the ability to revert, so long as the framework change is a single PR.

**Is there any way that untested work might be deployed?**

There are several gaps in my testing:

- The components between the API request and the Lambda are untested: The Docker packaging, the interaction between the Lambda code and API gateway, and the API gateway configuration. The Docker part could be tested easily by running the unit tests inside of Docker, though it'll slow down testing a bit. The AWS configuration could be better tested by using [AWS SAM](https://aws.amazon.com/serverless/sam/) to spin up a local version of the stack for testing. This issue also affects developer productivity, for example if a developer is changing the way that dependencies are packaged they may need to edit the Dockerfile and it's best if they can test it on their computer.
- Another gap is time-based: The dependencies for unit tests are installed at a different time than the dependencies for the Docker image. Because the dependencies aren't fully pinned (see previous post for why), that means that in theory a new library version could be deployed between testing and deployment which could cause a production outage. One way to address this is to build the Docker image in the PR pipeline, use it for unit testing, then upload to ECR. That would also save time in deployment. Another alternative is to pin dependencies more.
- In theory, someone could overwrite the model file in S3 and bypass our test automation, though it'd be annoying to do. If they did that it wouldn't actually trigger a deployment though because it wouldn't be a change in Github. It'd have to be the exact same file path on S3.

**Is it easy for new developers to learn?**

It's tough to judge your own work for learnability. Whenever possible it's better to have someone review the work and explain the challenges they faced.

- In my opinion, this is hard for a complete beginner to learn because there are so many tools. Most of the complexity happens in automation, which the developer may not need to fully understand. But DVC for instance introduces a new concept -- instead of just doing a *git clone* they also need to pull the DVC files to make the repo work. That could be improved with git hooks.
- A related challenge with DVC is that it requires an AWS credential -- now your devs need to have AWS setup to work in the repo, and you need to make sure that they have appropriate permissions to the S3 bucket.
- For a developer with prior AWS experience, this might be easier to learn than a repo with many ML-specific tools or platforms.
- Terraform adds another programming language and way of thinking. If I could do it again I'd try replacing that part with CDK so that devs don't need to learn another infrastructure language.
- API gateway and Lambda can be challenging to understand, and aren't great technologies for junior developers in my experience.
- The use of "dvc repro" might not be worth the effort to learn it.
- Also in my opinion it's not quite documented enough for a junior dev.
- The parameters to the Lambda handler are hard to learn in my opinion, because there's no autocomplete for the data structure. [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.8.0/) can help with this, but adds another dependency.

**Will developers face significant toil while using this repo?**

While the previous subsection was about new developers, this is about the day to day experience of experienced developers.

- Are there situations that might require multiple PRs across repos? Training, serving, and infrastructure are all in the same repo so major changes can be made in a single, well-tested PR. On the other hand, it's likely that this code is being called by another repo that isn't shown, and changes involving the JSON input shape, for example, may require PRs across repos.
- Would this repo work nicely with security scanners such as [depandabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/)? In the past I've had challenges in easily updating ML packages flagged by dependabot. With this repo setup it's possible to configure dependabot to open PRs with new dependencies, build updated models, and test that they work in the service. If the PR passes we can simply merge it to update dependencies.
- Although deployment takes 4-5 minutes, it'd be better if it took closer to 1 minute. Fortunately Github Actions gives us time tracking by stage so we can investigate further. For example, it takes a little over 1 minute just to install DVC and CDK every time. Running the CDK pipeline including the Docker build takes about 3 minutes.

**Any security concerns?**

I'm not a security professional but I've been involved in enough reviews to check for the basics.

- IAM safety for the Lambda role? CDK automatically creates a minimal IAM role for us. Even if an attacker finds a way to run arbitrary code inside of our Lambda, the role doesn't have permissions to actually do much.
- IAM safety for the Github Actions user? This user has a fair amount of permissions and an attacker could do some harm if they had access. Github Actions Secrets are pretty secure though. The biggest typical problem is that I'd need to rotate the IAM credentials manually if they were leaked.
- If you're adapting this to work with sensitive training data, Github Actions might not be an option.
- The API is completely open to the world. If the model is highly unique and valuable, you don't want others to probe it indiscriminately. Auth and/or IP filtering can help.
- pickle files allow arbitrary code execution. But to write those pickle files, someone would need write access to your S3 bucket and would need to trigger a redeploy from Github. Pickle files are an unlikely attack vector of choice in this system.
- If there are vulnerabilities in the Docker image, it won't be updated until the next deployment. This is one disadvantage of using Docker for lambda -- we're the ones managing these system dependencies rather than AWS managing them like they do for zip-file lambdas.

#### Concerns in an actual company

If you're building a system professionally, this repo isn't enough of a template. This is a list of considerations I had in industry:

- Endpoint security (auth, secret management, IP restrictions, etc)
- Endpoint stability (DNS)
- Endpoint versioning -- If the input or output data structure will change in a way that isn't backwards-compatible, you may need to support multiple data structures and have a version of the endpoint itself.
- CORS when it's being integrated with a frontend served from a different domain, and also latency optimization relating to CORS
- Private PyPI inside Docker, if you use any internal modules
- Multiple deployment stages: dev, staging, prod
- Integration testing, end-to-end testing, and unit testing for any business logic
- Provisioned concurrency, setup to warm up Lambda *before* the API gateway switches to the new version so that we have zero downtime
- Dashboards and alarms
- Training data versioning, data updates, and data testing -- If you're getting new data over time there's a need for a whole pipeline before training.

Now that I'm thinking about the business, it's a good time to mention the big picture. When you're writing an API it's a piece of a larger system. I've seen significant harm caused by focusing too much on just one repo and too little on the code that calls the API. For example, we could change our API without telling anyone and it may bring down our product.

Likewise, it's good to consider the experience of the developers using our API, such as whether it's easy to learn and use. Others have covered the topic of developer experience for APIs better than I can:

- [Ask a DevExpert: What Makes a Good API? (Adobe, 2018)](https://blog.developer.adobe.com/ask-a-devexpert-what-makes-a-good-api-93fc74d83428)
- [Best Practices in API Design](https://swagger.io/resources/articles/best-practices-in-api-design/) (Swagger)
- [5 Examples of API Documentation With Great Developer Experience (Nordic APIs, 2022)](https://nordicapis.com/5-examples-of-api-documentation-with-great-developer-experience/)
- [Awesome Developer Experience](https://github.com/workos/awesome-developer-experience)

If you're deploying the service into the same AWS account as other services, there are some additional considerations:

- Is the service named and tagged so that you can audit your AWS bill easily? I'd suggest at least tagging all resources with the team that produced them.
- If you don't have Lambda concurrency limits, keep in mind that all Lambdas in the same account and region share a concurrency limit. So if your Lambda is using 999 concurrency and the limit is 1000, only 1 other Lambda in the company can be running at a time and others will be throttled. (I say this from a real experience of production Lambdas being throttled due to a logging service eating up our concurrency.)

#### Priorities to fix

I covered a lot of problems with this example repo. In industry we often can't fix everything we want to, at least not right away. So we have to prioritize what to improve first.

Prioritization should be guided by the business needs, user needs, and how your service is integrated into the product. If this were a mission-critical service dealing with private data, that's very different than a nice-to-have service that can't bring down the product. If it's an API used by external developers that's very different than an internal API. If it's a service that supports 100,000 requests per hour that's different than 100 requests per hour. And so on.

The following is an example prioritization that might make sense for a small startup:

**High priorities**

- A domain name, so that we don't accidentally cause an outage when we change API gateway
- Provisioned concurrency so that there's less downtime when deploying updates
- Talk to the people integrating the API if it's not you!
- Any required compliance

**Medium priorities**

- IP filtering, auth, and/or your security of choice -- This could range high to low depending on the application though
- Alarms for outages -- This could range high to low depending on the application
- True zero-downtime deployments

**Low priorities**

- Everything else

------------------------------------------------------------------------

### Alternatives

I also tried a few alternatives and I'll briefly mention what I found.

#### [Deploy to AWS ECS](https://github.com/ktrnka/mlops_example_ecs)

AWS Elastic Container Service (ECS) is a better option than Lambda for most people. It's always on, so you don't need to worry about the time it takes to load your model when booting. The disadvantage of ECS is that it's tricky to get autoscaling setup right and it can be more expensive.

#### [Deploy with Cortex.dev](https://github.com/ktrnka/mlops_example_cortex)

I found [Cortex.dev](https://www.cortex.dev/) to be delightfully fast and easy. The deployment itself was much faster than anything else, and not much more complex than Heroku. I remember thinking at the time my security team might not like some aspects of the deployment though.

#### [Model versioning with git-lfs on Github](https://github.com/ktrnka/mlops_example_github_lfs_heroku)

I started off using git-lfs for model versioning and Heroku free tier for deployment. I was curious to use Github as the git-lfs provider after struggling with an alternative at work.

Well, I learned why we didn't use Github's git-lfs! When you hit the LFS quota your repo is locked until you buy more quota or delete the repo. Last I checked, Github doesn't have a way to automatically increase your quota so you're relying on people manually upgrading on the website periodically.

### Things I didn't get to

There are so many MLOps tools these days! For each library, tool, or platform I used, there are dozens of alternatives. I've heard good things about kubeflow for instance and it might be a good time to re-evaluate Sagemaker.

I've also seen some people deploy models with code using Python packaging. That seems like a nice way to package code, data, and dependencies together.

### Conclusions

I hope I was able to clarify common concepts in machine learning web services!

Although I used AWS Lambda in this example, it was mainly due to curiosity. Please don't interpret this post as an endorsement of Lambda for machine learning services. Whether Lambda is a good option will depend on your needs.

Also keep in mind this might serve as a guide for a small startup but I doubt it's ready for operating at a larger scale. And I surely left out some parts of typical MLOps work, such as support for experimentation.

------------------------------------------------------------------------

Thanks for reading! If there were parts of the article you found confusing, please let me know.
