## Setup local environment
To setup local development environment copy `.env.template` to `.env` and add your environment variables.
Create a new Deta micro in your project:
```bash
$ deta new --project <your-project-name>
```

You can deploy your app to Deta with:
```bash
$ make deploy-dev
```
