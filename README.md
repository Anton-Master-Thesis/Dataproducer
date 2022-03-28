# Dataproducer
Mockup of a dataprocessor, could be used with sensors

## Setup
create a folder venv

> mkdir venv

install venv via the command

> py -3 -m venv venv

activate the virtual environment

linux

> . venv/Script/activate

windows 

> venv/Script/activate

install required libraries

> pip install -r requirements.txt

run the project

> python run.py

## Configuration
There are several configuration/description files.
These determine what is sent to the core systems.

In the Arrowhead folder there is the SystemConfig.json file.
This specifies where the system is located and which certificate to use. It is important that the host and port coincides with the flaskapp. (Note, the certificate "common name" need to be the same as the systemName).

In the Arrowhead/EventHandler/Events folder there are several json files.
These json files describes which events that the system can send and what metadata they should contain.
These event files are loaded dynamically.

In the Arrowhead/Orchestration folder there is the file OrchestrationConfig.json.
This file describes where the Orchestrator is hosted and if it is secure.

In the Arrowhead/Orchestration/Services folder there are json files which describe which services to orchestrate for.

In the Arrowhead/Serviceregistry folder there is the file ServiceregistryConfig.json.
This file describes where the Serviceregistry is hosted and if it is secure.

In the Arrowhead/Serviceregistry/Services there are json files which describes which services should be published to the Serviceregistry.

## Structure
### Arrowhead
In the arrowhead folder all things arrowhead are located.
The system config describes the system for use in Arrowhead.

#### EventHandler
This folder contains everything related to the EventHandler.
The file "EventHandler.py" contains a class "EventHandler" which orchestrates the publish service and publishes the events defined in the "Events" folder.
This is done dynamically when the EventHandler class is instanciated.

#### Orchestration
This folder contains everything related to the orchestration process.
The file "Orchestrator.py" contains the class "Orchestrator" which can orchestrate the services described in the Services folder. This is done dynamically and is done every time the orchestrate method is called.

#### Serviceregistry
This folder contains everything related to the Serviceregistry.
The file "Serviceregistry.py" contains the class "Serviceregistry" which can register the services described in the "Services" folder. This is done dynamically when the "registerProvider" method is called.