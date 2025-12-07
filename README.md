# 猫粮 🐱

各种常用函数的集合。

## 安装

我自己仅在 CPython 3.13 (3.13.9) 测试过。  

### Pypi
```bash
# https://pypi.org/project/catfood/
pip install catfood
```

### Test Pypi
```bash
# https://test.pypi.org/project/catfood/
pip install -i https://test.pypi.org/simple/ catfood
```

### 从源安装
```bash
git clone https://github.com/DuckDuckStudio/catfood.git
pip install ./catfood
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
