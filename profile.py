""" Ubuntu 20.04 Optional Kubernetes Cluster w/ OpenWhisk optionally deployed with a parameterized
number of nodes.
Instructions:
Note: It can take upwards of 10 min. for the cluster to fully initialize. Thank you for your patience!
For full documentation, see the GitHub repo: https://github.com/CU-BISON-LAB/cloudlab-openwhisk
Output from the startup script is found at /home/openwhisk-kubernetes/start.log on all nodes
"""

import time

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec

BASE_IP = "10.10.1"
BANDWIDTH = 10000000
IMAGE = 'urn:publicid:IDN+utah.cloudlab.us+image+mlhrc-PG0:owimagecreator:1'

# Set up parameters
pc = portal.Context()
pc.defineParameter("nodeCount", 
                   "Number of nodes in the experiment. It is recommended that at least 3 be used.",
                   portal.ParameterType.INTEGER, 
                   3)
pc.defineParameter("nodeType", 
                   "Node Hardware Type",
                   portal.ParameterType.NODETYPE, 
                   "xl170",
                   longDescription="A specific hardware type to use for all nodes. This profile has primarily been tested with m510 and xl170 nodes.")
pc.defineParameter("startKubernetes",
                   "Create Kubernetes cluster",
                   portal.ParameterType.BOOLEAN,
                   True,
                   longDescription="Create a Kubernetes cluster using default image setup (calico networking, etc.)")
pc.defineParameter("deployOpenWhisk",
                   "Deploy OpenWhisk",
                   portal.ParameterType.BOOLEAN,
                   True,
                   longDescription="Use helm to deploy OpenWhisk.")
# Below two options copy/pasted directly from small-lan experiment on CloudLab
# Optional ephemeral blockstore
pc.defineParameter("tempFileSystemSize", 
                   "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 
                   100,
                   advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files. 0 GB indicates maximum size.")
pc.defineParameter("numInvokers",
                   "Number of Invokers",
                   portal.ParameterType.INTEGER,
                   1,
                   advanced=True,
                   longDescription="Number of OpenWhisk invokers set in the mycluster.yaml file, and number of nodes labelled as Openwhisk invokers. " \
                           "All nodes which are not invokers will be labelled as OpenWhisk core nodes.")
pc.defineParameter("invokerEngine",
                   "Invoker Engine",
                   portal.ParameterType.STRING,
                   "kubernetes",
                   advanced=True,
                   legalValues=[('kubernetes', 'Kubernetes Container Engine'), ('docker', 'Docker Container Engine')],
                   longDescription="Controls how the OpenWhisk invoker creates containers. Using docker indicates that you need one invoker per invoker " \
                           "node and the use of extra storage (temporary file system), since all runtime docker images are preloaded on each invoker " \
                           "node when OpenWhisk is deployed.")
params = pc.bindParameters()

# Verify parameters
if not params.startKubernetes and params.deployOpenWhisk:
    perr = portal.ParameterWarning("A Kubernetes cluster must be created in order to deploy OpenWhisk",['startKubernetes'])
    pc.reportError(perr)

pc.verifyParameters()
request = pc.makeRequestRSpec()

def create_node(name, nodes, lan):
  # Create node
  node = request.RawPC(name)
  node.disk_image = IMAGE
  node.hardware_type = params.nodeType
  
  # Add interface
  iface = node.addInterface("if1")
  iface.addAddress(rspec.IPv4Address("{}.{}".format(BASE_IP, 1 + len(nodes)), "255.255.255.0"))
  lan.addInterface(iface)
  
  # Add extra storage space
  bs = node.Blockstore(name + "-bs", "/mydata")
  bs.size = str(params.tempFileSystemSize) + "GB"
  bs.placement = "any"
  #bs2 = node.Blockstore(name + "-bench-bs", "/benchdata")
  #bs2.dataset = "urn:publicid:IDN+utah.cloudlab.us:mlhrc-pg0+imdataset+sebs-bench"
  #bs2.size = "50GB"
  #bs2.placement = "any"
  # Add to node list
  nodes.append(node)

nodes = []
lan = request.LAN()
lan.bandwidth = BANDWIDTH

# Create nodes
# The start script relies on the idea that the primary node is 10.10.1.1, and subsequent nodes follow the
# pattern 10.10.1.2, 10.10.1.3, ...
for i in range(params.nodeCount):
    name = "ow"+str(i+1)
    create_node(name, nodes, lan)

# Iterate over secondary nodes first
for i, node in enumerate(nodes[1:]):
    node.addService(rspec.Execute(shell="bash", command="/local/repository/start.sh secondary {}.{} {} > /home/cloudlab-openwhisk/start.log 2>&1 &".format(
      BASE_IP, i + 2, params.startKubernetes)))
    node.addService(rspec.Execute(shell="bash", command="sudo mkdir /mydata/workspace; sudo chown hwnam831 /mydata/workspace"))
    node.addService(rspec.Execute(shell="bash", command="git clone https://github.com/hwnam831/jRAPL-percore /mydata/workspace/jrapl"))

# Start primary node
nodes[0].addService(rspec.Execute(shell="bash", command="/local/repository/start.sh primary {}.1 {} {} {} {} {} > /home/cloudlab-openwhisk/start.log 2>&1".format(
  BASE_IP, params.nodeCount, params.startKubernetes, params.deployOpenWhisk, params.numInvokers, params.invokerEngine)))
nodes[0].addService(rspec.Execute(shell="bash", command="git clone https://github.com/spcl/serverless-benchmarks /mydata/workspace/sebs"))
nodes[0].addService(rspec.Execute(shell="bash", command="python3 ~/sebs/install.py --openwhisk"))
nodes[0].addService(rspec.Execute(shell="bash", command=". ~/sebs/python-venv/bin/activate; \
  /mydata/workspace/sebs/sebs.py storage start minio --output-json /mydata/workspace/sebs/config/minio.json;\
  jq --argfile file1 /mydata/workspace/sebs/config/minio.json '.deployment.openwhisk.storage = $file1 ' /mydata/workspace/sebs/config/example.json > /mydata/workspace/sebs/config/ow.json"))

pc.printRequestRSpec()
