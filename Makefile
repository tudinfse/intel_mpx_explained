IMG_NAME = mpx_evaluation
CONTAINER_NAME = cb_${ID}

DOCKER = sudo docker
DOCKER_RUN = $(DOCKER) run --log-driver none -it -v `pwd`/data_${ID}:/data

.PHONY: all build run start stop clean clean_all

all: build

build:
	@$(DOCKER) build --rm=true -t $(IMG_NAME) .

run:
	@$(DOCKER_RUN) --privileged=true --name=$(CONTAINER_NAME) $(IMG_NAME)

run_network:
	@$(DOCKER_RUN) --network=host -p 8080:8080 --privileged=true --name=$(CONTAINER_NAME) $(IMG_NAME)

start:
	@$(DOCKER) start -i $(CONTAINER_NAME)

stop:
	@$(DOCKER) stop $(CONTAINER_NAME)

pack:
	@$(DOCKER) commit $(CONTAINER_NAME) $(IMG_NAME)
	@$(DOCKER) save $(IMG_NAME) -o $(IMG_NAME).tar
	sudo chmod 755 $(IMG_NAME).tar
	gzip $(IMG_NAME).tar > $(IMG_NAME).tar.gz
	@tar -zcvf data.tar.gz data_${ID}/

clean:
	@$(DOCKER) rm $(CONTAINER_NAME)

clean_all:
	@$(DOCKER) rm $(CONTAINER_NAME)
	@$(DOCKER) rmi $(IMG_NAME)
