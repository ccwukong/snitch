# snitch <img src="https://img.shields.io/badge/pypi-v0.1.28-green" /> <img src="https://img.shields.io/badge/Tested%20on-macOS%20Ventura-brightgreen" /> <img src="https://img.shields.io/badge/Tested%20on-Ubuntu%2022.10-brightgreen" /> 

![logo](docs/logo.png)

# Table of contents

<!--ts-->
  * [Introduction](#introduction)
  * [Main features](#main-features)
    * [Demo](#demo)
  * [Installation](#installation)
  * [Use cases](#use-cases)
  * [How this works](#how-this-works)
  * [Flags](#flags)
  * [Idempotency](#idempotency)
  * [How to contribute](#how-to-contribute)
<!--te-->

## Introduction

snitch is a CLI tool that helps you do health check, API idempotency check and more for your APIs.

This is not a replacement for your existing testing tools, but rather it provides a convenient way to check your APIs swiftly.

## Main features

- Running health check concurrently (using coroutine)
- Running Idempotency check by mixing synchronous requests and coroutines, this will be slightly slower than features run by coroutines merely(e.g. health check)
- More to come

[CHANGELOG](CHANGELOG.md)

### Demo

![Demo](docs/demo.gif)

## Installation

Install snitch via pip. Make sure you have Python 3 installed on your machine.

**❗CAUTION** The package name is **api-snitch** instead of **snitch**.

```
pip3 install api-snitch
```

Once you have the config JSON file ready, you can run this in your commandline prompt:

```
snitch -p your_config_json_file_path [-o your_output_directory]
```

### Use cases

Senario 1: I want to run all tasks(API health check and API idempotency check)

```concole
snitch -p your_config_json_file_path
```

Senario 2: I want to run the API Idempotency check task only

```concole
snitch -p your_config_json_file_path -t id
```

Senario 3: I don't have a configuration json file, and I want to create one named **config.json** using the default template and stored it in my **current directory**

```concole
snitch -i ./config.json
```

Senario 4: I want to run all tasks(API health check and API idempotency check) with all API responses printed.

```concole
snitch -p your_config_json_file_path -v
```

## How this works

snitch accepts 2 types of API contracts: Postman collection file version **>= 2.0** or OpenAPI(Swagger) file version **>= 3.0.0**.

First, you need to have a global .json file which provides all essential configurations in order to run the test. 

You can create it by running

```console
snitch -i path_to_store_the_config_json_file/your_json_file_name.json
```

Or, you can use this template:
```json
{
  "postmanCollection": {
    "version": "2.1", 
    "filePath": "absolute_path_to_the_postman_collection_json_file",
    "metadata":{ // you can put all your placeholder strings here, for instance, the placeholder string for the host of the REST endpoints
      "{{restUrl}}": "https://your_api_domain",
      "{{accessToken}}": "the access token string",
      "{{apiKey}}": "api key string",
      ...
    }
  },
  "openApi": {
    "version": "3.0.0", 
    "filePath": "absolute_path_to_the_open_api_yaml_file",
    "metadata":{
      "{{restUrl}}": "https://your_api_domain",
      "{{accessToken}}": "the access token string",
      "{{apiKey}}":"api key string",
      ...
    }
  }
}
```

## Flags

Available flags for snitch CLI commands.

| flag      | Description |
| ----------- | ----------- |
| -i      | ***OPTIONAL*** Create a new config JSON file with default template |
| --init   | same as -i        |
| -o      | ***OPTIONAL*** Your output directory for storing the test results. It has to be a directory |
| --output   | same as -o        |
| -p      | Your config JSON file path |
| --path   | same as -p        |
| -t      | ***OPTIONAL*** There are 2 tasks available:<br /> - hc (API health check)<br /> - id (API idempotency check) |
| --task   | same as -t        |
| -v      | ***OPTIONAL*** Print API responses if -v or --verbose flag is specified |
| --verbose   | same as -v        |

## Idempotency

Explanation from [https://www.restapitutorial.com/](https://www.restapitutorial.com/lessons/idempotency.html#:~:text=From%20a%20RESTful%20service%20standpoint,as%20making%20a%20single%20request.)

> From a RESTful service standpoint, for an operation (or service call) to be idempotent, clients can make that same call repeatedly while producing the same result. In other words, making multiple identical requests has the same effect as making a single request. Note that while idempotent operations produce the same result on the server (no side effects), the response itself may not be the same (e.g. a resource's state may change between requests).

> The PUT and DELETE methods are defined to be idempotent. However, there is a caveat on DELETE. The problem with DELETE, which if successful would normally return a 200 (OK) or 204 (No Content), will often return a 404 (Not Found) on subsequent calls, unless the service is configured to "mark" resources for deletion without actually deleting them. However, when the service actually deletes the resource, the next call will not find the resource to delete it and return a 404. However, the state on the server is the same after each DELETE call, but the response is different.

> GET, HEAD, OPTIONS and TRACE methods are defined as safe, meaning they are only intended for retrieving data. This makes them idempotent as well since multiple, identical requests will behave the same.

POST method usually is not idempotent, however, for applications such as online banking, digital payment etc. it is also important to keep POST method idempotent to avoid duplicated payments and transactions. It's subjected to application owners to decide whether or not idempotency is non-trival to certain POST endpoints of their services, and snitch only simply checks if same API with same parameteres returns same response or not.

## How to contribute

**Step 1**: Clone this repo

**Step 2**: Create a Python 3 virtual environment

Run the following commands under **root** directory(NOT snitch/)

```console
python3 -m venv venv

source ./venv/bin/activate
```

**Step 3**: Create a new branch, add your code and test cases, make sure nothing breaks

Run unit testing under **root** directory(NOT snitch/)
```console
tox -e py310 -- ./tests
```

**Step 4**: Test the program manually

Run the following command under **root** directory(NOT snitch/) to avoid the relative import path issue.

```console 
python3 -m snitch.main -p your_config_json_file_path [-o your_output_directory]

```

**Step 5**: Push your branch and create a PR for review

