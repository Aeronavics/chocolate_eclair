# chocolate_eclair

WebODM docker-compose commands

Base command:
docker-compose -f docker-compose-WebODM.yml

To start WebODM:
docker-compose -f docker-compose-WebODM.yml start || docker-compose -f docker-compose-WebODM.yml up -d

To stop:
docker-compose -f docker-compose-WebODM.yml stop

To tear down:
docker-compose -f docker-compose-WebODM.yml down --remove-orphans
