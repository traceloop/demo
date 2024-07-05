## A full demo of Traceloop observability with LlamaIndex on our docs

See https://traceloop.com/demo

1. Install:

```python
poetry install
```

2. Set up the environment:

```python
export GITHUB_TOKEN=<your github token> # Needed to index our docs from github.com/traceloop/docs
export OPENAI_API_KEY=<your openai api key>
export TRACELOOP_API_KEY=<your traceloop api key>
```

You can connect OpenLLMetry to other platform by following one of the guides [here](https://www.traceloop.com/docs/openllmetry/integrations/introduction).

3. Run the demo locally like this:

```python
poetry run streamlit run demo/app.py
```
