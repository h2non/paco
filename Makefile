OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

all: test

export PYTHONPATH:=${PWD}
version=`python -c 'import paco; print(paco.__version__)'`
filename=paco-`python -c 'import paco; print(paco.__version__)'`.tar.gz

apidocs:
	@sphinx-apidoc -f --follow-links -H "API documentation" -o docs/source paco

htmldocs:
	@rm -rf docs/_build
	$(MAKE) -C docs html

lint:
	@echo "$(OK_COLOR)==> Linting code...$(NO_COLOR)"
	@flake8 .

test: clean lint
	@echo "$(OK_COLOR)==> Runnings tests...$(NO_COLOR)"
	@py.test -s -v --capture=sys --cov paco --cov-report term-missing

coverage:
	@coverage run --source paco -m py.test
	@coverage report

bump:
	@bumpversion --commit --tag --current-version $(version) patch paco/__init__.py --allow-dirty

bump-minor:
	@bumpversion --commit --tag --current-version $(version) minor paco/__init__.py --allow-dirty

push-tag:
	@echo "$(OK_COLOR)==> Pushing tag to remote...$(NO_COLOR)"
	@git push origin "v$(version)"

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -delete; done

release: clean bump push-tag publish
	@echo "$(OK_COLOR)==> Done! $(NO_COLOR)"

publish:
	@echo "$(OK_COLOR)==> Releasing package ...$(NO_COLOR)"
	@python setup.py register
	@python setup.py sdist upload
	@python setup.py bdist_wheel --universal upload
	@rm -fr build dist .egg requests.egg-info
