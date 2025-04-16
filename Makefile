# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# Maintainer's makefile.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

me:= $(firstword $(MAKEFILE_LIST))

# Prints usage message and exits.
perl_usage=\
  BEGIN {\
    $$/ = "";\
    print "Usage: ${MAKE} -f ${me} TARGET";\
    print "Maintainer\047s makefile; the following targets are supported:";\
    print "";\
    my @tgts;\
  }\
  /\#\s([^\n]+)\n(\.PHONY:)\s([\w-]+)\n/ and do {\
    my $$tgt = $$3;\
    my $$doc = $$1;\
    push(@tgts, sprintf("  %-20s  %s", $$tgt, $$doc));\
  };\
  END {\
    print(join("\n", sort(@tgts)));\
    print "";\
  }\
  ${NULL}

.PHONY: usage
usage:
	@perl -wnle '${perl_usage}' ${MAKEFILE_LIST}

CHECK_COPYRIGHT?= yes
CHECK_COPYRIGHT_IGNORE?= setup.py
CHECK_DEPS?= htmlcov-clean
CHECK_FLAKE8?= yes
CHECK_ISORT?= yes
CHECK_MYPY?= yes
CHECK_PYLINT?= yes
CHECK_PYRIGHT?= yes
CHECK_PYTEST?= yes
CHECK_SYNTAX?= yes
CHECK_SYNTAX_IGNORE?=
COVERAGERC?= .coveragerc
COVERAGERC_EXCLUDE_LINES?=
COVERAGERC_OMIT?=
DOCS_SETENV?=
DOCS_SRC?= docs
DOCS_TGT?= .docs
DOCS_TGT_BRANCH?= gh-pages
FLAKE8?= ${PYTHON} -m flake8
FLAKE8_OPERANDS?= ${PACKAGE} ${TESTS}
FLAKE8_OPTIONS?= --config .flake8rc
FLAKE8RC?= .flake8rc
FLAKE8RC_IGNORE?= E226, E741, W503
GEN_ALL_TARGETS?=
ISORT?= ${PYTHON} -m isort
ISORT_CFG?= .isort.cfg
ISORT_CFG_ADD_IMPORTS?=
ISORT_CFG_INCLUDE_TRAILING_COMMA?= True
ISORT_CFG_MULTI_LINE_OUTPUT?= 3
ISORT_CFG_ORDER_BY_TYPE?= False
ISORT_OPERANDS?= ${PACKAGE} ${TESTS}
ISORT_OPTIONS?= --check --diff
MYPY?= ${PYTHON} -m mypy
MYPY_OPERANDS?= ${PACKAGE} ${TESTS}
MYPY_OPTIONS?= --show-error-context --show-error-codes
PERL?= perl
PIP?= ${PYTHON} -m pip
PYLINT?= pylint
PYLINT_OPERANDS?= ${PACKAGE} ${TESTS}
PYLINT_OPTIONS?=
PYLINTRC?= .pylintrc
PYLINTRC_DISABLE?=
PYRIGHT?= ${PYTHON} -m pyright
PYRIGHT_OPERANDS?= ${PACKAGE} ${TESTS}
PYRIGHT_OPTIONS?=
PYRIGHTCONFIG_EXCLUDE?= []
PYRIGHTCONFIG_JSON?= pyrightconfig.json
PYRIGHTCONFIG_OPTIONS?= --warnings
PYRIGHTCONFIG_REPORT_MISSING_IMPORTS?= true
PYRIGHTCONFIG_REPORT_MISSING_TYPE_STUBS?= true
PYTEST?= ${PYTHON} -m pytest
PYTEST_COV_OPTIONS?= --cov=${PACKAGE} --cov-report=html
PYTEST_INI?= pytest.ini
PYTEST_OPTIONS?= -ra
PYTEST_SETENV?=
PYTHON?= python
PYUPGRADE?= ${PYTHON} -m pyupgrade
PYUPGRADE_OPTIONS?= --exit-zero-even-if-changed --py39-plus
SETUP_PY?= setup.py
SETUP_PY_ENTRY_POINTS?= {}
SETUP_PY_EXTRAS_REQUIRE_DOCS?= []
SETUP_PY_EXTRAS_REQUIRE_EXTRA?= []
SETUP_PY_EXTRAS_REQUIRE_TESTS?= ['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox']
SETUP_PY_FIND_PACKAGES_EXCLUDE?= ['tests', 'tests.*']
SETUP_PY_INCLUDE_PACKAGE_DATA?= True
SETUP_PY_INSTALL_REQUIRES?= []
SETUP_PY_PACKAGE_DATA?= dict()
SETUP_PY_PACKAGE_DIR?= {'${PACKAGE}': '${PACKAGE}'}
SETUP_PY_PYTHON_REQUIRES?= '>=3.9'
SETUP_PY_ZIP_SAFE?= False
TESTS?= tests
TOX?= tox
TOX_INI?= tox.ini
TOX_INI_ENVLIST?= mypy, py{39,310,311,312,313}
TOX_INI_EXTRAS?= tests
TOX_INI_PASSENV?=
TOX_INI_SKIP_MISSING_INTERPRETERS?= true
TOX_OPTIONS?=
TOX_SETENV?=

