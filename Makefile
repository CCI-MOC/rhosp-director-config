CUSTOM_ROLES = \
	       roles/ControllerDeployedServer.yaml \
	       roles/ComputeDeployedServer.yaml \
	       roles/NetworkerDeployedServer.yaml

CONTROLLER_SRC_ROLES = \
	    roles/ControllerOpenstack.yaml \
	    roles/Database.yaml \
	    roles/Messaging.yaml

ENVIRONMENTS = templates/deploy.yaml

%.html: %.md
	$(PANDOC) -s $< -o $@ --toc --css github-pandoc.css

all: $(ENVIRONMENTS) roles_data.yaml

templates/deploy.yaml: templates/deploy.yaml.in
	ansible-playbook -e @templates/credentials.yaml generate-deploy-files.yaml

roles_data.yaml: $(CUSTOM_ROLES)
	openstack overcloud roles generate --roles-path roles -o $@ \
		ControllerDeployedServer \
		ComputeDeployedServer \
		NetworkerDeployedServer