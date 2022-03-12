# Serverless REST API for Tasks Mgmt

This repository contains the definition of a Serverless service that implements the requirements 
specified by Empatica in the second assignment described in the interview assignment doc. 

The service exposes an HTTP REST API to manage "tasks" performing CRUD operations on a database.

## Repo Structure

The repository is structured TODO.

## Service Structure

## Local Environment Setup

```bash
npm install -g serverless
```

## Service Deployment

In order to deploy the endpoint simply first install the needed plugins.

```bash
serverless plugin install -n serverless-python-requirements
```

Then deploy the service.

```bash
serverless deploy [--aws-profile=<your-aws-profile-name>] [--region=<aws-region-name>]
```

## Service Testing

You can create, retrieve, or delete tasks with the following commands:

### Create a Task

```bash
curl -X POST -u <username>:<password> https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<env>/tasks --data '{ "description": "Complete Empatica assignment #02" }'
```

No output

### List all Tasks

```bash
curl -u <username>:<password> https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<stage>/tasks 
```

Example output:
```bash
[{"description":"Complete Empatica assignment #02","id":"ac90feaa11e6-9ede-afdfa051af86","createdAt":1479139961304}]
```

### Delete a Task

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE -u <username>:<password> https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<stage>/tasks/<id>
```

No output

## Service improvements

### Basic Authorizer

Currently, "username" and "password" are stored as environment variables of the authorizer lambda function.
Two suggestions here are reported:
- increasing security of the environment variables using a KMS key to cipher them, as result only specific AWS IAM Users
  could see the values of the variables
- moving sensitive information into Secrets Manager and let the authorizer lambda function retrieve the values. 
  WARNING: since secrets manager could have relevant costs it is suggested to "cache" inside the lambda function the 
  retrieved values. To obtain this result put the reading from secrets manager operation at the very beginning of lambda 
  function code (before handler code)

### ES Domain

- For real production domains it is suggested to use dedicated master nodes (3 of them) and more than 1 data node.

### API Gateway Logging

- TODO

### Environment Mgmt

The serverless.yml template is not differentiating resources configuration (such as: Lambda Function MEM, ES Domain 
nodes) per environment.
This approach should be improved using native Cloudformation "Mapping" strategy, or other Serverless tool features, 
correctly dimensioning resources considering the target environment.