---
layout: post
title: Serving machine learning models
date: 2019-08-13
---

Survey of options for web services with machine learning models in Python.

It's challenging to operate and maintain machine learning models in a production system. This post will survey the options for machine learning web services with Python. By the end of this post, you should have an understanding of your options and why you might pick one or another.

The main challenge is that the code and data must be compatible. For example, if you add a new feature to your model it needs changes to both the code and the model data. New code may crash with older models or vice versa.

### Goals

- Continuous deployment -- We shouldn't do much manual work to deploy an update.
- Continuous integration -- The model and code should be tested together before deployment. There should be no risk of model-code incompatibility on deployment.
- Risk-free reverting -- When we detect a bug and roll back to an older version, there's no risk of model-code incompatibility.

### Assumptions

- git for code versioning
- Jenkins for CI/CD (or similar)
- You have tests for your model endpoints that are run in Jenkins
- You already have a file format to save and load your model
- You're deploying using Docker or something similar

### Options

#### git

You can simply commit the model to your repo in git. We started this way and it works for a while, but checking out a repo, branching, and updating can be very slow because it downloads every version of every file.

If you make a mistake like this and switch later, it's still in your git history and will slow things down forever. Unless you rewrite git history or start over.

#### [git-lfs](https://git-lfs.github.com/) (large file storage)

This greatly reduces time to checkout, branch, and update compared to git. You're updating models with familiar commands like `git add`, `git push`, and `git pull`. It's a good option for a small startup.

Notes on LFS providers

- If you use github, they have an account-level limit on LFS storage and you need to buy data packs when you run out of storage space. You'll need to be proactive to ensure that your developers aren't blocked on pushing commits.
- You can use different storage providers for git and git-lfs. The LFS provider can be operated through services like Artifactory or you can create an AWS Lambda to use S3 for storage. However, the configuration for a secondary provider for LFS can be complex, especially in a CI/CD pipeline like Jenkins -- commands like `checkout scm` don't work anymore.

Your team will all need to install git-lfs onto their machines then configure git to use it. Your repo will need to be configured as well and the `.gitattributes` file should be tracked in regular git.

#### [lazydata](https://github.com/rstojnic/lazydata)

This is a Python module for data storage and it lazy-loads files from whatever provider you configure, like S3.

Advantages

- You can modify the code without downloading all of the data if necessary.
- S3 is fast and cheap.
- Less setup than other methods.

Disadvantages

- You'll implement loading to happen on boot or on first request, which adds a little latency.
- You need to run additional commands like `lazydata push` after running `git push` to ensure that it's pushed to S3.
- If you have a pipeline with dev/staging/prod, lazydata would be using the same S3 bucket for all three environments which violates best practices for devops.
- Python only

If you're adding lazydata to a repo, you need to install via `pip`, run `lazydata init`, configure the remote (S3), make sure the config file is added to git, then push. For adding new files, you'll need to either write them from Python with `track` or else add them manually via the command line. When you modify anything tracked by lazydata you'll need to do `lazydata push`.

When teammates just want to read the files, they don't need to do anything beyond installing it. If you're using `requirements.txt` or `Pipfile` it's easy.

#### [DVC](https://dvc.org/) (data version control)

Like lazydata, this can use S3 for versioning and storing your large files and keeping them in sync with git. DVC works more like a secondary git command though.

It's also designed for a much more general machine learning workflow that includes training data and experimentation. That won't help with deployment but may be important to you.

Advantages

- Language-agnostic

Disadvantages

- Need to run additional commands like `dvc add`, `dvc push`, `dvc pull`. It's slightly more work than lazydata.

The process for adding to a new repo is similar to lazydata -- you install it via pip, run `dvc init`, setup the remote, and then commit the new files. When adding a file you run `dvc add`. And then when you commit via git you also run `dvc push`.

When teammates want to read the files they need to install it via `requirements.txt`/`Pipfile` and then run `dvc pull` after cloning the repo.

#### Amazon Sagemaker

Sagemaker works very differently -- you aren't taking your existing Flask service and standing it up so much as you change your model training and serving process to fit Sagemaker. They manage model versions in S3 for you and manage the hosting of the models as well.

Azure and Google Cloud have similar services.

Advantages

- Very easy if the provided model types are suitable for your problem
- Autoscales your model endpoint based on demand

Disadvantages

- AWS authentication for the model endpoint may not suit your needs
- You'll need to understand the AWS ecosystem much more, especially for security
- It makes custom model serving a bit harder

The setup for this is more extensive -- see [Sagemaker docs](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-hosting.html).

### Briefly mentioned

#### Pickle files

Pickle is the easy way to serialize machine learning models. Popular libraries like scikit-learn and Keras are compatible with Pickle. You should pin the versions of your dependencies because the format is version-specific for libraries like joblib.

#### scikit-learn pipelines

If you're using scikit-learn in any way, I recommend using pipelines. They bundle together all preprocessing with the model itself and you save it as a single file. This eliminates a common source of error -- different preprocessing for training and testing/serving.

#### [ONNX](https://onnx.ai)

ONNX is an open source neural network serialization format. There are many efficient implementations of model serving using ONNX. I looked into it earlier this year but found only minimal support for text processing -- it's really mainly for image processing.

#### Weights database

You could serialize your model to a database but then you need to manage the format and versions yourself. The only advantage I've seen is that you can put word embeddings in a database and only load the few words in the input, rather than keeping the entire vocabulary in memory.

#### AWS Lambda

Lambda is a great way to achieve scalability and reduce costs for your web service. But you need to package up all of the non-standard Python dependencies into a small package. You probably won't have room left in the package for the model itself. Luckily, you can download your model from S3 on demand. Lazydata is a good solution for this.

### Recommendations

If Sagemaker meets your needs, that's what I'd recommend because you get model versioning and autoscaling of your service.

If Sagemaker doesn't meet your needs, I'd recommend `dvc` with S3 for storage.

If you're in a rush and have github admin, git-lfs is reasonable.
