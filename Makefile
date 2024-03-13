# Copyright (C) 2023-2024 IBM Corp.
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
  }\
  /\#\s([^\n]+)\n(\.PHONY:|SC_RULES\+=)\s([\w-]+)\n/ and do {\
    my $$tgt = $$3;\
    my $$doc = $$1;\
    printf ("  %-20s  %s\n", $$tgt, $$doc);\
  };\
  END { print ""; }\
  ${NULL}

.PHONY: usage
usage:
	@perl -wnle '${perl_usage}' ${MAKEFILE_LIST}

CHECK_COPYRIGHT?= yes
CHECK_COPYRIGHT_IGNORE?=
CHECK_DEPS?= htmlcov-clean
CHECK_FLAKE8=? yes
CHECK_ISORT?= yes
CHECK_MYPY?= yes
CHECK_PYTEST?= yes
COVERAGERC?= .coveragerc
COVERAGERC_EXCLUDE_LINES?=
COVERAGERC_OMIT?=
DOCS_SRC?= docs
DOCS_TGT?= .docs
DOCS_TGT_BRANCH?= gh-pages
FLAKE8_IGNORE?= E741, W503
FLAKE8_OPTIONS?= --config .flake8rc
FLAKE8RC?= .flake8rc
ISORT_CFG?= .isort.cfg
ISORT_CFG_INCLUDE_TRAILING_COMMA?= True
ISORT_CFG_MULTI_LINE_OUTPUT?= 3
ISORT_CFG_ORDER_BY_TYPE?= False
ISORT_OPTIONS?= --check --diff
MANIFEST_IN?= Manifest.in
MANIFEST_IN_GIT_LS_FILES_PATHSPEC?=
MYPY_OPTIONS?= --show-error-context --show-error-codes
PERL?= perl
PIP?= ${PYTHON} -m pip
PYTEST?= ${PYTHON} -m pytest
PYTEST_COV_OPTIONS?= --cov=${PACKAGE} --cov-report=html
PYTEST_ENV?=
PYTEST_INI?= pytest.ini
PYTEST_OPTIONS?= -ra
PYTHON?= python
TESTS?= tests
TOX?= tox
TOX_ENVLIST?= mypy, py{39,310,311,312}
TOX_INI?= tox.ini
TOX_OPTIONS?=
TOX_PASSENV?=
TOX_SETENV?=

include Makefile.conf

CHECK_DEPS+= $(if $(filter yes,${CHECK_COPYRIGHT}),check-copyright)
CHECK_DEPS+= $(if $(filter yes,${CHECK_FLAKE8}),check-flake8)
CHECK_DEPS+= $(if $(filter yes,${CHECK_ISORT}),check-isort)
CHECK_DEPS+= $(if $(filter yes,${CHECK_MYPY}),check-mypy)
CHECK_DEPS+= $(if $(filter yes,${CHECK_PYTEST}),check-pytest)
PYTEST_OPTIONS+= $(if $(filter yes,${CHECK_MYPY}),--mypy)

split = $(shell printf '$(1)'\
   | sed -e 's/\s*<line>/    /g' -e 's,</line>,\\n,g')

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
	${PYTEST_ENV} ${PYTEST} -c ${PYTEST_INI} --strict-config ${TESTS}

# check sources using flake8
.PHONY: check-flake8
check-flake8:
	${PYTHON} -m flake8 ${FLAKE8_OPTIONS} ${PACKAGE} ${TESTS}

# check sources using isort
.PHONY: check-isort
check-isort:
	${PYTHON} -m isort ${ISORT_OPTIONS} ${PACKAGE} ${TESTS}

# check sources using mypy
.PHONY: check-mypy
check-mypy:
	${PYTHON} -m mypy ${MYPY_OPTIONS} ${PACKAGE} ${TESTS}

# check copyright
.PHONY: check-copyright
check-copyright: check-copyright-python

.PHONY: check-copyright-python
check-copyright-python:
	@${CHECK_COPYRIGHT} $(filter-out\
	  ${CHECK_COPYRIGHT_IGNORE}, $(shell git ls-files '*.py'))

