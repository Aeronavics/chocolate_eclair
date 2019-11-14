# chocolate_eclair

WebODM docker-compose commands

Base commands:\n
WebODM:\n
docker-compose -f docker-compose-WebODM.yml

nodeodm:\n
docker-compose -f docker-compose-nodeodm.yml

nodemicmac:\n
docker-compose -f docker-compose-nodemicmac.yml

To start WebODM without nodes:\n
docker-compose -f docker-compose-WebODM.yml start || docker-compose -f docker-compose-WebODM.yml up -d


To start WebODM with nodes:\n
change WO_DEFAULT_NODES in .env to the number wanted
docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm start || docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm up -d --scale node-odm=$default_nodes

To start WebODM with micmac nodes:\n
change WO_DEFAULT_NODES in .env to the number wanted
docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm -f docker-compose-nodemicmac.yml start || docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm -f docker-compose-nodemicmac.yml up -d --scale node-odm=$default_nodes


To stop:\n
docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm -f docker-compose-nodemicmac stop

To tear down:\n
docker-compose -f docker-compose-WebODM.yml -f docker-compose-nodeodm -f docker-compose-nodemicmac down --remove-orphans
