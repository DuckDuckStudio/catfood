# 猫粮 🐱

[![Pypi 上的版本](https://img.shields.io/pypi/v/catfood.svg)](https://pypi.org/project/catfood)  

各种常用函数的集合。

## 安装

我自己仅在 CPython 3.12 - 3.14 上测试过。  

### Pypi

https://pypi.org/project/catfood/

```bash
python -m pip install catfood
```

### Test Pypi

https://test.pypi.org/project/catfood/

```bash
python -m pip install -i https://test.pypi.org/simple/ catfood
```

### 从源安装
```bash
git clone https://github.com/DuckDuckStudio/catfood.git
python -m pip install ./catfood
```

#### Build whl
```bash
# Windows PowerShell
git clone https://github.com/DuckDuckStudio/catfood.git
cd catfood

python -m venv .venv
& ".venv/Scripts/Activate.ps1"
python.exe -m pip install pip --upgrade

pip install ".[build_and_publish]" # 包括构建和发布依赖 build 和 twine
python -m build
ls dist/

# 从 whl 安装
pip install dist/catfood-1.0.0-py3-none-any.whl
```
