# 用于 Sphinx 文档的最小 makefile
#

# 你可以从命令行设置这些变量，也可以
# 从环境变量中设置前两个变量。
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# 把它放在最前面，这样在不带参数时，"make" 就等价于 "make help"。
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# 通用目标：将所有未知目标转发给 Sphinx，使用新的
# "make mode" 选项。$(O) 是 $(SPHINXOPTS) 的简写。
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
