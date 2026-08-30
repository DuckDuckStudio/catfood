# Sphinx 文档生成器的配置文件。
#
# 有关内置配置值的完整列表，请参阅文档：
# https://www.sphinx-doc.org/zh-cn/master/usage/configuration.html

# -- 项目信息 -----------------------------------------------------
# https://www.sphinx-doc.org/zh-cn/master/usage/configuration.html#project-information

project = "catfood"
copyright = "2026-%Y, 鸭鸭「カモ」"  # pylint: disable=redefined-builtin / W0622
author = "鸭鸭「カモ」"
release = version = "2.2.2"

# -- 一般配置 -----------------------------------------------------
# https://www.sphinx-doc.org/zh-cn/master/usage/configuration.html#general-configuration

needs_sphinx = (
    "2.1"  # https://www.sphinx-doc.org/zh-cn/master/usage/markdown.html#configuration
)

extensions = [
    "sphinx.ext.autodoc",  # 纳入来自文档字符串的文档 https://www.sphinx-doc.org/zh-cn/master/usage/extensions/autodoc.html
    "sphinx.ext.napoleon",  # 支持 NumPy 和 Google 风格的文档字符串 https://www.sphinx-doc.org/zh-cn/master/usage/extensions/napoleon.html
    "myst_parser",  # 我要我的 Markdown https://myst-parser.readthedocs.io/en/latest/
]

templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"

# -- 用于 HTML 输出的选项 -----------------------------------------
# https://www.sphinx-doc.org/zh-cn/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
