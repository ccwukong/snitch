![logo](docs/logo.png)
# snitch
snitch is a CLI tool that helps you do health check, API contract validation and more for your microservices.

This is not a replacement for your existing testing tools, but rather it provides a convenient way to check your APIs swiftly.

## Main features

- Running health check and contract validation concurrently (using coroutine)
- Running Idempotency check by mixing synchronous requests and coroutines, this will be slightly slower than features run by coroutines merely(e.g. health check)
- More to come

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

### Flags
| flag      | Description |
| ----------- | ----------- |
| -i      | ***OPTIONAL*** Create a new config JSON file with default template |
| --init   | same as -o        |
| -p      | Your config JSON file path |
| --path   | same as -p        |
| -o      | ***OPTIONAL*** Your output directory for storing the test results. It has to be a directory |
| --output   | same as -o        |

## Development

### Create a Python 3 virtual environment under **root** directory(NOT src/snitch/)

```console
python3 -m venv venv

source ./venv/bin/activate
```

### Run the program

Run the following command under **root** directory(NOT src/snitch/) to avoid the relative import path issue.

```console 
python3 -m src.snitch.main -p your_config_json_file_path [-o your_output_directory]

```

### Run unit testing

Run unit testing under **root** directory(NOT src/snitch/)
```console
tox -e py310 -- ./tests
```

## How does this work?

snitch accepts 2 types of API contracts: Postman collection file version >= 2.1 or OpenAPI(Swagger) file version >= 3.0.0.

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
    "collectionFilePath": "absolute_path_to_the_postman_collection_json_file",
    "metadata":{ // you can put all your placeholder strings here, for instance, the placeholder string for the host of the REST endpoints
      "{{restUrl}}": "https://your_api_domain",
      "{{accessToken}}": "the access token string",
      "{{apiKey}}": "api key string",
      ...
    },
    "header":{
      "Authorization":"{{accessToken}}", // the placeholder string will be replaced by the metadata values automatically by the script
      "x-api-key":"{{apiKey}}"
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
    },
    "header":{
      "Authorization":"{{accessToken}}",
      "x-api-key":"{{apiKey}}"
    }
  }
}
```

## TODO
- Idempotency check
- Improve exception handling