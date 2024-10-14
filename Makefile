
VENV_DIR = venv

PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip


.PHONY: install run


install: $(VENV_DIR)/bin/python
	pip install numpy scikit-learn flask
	@echo "依赖包安装完成。"


$(VENV_DIR)/bin/python:
	@echo "创建虚拟环境..."
	python3 -m venv $(VENV_DIR)
	@echo "虚拟环境创建完成。"

run:
	@echo "启动 Flask 应用..."
	python3 app.py
	python app.py