<p align="center">
    <a href="https://codecov.io/github/ajauniskis/url-shortener" > 
    <img src="https://codecov.io/github/ajauniskis/url-shortener/branch/feature/init/graph/badge.svg?token=T3JC9SMO7H"/> 
    </a>
    <a href="https://github.com/ajauniskis/url-shortener/actions?query=branch%3Amain+" target="_blank">
        <img src="https://github.com/ajauniskis/url-shortener/actions/workflows/workflow.yaml/badge.svg?branch=main">
    </a>
</p>

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
