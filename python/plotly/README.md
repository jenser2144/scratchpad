# plotly-reporting-test

## Setup JupyterLab to run code
1. Update _docker_compose.yml_ (optional): Can change `container_name` and/or `JUPYTER_TOKEN` values
1. Start and build Docker container: `docker-compose up`
1. Accessing JupyterLab: In your browser, go to _http://localhost:8888_ and enter the token you defined in _docker_compose.yml_
1. To display images in JupyterLab, run the following to install an additional extension: `jupyter labextension install jupyterlab-plotly@4.14.3; pip install "jupyterlab>=3" "ipywidgets>=7.6";`

## Additional Documentation Links
### JupyterLab Setup
- [dockerhub: jupyter/datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook)
- [How to run JupyterLab on Docker](https://dev.to/juanbelieni/how-to-run-jupyterlab-on-docker-4n80)
### Plotly
- [Getting Started with Plotly in Python](https://plotly.com/python/getting-started/)
- [Bar Charts in Python](https://plotly.com/python/bar-charts/)
- [Hover Text and Formatting in Python](https://plotly.com/python/hover-text-and-formatting/)
- [Setting the Font, Title, Legend Entries, and Axis Titles in Python](https://plotly.com/python/figure-labels/)
- [Styling Plotly Express Figures in Python](https://plotly.com/python/styling-plotly-express/)
- [Indicators in Python](https://plotly.com/python/indicator/)
- [Images in Python](https://plotly.com/python/imshow/)