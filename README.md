# Pokemon finder

This app provides a Pokemon Finder automatically synced with the PokeApi (https://pokeapi.co).


## Prerequisites

Python 3.9 must be installed as well as MySQL.

## Installation

CD into the root project folder and use command:

    pip install -r requirements.txt

Afterwards, run:

    run_app.sh

The script will first run necessary migrations. During the first initialization, the database will sync with the external API. Progress status will be given througout. 

Further runs will only sync when the PokeApi has more entries than the local database.

## Usage

To utilize the Pokemon Finder, navigate to http://localhost:8000/search, or in case you're using a DNS, or local tunneling https://{host}:{port}/search

## Tests

Running tests is as simple as issuing the command:

    run_tests.sh

This script will run the full models, views and utils tests with a level 2 verbosity.

## Relevant To-Do:

* Prettier UI
* Fetch more detailed information about Pokemon for details page.
* Break up total number of pokemon into pages.
* Select pokemon based on 'League'.
* Offer individual pokemon sound when first arriving at details page.
* Save images as blobs in database (Django ImageField was preferred for simplicity and coherence with Django's internal functioning). Another way, if considering to move images to S3 storage is to create separate table Image, with bucket, key and name of said image, linking it with Pokemon through ForeignKey.

## Running with Docker

A Dockerization option is offered. Simply run:

    docker build -t pokemonFinder ./

After successful building stage, run the Docker as such:

    docker run -p 8000:8000 pokemonFinder
	
# Technical information

The PokemonSearch app is leveraged through the following technologies:

* Python 3.9
* Django Framework
* Unittest library (Through Django implementation)
* MySQL Database (Not provided but installed through the appropiate installation process)
* Docker