include Makefile.conf

CHECK_DEPS+= $(if $(filter yes,${CHECK_COPYRIGHT}),check-copyright)
CHECK_DEPS+= $(if $(filter yes,${CHECK_FLAKE8}),check-flake8)
CHECK_DEPS+= $(if $(filter yes,${CHECK_ISORT}),check-isort)
CHECK_DEPS+= $(if $(filter yes,${CHECK_MYPY}),check-mypy)
CHECK_DEPS+= $(if $(filter yes,${CHECK_PYLINT}),check-pylint)
CHECK_DEPS+= $(if $(filter yes,${CHECK_PYRIGHT}),check-pyright)
CHECK_DEPS+= $(if $(filter yes,${CHECK_PYTEST}),check-pytest)
CHECK_DEPS+= $(if $(filter yes,${CHECK_SYNTAX}),check-syntax)
PYTEST_OPTIONS+= $(if $(filter yes,${CHECK_MYPY}),--mypy)

ECHO:= printf '%s\n'
ECHO_SPLIT= ${ECHO} '$(2)' | sed -e 's/\s*<line>/$(1)/g' -e 's,</line>,\n,g'

P:= @${ECHO}
P_SPLIT:= @$(call ECHO_SPLIT,$(1),$(2))

# check sources and run testsuite
.PHONY: check
check: ${CHECK_DEPS}

# check sources and run testsuite skipping slow tests
.PHONY: checkfast
checkfast:
	${MAKE} check ${CHECKFAST}

# run testsuite
.PHONY: check-pytest
check-pytest:
	${PYTEST_SETENV} ${PYTEST} -c ${PYTEST_INI} --strict-config ${TESTS}

# check sources using flake8
.PHONY: check-flake8
check-flake8:
	${FLAKE8} ${FLAKE8_OPTIONS} ${FLAKE8_OPERANDS}

# check sources using isort
.PHONY: check-isort
check-isort:
	${ISORT} ${ISORT_OPTIONS} ${ISORT_OPERANDS}

# check sources using mypy
.PHONY: check-mypy
check-mypy:
	${MYPY} ${MYPY_OPTIONS} ${MYPY_OPERANDS}

# check sources using pylint
.PHONY: check-pylint
check-pylint:
	${PYLINT} ${PYLINT_OPTIONS} ${PYLINT_OPERANDS}

# check sources using pyright
.PHONY: check-pyright
check-pyright:
	${PYRIGHT} ${PYRIGHT_OPTIONS} ${PYRIGHT_OPERANDS}

# check copyright
.PHONY: check-copyright
check-copyright: check-copyright-python

