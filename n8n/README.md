# n8n integration

The n8n workflow is intentionally kept separate from the GitHub worker code.

n8n should orchestrate and persist state; GitHub Actions should perform
deterministic compute-heavy work.

Do not copy credentials into GitHub files. Store credentials in n8n/GitHub
secret stores and pass only short-lived or required values to workers.