CHECK_COPYRIGHT= ${PERL} -s -0777 -wnle '${perl_check_copyright}'
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
	${MAKE} -C ./${DOCS_SRC} html\
	 NAME='${NAME}'\
	 PACKAGE='${PACKAGE}'\
	 COPYRIGHT='${COPYRIGHT}'\
	 COPYRIGHT_START_YEAR='${COPYRIGHT_START_YEAR}'
	@echo 'Index: file://${PWD}/${DOCS_SRC}/_build/html/index.html'

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
	 echo 1>&2 "*** ERROR: ${DOCS_TGT} does not exist";\
	 exit 1;\
	fi
	touch ./${DOCS_TGT}/.nojekyll
	cp -a ./${DOCS_SRC}/_build/html/* ./${DOCS_TGT}
	cd ${DOCS_TGT} && git add .
	cd ${DOCS_TGT} && git commit -m 'Update docs'
	cd ${DOCS_TGT} && git push origin ${DOCS_TGT_BRANCH}

# run all gen-* targets
.PHONY: gen-all
gen-all: gen-coveragerc gen-isort-cfg gen-flake8rc gen-manifest-in\
  gen-pytest-ini gen-tox-ini

# generate .coveragerc
.PHONY: gen-coveragerc
gen-coveragerc:
	@echo 'generating ${COVERAGERC}'
	@echo '[report]' >${COVERAGERC}
	@echo 'omit = ${COVERAGERC_OMIT}' >>${COVERAGERC}
	@echo 'exclude_lines =' >>${COVERAGERC}
	@echo '    @(abc\.)?abstractmethod' >>${COVERAGERC}
	@echo '    class .*\\bProtocol\):' >>${COVERAGERC}
	@echo '    def __repr__' >>${COVERAGERC}
	@echo '    def __str__' >>${COVERAGERC}
	@echo '    if 0:' >>${COVERAGERC}
	@echo '    if __name__ == .__main__.:' >>${COVERAGERC}
	@echo '    pragma: no cover' >>${COVERAGERC}
	@echo '    raise AssertionError' >>${COVERAGERC}
	@echo '    raise NotImplementedError' >>${COVERAGERC}
	@echo "$(call split,${COVERAGERC_EXCLUDE_LINES})" >>${COVERAGERC}

# generate .flake8rc
.PHONY: gen-flake8rc
gen-flake8rc:
	@echo 'generating ${FLAKE8RC}'
	@echo '[flake8]' >${FLAKE8RC}
	@echo 'ignore = ${FLAKE8_IGNORE}' >>${FLAKE8RC}

# generage .isort.cfg
.PHONY: gen-isort-cfg
gen-isort-cfg:
	@echo 'generating ${ISORT_CFG}'
	@echo '[settings]' >${ISORT_CFG}
	@echo 'include_trailing_comma = ${ISORT_CFG_INCLUDE_TRAILING_COMMA}' >>${ISORT_CFG}
	@echo 'multi_line_output = ${ISORT_CFG_MULTI_LINE_OUTPUT}' >>${ISORT_CFG}
	@echo 'order_by_type = ${ISORT_CFG_ORDER_BY_TYPE}' >>${ISORT_CFG}

# generate Manifest.in
.PHONY: gen-manifest-in
gen-manifest-in:
	@echo 'generating ${MANIFEST_IN}'
	@git ls-files ${MANIFEST_IN_GIT_LS_FILES_PATHSPEC} |\
	 sed 's,\(.*\),include \1,' >${MANIFEST_IN}

# generate pytest.ini
.PHONY: gen-pytest-ini
gen-pytest-ini:
	@echo 'generating ${PYTEST_INI}'
	@echo '[pytest]' >${PYTEST_INI}
	@echo 'addopts = ${PYTEST_OPTIONS} ${PYTEST_COV_OPTIONS}' >>${PYTEST_INI}
	@echo 'testpaths = ${TESTS}' >>${PYTEST_INI}

# generate tox.ini
.PHONY: gen-tox-ini
gen-tox-ini:
	@echo 'generating ${TOX_INI}'
	@echo '[tox]' >${TOX_INI}
	@echo 'envlist = ${TOX_ENVLIST}' >>${TOX_INI}
	@echo 'skip_missing_interpreters = true' >>${TOX_INI}
	@echo '' >>${TOX_INI}
	@echo '[testenv]' >>${TOX_INI}
	@echo 'commands = {posargs:py.test}' >>${TOX_INI}
	@echo 'extras = tests' >>${TOX_INI}
	@echo 'passenv =' >>${TOX_INI}
	@echo "$(call split,${TOX_PASSENV})" >> ${TOX_INI}
	@echo '[testenv:mypy]' >>${TOX_INI}
	@echo 'commands = mypy -p ${PACKAGE}' >>${TOX_INI}

# refresh indents
.PHONY: ident
ident:
	for f in `grep ident .gitattributes | sed 's/\s*ident$$//'`; do\
	  touch $$f; git checkout $$f; echo "`head -n1 $$f` $$f";\
	done

# install package
.PHONY: install
install:
	${PIP} install -e .

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