.PHONY: check-copyright-python
check-copyright-python:
	@${DO_CHECK_COPYRIGHT} $(filter-out\
	  ${CHECK_COPYRIGHT_IGNORE}, $(shell git ls-files '*.py'))

DO_CHECK_COPYRIGHT= ${PERL} -s -0777 -wnle '${perl_check_copyright}'
perl_check_copyright:=\
  BEGIN {\
    $$p = "\# " if !defined $$p;\
    $$q = $$p if !defined $$q;\
    $$h = "${COPYRIGHT}" if !defined $$h;\
    $$l = "SPDX-License-Identifier: ${LICENSE}" if !defined $$l;\
    $$regex = qr(\Q$$p\ECopyright \(C\) (20\d\d)(-(20\d\d))? \Q$$h\E\n\Q$$q$$l\E);\
    sub guess_year {\
      my $$date =\
        `git log --diff-filter=$$_[0] --follow --format=%as -1 -- $$ARGV`\
        || `date -I`;\
      $$date =~ /^(\d\d\d\d)/s;\
      return $$1;\
    }\
    $$errcnt = 0;\
    sub put_error {\
      warn("error:$$ARGV: $$_[0]\n");\
      $$errcnt++;\
    }\
  }\
  if (/$$regex/m) {\
    my $$start = $$1;\
    my $$end = $$3 if defined $$3;\
    my $$exp_start = guess_year("A");\
    if ($$start ne $$exp_start) {\
      put_error("copyright: bad start-year (expected $$exp_start, got $$start)");\
    } else {\
      my $$exp_end = guess_year("M");\
      if ($$exp_end eq $$exp_start) {\
        if (defined $$end) {\
          put_error("copyright: bad end-year (expected none, got $$end)");\
        }\
      } else {\
        if (!defined $$end) {\
          put_error("copyright: bad end-year (expected $$exp_end, got none)");\
        }\
      }\
    }\
  } else {\
    put_error("copyright: bad or missing license tag");\
  }\
  END { exit($$errcnt); }\
  ${NULL}

# check syntax
.PHONY: check-syntax
check-syntax: check-syntax-python

.PHONY: check-syntax-python
check-syntax-python:
	@${DO_CHECK_SYNTAX_PYTHON} $(filter-out\
	  ${CHECK_SYNTAX_IGNORE}, $(shell git ls-files '*.py'))

DO_CHECK_SYNTAX_PYTHON= ${PERL} -s -00 -wnle '${perl_check_syntax_python}'

perl_check_syntax_python:=\
  BEGIN {\
    $$errcnt = 0;\
    sub put_error {\
      warn("error:$$ARGV: $$_[0]\n");\
      $$errcnt++;\
    }\
  }\
  if (/^((\s\s\s\s+)(Parameters|Returns)(.*?))\"\"\"/s\
      or /^((\s\s\s\s+)(Parameters|Returns)(.*))$$/s) {\
    $$section = $$1;\
    $$header = $$3;\
    sub bad_section {\
      $$explain = shift;\
      put_error("bad $$header ($$explain):\n$$section\n");\
    }\
    $$section_indent = length($$2);\
    $$section_text = $$4;\
    if ($$section_text !~ /^:\n/) {\
      bad_section("missing colon-newline");\
    } else {\
      $$section_text =~ /^:\n(.*?)\s*(\"\"\")?$$/s;\
      if (!defined $$1) {\
        bad_section("syntax error");\
      }\
      foreach (split "\n", $$1) {\
        $$_ =~ /^(\s*)(.*)$$/;\
        if (length($$1) != $$section_indent + 3) {\
          bad_section("misalignment");\
        }\
        if ($$header eq "Parameters") {\
          $$line = $$2;\
          if ($$line !~ /^\w+:/) {\
            bad_section("missing colon in \"$$line");\
          }\
          if ($$line !~ /\.$$/) {\
            bad_section("missing final dot in \"$$line\"");\
          }\
        }\
      }\
      if ($$header eq "Returns" and $$section_text !~ /\.\s*$$/) {\
        bad_section("missing final dot");\
      }\
    }\
  }\
  END { exit($$errcnt); }\
  ${NULL}

