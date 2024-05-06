from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.network import Gunicorn
from diagrams.onprem.client import Client
from diagrams.aws.compute import ElasticBeanstalkDeployment

graph_attr = {
    "fontsize": "18",
    "bgcolor": "transparent",
}

cluster_attr = {
    "fontsize": "16",
    "bgcolor": "lightblue",
}

node_attr = {
    "fontsize": "16",
    "shape": "ellipse",
    "style": "filled",
    "fillcolor": "transparent",
}

with Diagram("", show=False, graph_attr=graph_attr, node_attr=node_attr):
    client = Client('Local Computer')

    beautifulsoup = Custom('Data Scraping', './assets/beautifulsoup.png')
    patch_notes = Custom('Patch Notes', './assets/gear.png')
    database = Custom('Database', './assets/database.png')

    client >> beautifulsoup
    beautifulsoup >> client
    client >> database
