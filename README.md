# snitch
snitch is a CLI tool that helps you do health check, API contract validation and more for your microservices.

There's no tendancies to replace your existing testing tools, but rather provides a convenient way to check your microservices on demand.
## Main features
- Health check on every endpoint concurrently (using aiohttp)
- API Contract validation
- More to come

## Installation

Install snitch via pip. 

**❗CAUTION** The package name is **api-snitch** instead of **snitch**.

```
pip install api-snitch
```

Once you have the config JSON file ready, you can run this in your commandline prompt:

```
snitch -p your_config_json_file_path
```

## Development

Run the following command under **root** directory(NOT src/snitch/) to avoid the relative import path issue.

```console 
python3 -m src.snitch.main -p your_config_json_file_path

```

## How does this work?

snitch accepts 2 types of API contracts: Postman collection file or OpenAPI(Swagger) file.

First, you need to have a global .json file which provides all essential configurations in order to run the test. You can use this template:
```json
{
  "postmanCollection": {
    "version": "2.1", 
    "collectionFilePath": "absolute_path_to_the_postman_collection_json_file",
    "metadata":{ // you can put all your placeholder strings here, for instance, the placeholder string for the host of the REST endpoints
      "{{rest_url}}": "https://your_api_domain",
      "{{accessToken}}": "the access token string",
      "{{apiKey}}": "api key string",
      ...
    },
    "header":{
      "Authorization":"{{accessToken}}", // the placeholder string will be replaced by the metadata values automatically by the script
      "x-api-key":"{{apiKey}}"
    }
  }
}
```

## TODO
- support other content-type values other than application/json
- Improve exception handling