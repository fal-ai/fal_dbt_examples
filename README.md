## Fal example dbt project

This is an example dbt project that uses [fal](https://github.com/fal-ai/fal)

To get started, install the dependency requirements:

```bash
pip install -r requirements.txt
```

Copy `profiles.yml` to `.dbt` directory:

```bash
mkdir $HOME/.dbt
cp profiles.yml $HOME/.dbt/
```

Setup up the necessary environment variables:

```bash
export KEYFILE_DIR=$HOME
export GCLOUD_PROJECT='your_gcloud_project_id'
export BQ_DATASET='your_bigquery_dataset_id'
export SLACK_BOT_TOKEN='your_slack_bot_token'
export SLACK_BOT_CHANNEL='your_slack_bot_channel'
export DD_API_KEY="your_datadog_api_key"
export DD_APP_KEY="your_datadog_app_key"
```

You can now try to run dbt and fal:

```bash
dbt seed
dbt run
fal run
```

See example details:

- [schema.yml](models/schema.yml) for model configurations
- [script examples](fal_scripts/)
- [profiles.yml](profiles.yml) for example profile
- [requirements.txt](requirements.txt)
- [fal_workflow.yml](.github/workflows/fal_workflow.yml) for example Github Action workflow

