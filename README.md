# Serverless REST API for Tasks Mgmt

This repository contains the definition of a Serverless service named "tasks-manager" that implements the requirements 
specified by Empatica in the second assignment described in the interview assignment [doc](doc/assignment.pdf). 

The service exposes an HTTP REST API to manage "tasks" performing CRUD operations on a database.

## Repo Structure

The repository contains the following resources:

TODO: insert repo structure with descriptions

## Service Architecture 

TODO: insert link to architecture image

## Service Deployment

### Prerequisites

To deploy "tasks-manager" service it is needed ot have the following tools installed on the computer:

- [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [Serverless](https://www.serverless.com/framework/docs/getting-started)
- [Docker](https://www.docker.com/get-started)
  - docker daemon must be up&running during serverless packaging process

### Deployment

Install una-tantum the needed serverless plugins:

```bash
serverless plugin install -n serverless-python-requirements
```

Deploy the service specifying the needed parameters.

```bash
serverless deploy [\]
  [--stage=<stage_name> \]
  [--username=<basic_auth_usr> \]
  [--password=<basic_auth_pwd> \]
  [--aws-profile=<your-aws-profile-name> \]
  [--region=<aws-region-name>]
```

WARNING: it is possible that the deployment process could require more than 30min. This huge time is due to the 
initialization of the ElasticSearch domain.

WARNING: if the serverless client reports an error message regarding "timeout" issue (or similar) after deploy command 
has been launched, please check that the corresponding cloudformation stack on aws is proceeding with the update.
Cloudformation Stack name: <service_name>-<stage_name>"

Below the default values for some optional attributes reported above are listed:

- stage=dev
- username=<stage_name>
- password=password

## Service Testing

### REST API

You can create, retrieve, or delete tasks with the following commands:

#### Create a Task

```bash
curl -X POST -u <basic_auth_usr>:<basic_auth_pwd> "https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<stage_name>/tasks" --data '{ "description": "Complete Empatica assignment #02" }'
```

No output

#### List all Tasks

```bash
curl -u <basic_auth_usr>:<basic_auth_pwd> "https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<stage_name>/tasks[?limit=<integer>&next_page=<next_page string obtained in previous response>]" 
```

Example output:
```bash
{"tasks": [{"createdAt": "1647166390.7805717", "description": "this is the first task", "id": "2f96daa9-a2b6-11ec-960a-3924964e7875"}], "size": 1, "next_page": null}
```

#### Delete a Task

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE -u <basic_auth_usr>:<basic_auth_pwd> "https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<stage_name>/tasks/<id>"
```

No output

### Logs review

All the lambda function logs are collected on cloudwatch dedicated log groups (retention 1 day) and automatically 
streamed to a dedicated elasticsearch domain.

To see the logs collected on ES it is needed to use a Node.js command line tool since the ES domain cannot publicly
accessible.

#### Accessing ES Domain

- install [aws-es-kibana](https://github.com/santthosh/aws-es-kibana) tool

```bash
npm install -g aws-es-kibana
```

- access the AWS Account and region in which the service "tasks-manager" has been deployed
- go to Amazon OpenSearch Service dashboard and open the details of the ES domain deployed within "tasks-manager" 
  service
- copy the Domain URL without selecting the "http(s)://" prefix 
  (e.g. "search-tasks-manager-qa-logsstore-5pk64363ictlcbd7b5wpo4mqaq.eu-west-1.es.amazonaws.com")
- go back to the command line and open a connection to the ES domain

```bash
AWS_PROFILE=<your_aws_profile_name> aws-es-kibana <ES domain URL> --port <any available port on your computer: 9210>
```

- copy the provided Kibana URL in your browser, you're in!

#### First Kibana set-up: Index Pattern creation

WARNING: it is suggested to invoke few times the REST API exposed by tasks-manager service before defining any Index 
Pattern on Kibana. In this way the ES domain would be already populated with some logs.

After you've accessed Kibana dashboard for the first time you need to define an "Index Pattern" to have a look at the
stored logs.

- open the left menu
- open "Stack Management" window
- click on "Index Patterns"
- click on "Create Index Pattern"
  - you should already see that an index named "tasks-manager-<stage>-logs-YYYY-MM-DD" is present
- specify "tasks-manager-<stage>-logs*" as index pattern
- click on "Next Step"
- select "@timestamp" attribute as "Time Field"
- click on "Create Index Pattern"
- mark this index pattern as default clicking on the star icon on the top right

Once you've created the index pattern, you can go back to the "Discover" page opening the side menu again.

#### Discover logs messages

If you've already set-up the correct index pattern ([guide](#first-kibana-set-up-index-pattern-creation)), access 
the "Discover" section of the Kibana dashboard and have a look at the collected logs.

WARNING: if you don't see any log in the Discover page, and you've already invoked REST API of tasks-manager service 
try to extend the time range (Kibana default 15min) or invoke again the REST API (at least 1 min latency between 
lambda functions execution and logs writing on ES is present).

## Service improvements

This section reports some improvements that should be applied to the current solution in order to have better 
maintainability, more security, and increased observability. 

### Basic Authorizer

Currently, "basic_auth_usr" and "basic_auth_pwd" are stored as environment variables of the authorizer lambda function.
Two suggestions here are reported:
- increasing security of the environment variables using a KMS key to cipher them, as result only specific AWS IAM Users
  could see the values of the variables
- moving sensitive information into Secrets Manager and let the authorizer lambda function retrieve the values. 
  WARNING: since secrets manager could have relevant costs it is suggested to "cache" inside the lambda function the 
  retrieved values. To obtain this result put the reading from secrets manager operation at the very beginning of lambda 
  function code (before handler code)

### ES Domain

- For real production domains it is suggested to use dedicated master nodes (3 of them) and more than 1 data node.
- A more secured network configuration should be applied, see [VPC](#vpc-configuration) section.
- indices name in this service are designed to have a daily rotation (index name suffix: YYYY-MM-DD). In addition to 
  the naming convention, a policy in ES should be configured in order to delete older incides after the desired 
  retention period (e.g. 30 days) is expired.


### API Gateway Logging

Currently, only Lambda Function's log groups have subscriptions forwarding logs to the Elastic Search domain.
It would be possible to specify dedicated CloudWatch log groups also for API Gateway resources and forward these  
logs to ES.

### VPC configuration

The implemented solution does not use any dedicated VPC set-up, all the resources are created in the default VPC which 
has public subnets.

It is recommended to create ad hoc network configurations based on project requirements. 

### Environment Mgmt

The serverless.yml template is not differentiating resources configuration (such as: Lambda Function MEM, ES Domain 
nodes) per environment.
This approach should be improved using native Cloudformation "Mapping" strategy, or other Serverless tool features, 
correctly dimensioning resources considering the target environment.