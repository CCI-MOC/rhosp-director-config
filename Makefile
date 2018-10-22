CUSTOM_ROLES = \
	       roles/ControllerDeployedServer.yaml \
	       roles/ComputeDeployedServer.yaml \
	       roles/NetworkerDeployedServer.yaml

CONTROLLER_SRC_ROLES = \
	    roles/ControllerOpenstack.yaml \
	    roles/Database.yaml \
	    roles/Messaging.yaml

ENVIRONMENTS = templates/deploy.yaml templates/credentials.yaml

all: environments roles_data.yaml

environments: $(ENVIRONMENTS)

templates/deploy.yaml: templates/deploy.yaml.in
	ansible-playbook \
		-e templates=$(TEMPLATES) \
		-t deploy.yaml \
		generate-deploy-files.yaml

templates/credentials.yaml: templates/credentials.yaml.in
	ansible-playbook \
		-e templates=$(TEMPLATES) \
		-t credentials.yaml \
		generate-deploy-files.yaml

roles_data.yaml: $(CUSTOM_ROLES)
	openstack overcloud roles generate --roles-path roles -o $@ \
		ControllerDeployedServer \
		ComputeDeployedServer \
		NetworkerDeployedServer
