from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.network import Gunicorn
from diagrams.onprem.client import Client
from diagrams.onprem.database import MongoDB
from diagrams.aws.compute import ElasticBeanstalkDeployment

graph_attr = {
    "fontsize": "32",
    "bgcolor": "transparent",
    "pad": "0.5"
}

cluster_attr = {
    "fontsize": "16",  # Updated fontsize for clusters
    "bgcolor": "lightblue",
    "margin": "10"
}

node_attr = {
    "fontsize": "12",
    "shape": "ellipse",
    "style": "filled",
    "fillcolor": "transparent",
    "height": "1.0",
    "width": "1.5"
}

with Diagram("Pipeline", show=False, graph_attr=graph_attr, node_attr=node_attr):
    user = User('User')
    client = Client('Browser')
    patchalysis = Custom('Patchalysis', './assets/logo.png')

    client >> user
    user >> client
    client >> patchalysis

    with Cluster('Data Collection', graph_attr=cluster_attr) as data_collect:
        beautifulsoup = Custom('BeautifulSoup', './assets/beautifulsoup.png')
        documents = Custom('Patch Notes', './assets/documents.png')
        stats = Custom('Stats', './assets/percentage.png')
        mongodb = MongoDB('MongoDB')
        beautifulsoup >> documents >> mongodb
        beautifulsoup >> stats >> mongodb

    patchalysis >> beautifulsoup

    with Cluster('Data Processing', graph_attr=cluster_attr) as data_process:
        processing = Custom('Processing', './assets/processing.png')
        mongodb = MongoDB('MongoDB')
        mongodb >> processing

    patchalysis >> mongodb

    with Cluster('Deployment', graph_attr=cluster_attr) as deployment:
        eb = ElasticBeanstalkDeployment('AWS EB')
        gunicorn = Gunicorn('Gunicorn')
        browser = Custom('patchalysis.com', './assets/browser.png')
        eb >> gunicorn >> browser
    
    patchalysis >> eb
