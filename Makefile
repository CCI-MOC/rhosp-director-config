CUSTOM_ROLES = \
	       roles/ControllerDeployedServer.yaml \
	       roles/ComputeDeployedServer.yaml \
	       roles/NetworkerDeployedServer.yaml

CONTROLLER_SRC_ROLES = \
	    roles/ControllerOpenstack.yaml \
	    roles/Database.yaml \
	    roles/Messaging.yaml

ENVIRONMENTS = \
	       templates/credentials.yaml \
	       templates/fencing.yaml

%.yaml: %.yaml.in
	ansible-playbook \
		-e templates=$(TEMPLATES) \
		-t $(notdir $@) \
		generate-deploy-files.yaml

all: environments roles_data.yaml

environments: $(ENVIRONMENTS)

roles_data.yaml: $(CUSTOM_ROLES)
	openstack overcloud roles generate --roles-path roles -o $@ \
		ControllerDeployedServer \
		ComputeDeployedServer \
		NetworkerDeployedServer

clean:
	rm -f $(ENVIRONMENTS)
