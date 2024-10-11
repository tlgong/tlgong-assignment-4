# Makefile

.PHONY: install run clean

VENV := venv

# 创建虚拟环境
venv:
	python -m venv $(VENV)

# 安装项目依赖
install: venv
	. $(VENV)/Scripts/activate && pip install --upgrade pip && pip install -r requirements.txt

# 运行Flask应用
run:
	. $(VENV)/Scripts/activate && python app.py

# 清理虚拟环境
clean:
	rm -rf $(VENV)