# upgrade Python syntax
.PHONY: pyupgrade
pyupgrade:
	${PYUPGRADE} ${PYUPGRADE_OPTIONS} $(shell git ls-files '*.py')

# remove generated files
.PHONY: clean
clean: dist-clean docs-clean htmlcov-clean
	-${PYTHON} setup.py clean --all

.PHONY: dist-clean
dist-clean:
	-rm -rf ./dist ./${PACKAGE}.egg-info

.PHONY: htmlcov-clean
htmlcov-clean:
	-rm -rf ./htmlcov

# build docs
.PHONY: docs
docs:
	${DOCS_SETENV} ${MAKE} -C ./${DOCS_SRC} html\
	 NAME='${NAME}'\
	 PACKAGE='${PACKAGE}'\
	 VERSION='${VERSION}'\
	 COPYRIGHT='${COPYRIGHT}'\
	 COPYRIGHT_START_YEAR='${COPYRIGHT_START_YEAR}'
	$P 'Index: file://${PWD}/${DOCS_SRC}/_build/html/index.html'

.PHONY: docs-clean
docs-clean:
	${MAKE} -C ./${DOCS_SRC} clean
	-rm -rf ./${DOCS_SRC}/generated

# initialize docs branch
.PHONY: docs-init
docs-init:
	if ! test -d ${DOCS_TGT}; then\
	 mkdir -p ${DOCS_TGT};\
	 cd ${DOCS_TGT};\
	 git init;\
	 git checkout --orphan ${DOCS_TGT_BRANCH};\
	 git remote add origin ${URL_SSH};\
	fi
	-cd ${DOCS_TGT} && git pull origin ${DOCS_TGT_BRANCH}

