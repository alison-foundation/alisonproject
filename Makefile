BASEDIR=./alison
TESTDIR=./alison/lib/tests

all : clean tests

clean :
	@if [ -f "Pipfile" ]; 		then rm "Pipfile"; 		fi
	@if [ -f "Pipfile.lock" ]; 	then rm "Pipfile.lock"; fi
	@rm -rf `find ${BASEDIR} -type d -name "*__pycache__"`

dependencies:
	@sudo apt-get install python-scipy
	@python3 -m pip install pipenv
	@pipenv install -r ${BASEDIR}/requirements.txt

tests : dependencies
	@pipenv run python3 ${TESTDIR}/main_tests.py

build : dependencies
	@pipenv run python3 ${BASEDIR}/setup.py sdist

upload : dependencies
	@pipenv run python3 ${BASEDIR}/setup.py sdist upload
