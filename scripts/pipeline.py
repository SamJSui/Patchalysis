from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.network import Gunicorn
from diagrams.onprem.client import Client
from diagrams.onprem.database import MongoDB
from diagrams.aws.compute import ElasticBeanstalkDeployment

graph_attr = {
    "fontsize": "18",
    "bgcolor": "transparent",
}

node_attr = {
    "fontsize": "18",
    "shape": "ellipse",
    "style": "filled",
    "fillcolor": "transparent",
}

with Diagram("", show=False, graph_attr=graph_attr, node_attr=node_attr, direction='TB'): # Leave the title blank to avoid taking up more vertical space
    patchalysis = Custom('Patchalysis', './assets/patchalysis.png')

    scraper = Custom('Data Collection', './assets/scraper.png')
    text_analysis = Custom('Text Analysis', './assets/find.png')
    modeling = Custom('Modeling', './assets/cluster.png')
    deployment = ElasticBeanstalkDeployment('Web Deployment')

    patchalysis >> scraper
    patchalysis >> text_analysis
    patchalysis >> modeling
    patchalysis >> deployment
