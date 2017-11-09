NAME := capture-webscreen
PYTHON_VERSION := 3.5

conda-create:
	conda create -n $(NAME) python=$(PYTHON_VERSION)
	source activate $(NAME) \
		& pip install -r requirements.txt

conda-remove:
	conda env remove -n $(NAME)
