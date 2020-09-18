# sphinx-express

## Setup

```bash

$ sphinx-express.py --setup

You should install follows packages.
python -m pip install sphinx-rtd-theme sphinx-charts pallets_sphinx_themes sphinxcontrib-runcmd sphinxcontrib-napoleon

your configfile: /Users/goichiiisaka/.sphinx/quickstartrc
your templatedir: /Users/goichiiisaka/.sphinx/templates/quickstart
quickstart templates of sphinx into your templatedir.


```

Here is default quickstarrc.

```yaml

sep: true
language: ja
suffix: .rst
master: index
makefile: true
batchfile: true
autodoc: true
doctest: false
intersphinx: false
todo: false
coverage: false
imgmath: true
mathjax: true
ifconfig: true
viewcode: true
project: sample
version: 0.0.1
release: 0.0.1
lang: ja
make_mode: true
ext_mathjax: true
extensions:
- pallets_sphinx_themes
- sphinx_rtd_theme
- sphinx.ext.autodoc
- sphinx.ext.mathjax
- sphinx.ext.autosectionlabel
- sphinxcontrib.blockdiag
- sphinxcontrib.seqdiag
- sphinxcontrib.blockdiag
- sphinxcontrib.nwdiag
- sphinxcontrib.rackdiag
- sphinxcontrib.httpdomain
- sphinxcontrib.runcmd
- recommonmark
mastertocmaxdepth: 2
project_underline: ======

```

You can change above settings.
and run sphinx-express again.

```bash
$ sphinx-express.py sample
Welcome to the Sphinx 3.2.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: sample

Creating file /Users/goichiiisaka/bin/kk/sample/source/conf.py.
Creating file /Users/goichiiisaka/bin/kk/sample/source/index.rst.
Creating file /Users/goichiiisaka/bin/kk/sample/Makefile.
Creating file /Users/goichiiisaka/bin/kk/sample/make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file /Users/goichiiisaka/bin/kk/sample/source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

```
Usage:

```
$ ./sphinx-express.py --help
Usage: sphinx-express.py [OPTIONS] [PROJECT_DIR]

  Create required files for a Sphinx project.

Options:
  -p, --project TEXT      project name
  -a, --author TEXT       author name. default is "goichiiisaka"
  -v, --version TEXT      version of project
  -l, --lang TEXT         document language. default is 'ja'
  -t, --templatedir PATH  template directory for template files. default:
                          /Users/goichiiisaka/.sphinx/templates/quickstart

  -c, --configfile PATH   sphinx-quickstart configfile. default:
                          /Users/goichiiisaka/.sphinx/quickstartrc

  -N, --new               Ignore least configures.
  --setup                 Copy quickstart templates and exit.
  --help                  Show this message and exit.

```