# publish docs
.PHONY: docs-publish
docs-publish: docs-clean docs
	@if ! test -d ./${DOCS_TGT}; then\
	  ${ECHO} 1>&2 "*** ERROR: ${DOCS_TGT} does not exist";\
	  exit 1;\
	fi
	touch ./${DOCS_TGT}/.nojekyll
	cp -a ./${DOCS_SRC}/_build/html/* ./${DOCS_TGT}
	cd ${DOCS_TGT} && git add .
	cd ${DOCS_TGT} && git commit -m 'Update docs'
	cd ${DOCS_TGT} && git push origin ${DOCS_TGT_BRANCH}

GEN_ALL_TARGETS+= gen-coveragerc

# generate .coveragerc
.PHONY: gen-coveragerc
gen-coveragerc:
	$P 'generating ${COVERAGERC}'
	$P '[report]' >${COVERAGERC}
	$P 'omit = ${COVERAGERC_OMIT}' >>${COVERAGERC}
	$P 'exclude_lines =' >>${COVERAGERC}
	$P '    @(abc\.)?abstractmethod' >>${COVERAGERC}
	$P '    class .*\bProtocol\):' >>${COVERAGERC}
	$P '    def __repr__' >>${COVERAGERC}
	$P '    def __str__' >>${COVERAGERC}
	$P '    if 0:' >>${COVERAGERC}
	$P '    if __name__ == .__main__.:' >>${COVERAGERC}
	$P '    pragma: no cover' >>${COVERAGERC}
	$P '    raise AssertionError' >>${COVERAGERC}
	$P '    raise NotImplementedError' >>${COVERAGERC}
	@$(call ECHO_SPLIT,    ,${COVERAGERC_EXCLUDE_LINES}) >>${COVERAGERC}

GEN_ALL_TARGETS+= gen-flake8rc

# generate .flake8rc
.PHONY: gen-flake8rc
gen-flake8rc:
	$P 'generating ${FLAKE8RC}'
	$P '[flake8]' >${FLAKE8RC}
	$P 'ignore = ${FLAKE8RC_IGNORE}' >>${FLAKE8RC}

GEN_ALL_TARGETS+= gen-isort-cfg

# generage .isort.cfg
.PHONY: gen-isort-cfg
gen-isort-cfg:
	$P 'generating ${ISORT_CFG}'
	$P '[settings]' >${ISORT_CFG}
	$P 'add_imports = ${ISORT_CFG_ADD_IMPORTS}' >> ${ISORT_CFG}
	$P 'include_trailing_comma = ${ISORT_CFG_INCLUDE_TRAILING_COMMA}' >>${ISORT_CFG}
	$P 'multi_line_output = ${ISORT_CFG_MULTI_LINE_OUTPUT}' >>${ISORT_CFG}
	$P 'order_by_type = ${ISORT_CFG_ORDER_BY_TYPE}' >>${ISORT_CFG}

# generate .pylintrc
GEN_ALL_TARGETS+= gen-pylintrc

.PHONY: gen-pylintrc
gen-pylintrc:
	$P 'generating ${PYLINTRC}'
	$P '[MAIN]' > ${PYLINTRC}
	$P 'disable=' >> ${PYLINTRC}
	@$(call ECHO_SPLIT,    ,${PYLINTRC_DISABLE}) >>${PYLINTRC}

GEN_ALL_TARGETS+= gen-pyrightconfig-json

# generate pyrightconfig.json
.PHONY: gen-pyrightconfig-json
gen-pyrightconfig-json:
	$P 'generating ${PYRIGHTCONFIG_JSON}'
	$P '{' >${PYRIGHTCONFIG_JSON}
	$P '  "exclude": ${PYRIGHTCONFIG_EXCLUDE},' >>${PYRIGHTCONFIG_JSON}
	$P '  "reportMissingImports": ${PYRIGHTCONFIG_REPORT_MISSING_IMPORTS},' >>${PYRIGHTCONFIG_JSON}
	$P '  "reportMissingTypeStubs": ${PYRIGHTCONFIG_REPORT_MISSING_TYPE_STUBS}' >>${PYRIGHTCONFIG_JSON}
	$P '}' >>${PYRIGHTCONFIG_JSON}

GEN_ALL_TARGETS+= gen-pytest-ini

# generate pytest.ini
.PHONY: gen-pytest-ini
gen-pytest-ini:
	$P 'generating ${PYTEST_INI}'
	$P '[pytest]' >${PYTEST_INI}
	$P 'addopts = ${PYTEST_OPTIONS} ${PYTEST_COV_OPTIONS}' >>${PYTEST_INI}
	$P 'testpaths = ${TESTS}' >>${PYTEST_INI}

GEN_ALL_TARGETS+= gen-setup-py

# generate setup.py
.PHONY: gen-setup-py
gen-setup-py:
	$P 'generating ${SETUP_PY}'
	$P '# ** GENERATED FILE, DO NOT EDIT! **' >${SETUP_PY}
	$P 'import re' >>${SETUP_PY}
	$P 'import setuptools' >>${SETUP_PY}
	$P "with open('${PACKAGE}/version.py', 'r') as fp:" >>${SETUP_PY}
	$P '    text = fp.read()' >>${SETUP_PY}
	$P "    VERSION, = re.findall(r\"__version__\s*=\s*'(.*)'\", text)" >>${SETUP_PY}
	$P "with open('README.md', 'r') as fp:" >>${SETUP_PY}
	$P '    README = fp.read()' >>${SETUP_PY}
	$P 'setuptools.setup(' >>${SETUP_PY}
	$P "    name='${NAME}'," >>${SETUP_PY}
	$P '    version=VERSION,' >>${SETUP_PY}
	$P "    description='${DESCRIPTION}'," >>${SETUP_PY}
	$P '    long_description=README,' >>${SETUP_PY}
	$P "    long_description_content_type='text/markdown'," >>${SETUP_PY}
	$P "    author='${AUTHOR}'," >>${SETUP_PY}
	$P "    author_email='${EMAIL}'," >>${SETUP_PY}
	$P "    url='${URL}'," >>${SETUP_PY}
	$P "    license='${LICENSE}'," >>${SETUP_PY}
	$P "    python_requires=${SETUP_PY_PYTHON_REQUIRES}," >>${SETUP_PY}
	$P "    packages=setuptools.find_packages(exclude=${SETUP_PY_FIND_PACKAGES_EXCLUDE})," >>${SETUP_PY}
	$P "    package_data=${SETUP_PY_PACKAGE_DATA}," >>${SETUP_PY}
	$P '    include_package_data=True,' >>${SETUP_PY}
	$P "    package_dir=${SETUP_PY_PACKAGE_DIR}," >>${SETUP_PY}
	$P "    install_requires=${SETUP_PY_INSTALL_REQUIRES}," >>${SETUP_PY}
	$P '    extras_require={' >>${SETUP_PY}
	$P "        'docs': ${SETUP_PY_EXTRAS_REQUIRE_DOCS}," >>${SETUP_PY}
	$P "        'extra': ${SETUP_PY_EXTRAS_REQUIRE_EXTRA}," >>${SETUP_PY}
	$P "        'tests': ${SETUP_PY_EXTRAS_REQUIRE_TESTS}," >>${SETUP_PY}
	$P '    },' >>${SETUP_PY}
	$P "    entry_points=${SETUP_PY_ENTRY_POINTS}," >>${SETUP_PY}
	$P "    zip_safe=${SETUP_PY_ZIP_SAFE}," >>${SETUP_PY}
	$P ')' >>${SETUP_PY}

GEN_ALL_TARGETS+= gen-tox-ini

# generate tox.ini
.PHONY: gen-tox-ini
gen-tox-ini:
	$P 'generating ${TOX_INI}'
	$P '[tox]' >${TOX_INI}
	$P 'envlist = ${TOX_INI_ENVLIST}' >>${TOX_INI}
	$P 'skip_missing_interpreters = ${TOX_INI_SKIP_MISSING_INTERPRETERS}' >>${TOX_INI}
	$P '' >>${TOX_INI}
	$P '[testenv]' >>${TOX_INI}
	$P 'commands = {posargs:py.test}' >>${TOX_INI}
	$P 'extras = ${TOX_INI_EXTRAS}' >>${TOX_INI}
	$P 'passenv =' >>${TOX_INI}
	@$(call ECHO_SPLIT,    ,${TOX_INI_PASSENV}) >> ${TOX_INI}
	$P '[testenv:mypy]' >>${TOX_INI}
	$P 'commands = mypy -p ${PACKAGE}' >>${TOX_INI}

# run all gen-* targets
.PHONY: gen-all
gen-all: ${GEN_ALL_TARGETS}

# refresh indents
.PHONY: ident
ident:
	for f in `grep ident .gitattributes | sed 's/\s*ident$$//'`; do\
	  touch $$f; git checkout $$f; ${ECHO} "`head -n1 $$f` $$f";\
	done

# install package
.PHONY: install
install:
	${PIP} install -e '.[extra]'

# install doc-build, publish, and test dependencies
.PHONY: install-deps
install-deps:
	${PIP} install --upgrade '.[docs]' '.[tests]' build twine

# run tox
.PHONY: tox
tox:
	${TOX_SETENV} ${TOX} ${TOX_OPTIONS} $(if ${ENV},-e ${ENV})

# debug tox environment
.PHONY: tox-debug
tox-debug:
	${TOX_SETENV} ${TOX} -e $(or ${ENV},py311) -- python

# uninstall package
.PHONY: uninstall
uninstall:
	${PYTHON} setup.py develop -u

# publish package
.PHONY: publish
publish: dist-clean
	${PYTHON} -m build
	${PYTHON} -m twine upload dist/*
