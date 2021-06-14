
# Welcome to my CDK Python project!

This was a blank project for Python development with CDK.

## Prerequisites

I suggest you try WSL and get your flavor of Linux. Follow Matt Livesey's awesome guide: [Python development using WSL 2 and Visual Studio Code](https://www.mjlivesey.co.uk/2020/08/02/vs-code-wsl2-python.html). If you insist doing your way...

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
- [AWS Account and User with Admin rights](https://portal.aws.amazon.com/billing/signup)
- [Node.js](https://nodejs.org/)
- [IDE for your programming language](https://code.visualstudio.com/)
- AWS CDK Toolkit
    ```sh
    npm install -g aws-cdk
    cdk --version
    ```
- [Python](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)

## Instructions

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
