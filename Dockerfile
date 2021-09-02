FROM ubuntu:focal

ENV POKEHOME=/home/pokemonSearch
ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -r pokemonSearch; \
    useradd -m -s /bin/bash -g pokemonSearch pokemonSearch
	
RUN chown pokemonSearch:pokemonSearch -R $POKEHOME

RUN set -eux; \
	apt-get update && apt-get -y install python3-pip

RUN set -eux; \
    apt-get -qq -y autoremove; \
    apt-get autoclean; \

##################################################################

USER pokemonSearch

COPY pokemonSearch $POKEHOME/pokemonSearch

WORKDIR $POKEHOME/pokemonSearch

RUN set -eux; \
	pip3 install --default-timeout=100 -r requirements.txt
	
USER root

RUN set -eux; \
    chown -R pokemonSearch:pokemonSearch $POKEHOME/pokemonSearch;

USER pokemonSearch

RUN set -eux; \
    python3 manage.py makemigrations; \
    python3 manage.py migrate; \

EXPOSE 8000
CMD ["python3", "manage.py runserver"]

