@ECHO OFF

pushd %~dp0

REM Sphinx 文档的命令文件

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.未找到 'sphinx-build' 命令。请确保已安装 Sphinx
	echo.然后设置 SPHINXBUILD 环境变量，使其指向
	echo.'sphinx-build' 可执行文件的完整路径。或者你也可以
	echo.将 Sphinx 目录添加到 PATH。
	echo.
	echo.如果你还没有安装 Sphinx，可以从这里获取：
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
