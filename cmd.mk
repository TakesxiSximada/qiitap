.DEFAULT_GOAL: help


.PHONY: pypi
pypi:
	@# Upload test pypi

	twine upload dist/*.whl -r pypi


# .PHONY: register
# register:
# 	@# Register to pypi

# 	twine register dist/*.whl -r pypi


.PHONY: wheel
wheel:
	@# Build wheel package

	rm -rf dist
	python setup.py bdist_wheel --universal


.PHONY: testpypi
testpypi: wheel
	@# Register to test pypi

	twine register dist/*.whl -r testpypi
	twine upload dist/*.whl -r testpypi


.PHONY: help
help:
	@# Display usage

	unmake $(MAKEFILE_LIST)
