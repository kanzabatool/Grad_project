# Automatically annotating cancer variants using publicdatabases

## Prequisite:

	- Follow all steps here  https://runnable.com/docker/install-docker-on-linux
	- CLONE using this command: git clone https://github.com/kanzabatool/Grad_project
	- While into a folder run commands:
	    - virtualenv venv
		- source venv/bin/activate
	    - pip install -r requirements.txt
	- sudo apt-get install wkhtmltopdf (LINUX) | brew cask install wkhtmltopdf (MAC)


## Command Needs to be run:

	- docker pull selenium/standalone-chrome
	- docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.14.0-dubnium

## To Run Program
	
	- python main.py 
