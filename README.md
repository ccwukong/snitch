# snitch
snitch is a CLI tool that helps you do health check, API contract validation and load testing agaist your microservices.

There's no tendancies to replace your existing testing tools, but rather provides a convenient way to check your microservices on demand.
## Main features
- Health check on every endpoint
- API Contract validation
- Concurrency testing
- More to come

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
      "{{skyweatherToken}}": "the access token string",
      "{{apiKey}}": "api key string",
      ...
    },
    "header":{
      "Authorization":"{{skyweatherToken}}", // the placeholder string will be replaced by the metadata values automatically by the script
      "x-api-key":"{{apiKey}}"
    }
  }
}
```

Once you have the config JSON file ready, you can run this in your commandline prompt:

```console 
python main.py -p your_config_json_file_path

```