OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

all: test

export PYTHONPATH:=${PWD}
version=`python -c 'import paco; print(paco.version)'`
filename=paco-`python -c 'import paco; print(paco.version)'`.tar.gz

apidocs:
	@sphinx-apidoc -f --follow-links -H "API documentation" -o docs/source pyco

htmldocs:
	@rm -rf docs/_build
	$(MAKE) -C docs html

lint:
	@echo "$(OK_COLOR)==> Linting code...$(NO_COLOR)"
	@flake8 .

test: clean lint
	@echo "$(OK_COLOR)==> Runnings tests...$(NO_COLOR)"
	@py.test -s -v --cov pyco --cov-report term-missing

coverage:
	@coverage run --source pyco -m py.test
	@coverage report

tag:
	@echo "$(OK_COLOR)==> Creating tag $(version)...$(NO_COLOR)"
	@git tag -a "v$(version)" -m "Version $(version)"
	@echo "$(OK_COLOR)==> Pushing tag $(version) to origin...$(NO_COLOR)"
	@git push origin "v$(version)"

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -delete; done

release: clean publish
	@echo "$(OK_COLOR)==> Exporting to $(filename)...$(NO_COLOR)"
	@tar czf $(filename) paco setup.py README.md LICENSE

publish:
	@python setup.py sdist register upload
