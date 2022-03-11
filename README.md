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
curl -X POST https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/<env>/tasks --data '{ "description": "Complete Empatica assignment #02" }'
```

No output

### List all Tasks

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/todos
```

Example output:
```bash
[{"description":"Complete Empatica assignment #02","id":"ac90feaa11e6-9ede-afdfa051af86","createdAt":1479139961304}]
```

### Delete a Task

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE https://XXXXXXX.execute-api.<aws-region-name>.amazonaws.com/dev/tasks/<id>
```

No output