#!/usr/bin/env python
"""
    sphinx-express
    ~~~~~~~~~~~~~~~~~~~~~

    Quickly setup documentation source to work with Sphinx.

    :copyright: Copyright 2020- Goichi (iisaka) Yukawa
    :license: MIT, see LICENSE.txt for details.
"""


__AUTHOR__="Gochi (iisaka) Yukawa"
__VERSION__="0.1.3"
__LICENSE__="MIT"

import os
import click
import yaml
import sys
import shutil
import fileinput
from pathlib import Path
from string import Template
import sphinx
import pkg_resources
from sphinx.cmd.quickstart import ask_user, generate, DEFAULTS


RECOMEND_MODULES = {
    "pallets_sphinx_themes",
    "sphinx-rtd-theme",
    "sphinx-jinja",
    "sphinxcontrib-seqdiag",
    "sphinxcontrib-blockdiag",
    "sphinxcontrib-nwdiag",
    "sphinxcontrib-jsmath",
    "sphinxcontrib-runcmd",
    "sphinxcontrib-applehelp",
    "sphinxcontrib-devhelp",
    "sphinxcontrib-htmlhelp",
    "sphinxcontrib-httpdomain",
    "sphinxcontrib-serializinghtml",
    "sphinxcontrib-napoleon",
    "sphinx-charts",
    "commonmark",
    "recommonmark",
}

DEFAULT_CONFIG = """
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
- sphinxcontrib.jinja
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
"""

IGNORE_OPTIONS=[
    "path",
    "project",
    "rsrcdir",
    "rbuilddir",
    "now",
]

REPLACE_CONFIGS = {
    "html_theme = 'alabaster'":
"""
# Avilable Themes:
# alabaster
{% set default_theme="alabaster" %}
{%- if 'sphinx_rtd_theme' in extensions -%}
# sphinx_rtd_theme
{% set default_theme="sphinx_rtd_theme" %}
{%- endif -%}
{%- if 'pallets_sphinx_themes' in extensions -%}
# babel, click, flask, jinja, platter, pocoo, werkzeug
{% set default_theme="flask" %}
{%- endif -%}
#
html_theme = "{{ default_theme }}"
""",
}

APPEND_CONFIGS = """
{%- if 'sphinx.ext.autosectionlabel ' in extensions %}
## True to prefix each section label with the name of the document it is in,
## followed by a colon. For example,
## index:Introduction for a section called Introduction
## that appears in document index.rst.
## Useful for avoiding ambiguity when the same section heading appears
## in different documents.
autosectionlabel_prefix_document = True

## If set, autosectionlabel chooses the sections for labeling by its depth.
## For example, when set 1 to autosectionlabel_maxdepth,
## labels are generated only for top level sections,
## and deeper sections are not labeled. It defaults to None (disabled).
autosectionlabel_maxdepth = 1

{%- endif %}

{%- if 'sphinxcontrib.seqdiag' in extensions %}
# -- Options for seqdiag output -------------------------------------------

# curl -O https://ja.osdn.net/projects/ipafonts/downloads/51868/IPAfont00303.zip
import os
basedir = os.path.abspath(os.path.dirname(__file__))
seqdiag_fontpath = basedir + '/_fonts/IPAfont00303/ipagp.ttf'
seqdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.nwdiag' in extensions %}
# -- Options for nwdiag output --------------------------------------------

nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.blockdiag' in extensions %}
# -- Options for blockdiag output ------------------------------------------

blockdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.actdiag' in extensions %}
# -- Options for actdiag output --------------------------------------------

actdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.jinja' in extensions %}
# -- Options for jinja output ------------------------------------------
# jinja_contexts = {}
{%- endif %}

{%- if 'sphinxcontrib.httpdomain' in extensions %}
# -- Options for httpdomain output ------------------------------------------

# List of HTTP header prefixes which should be ignored in strict mode:
http_headers_ignore_prefixes = ['X-']

# Strips the leading segments from the endpoint paths
# by given list of prefixes:
# http_index_ignore_prefixes = ['/internal', '/_proxy']

# Short name of the index which will appear on every page:
# http_index_shortname = 'api'

# Full index name which is used on index page:
# http_index_localname = "My Project HTTP API"

# When True (default) emits build errors when status codes,
# methods and headers are looks non-standard:
http_strict_mode = True
{%- endif %}


{%- if 'recommonmark' in extensions %}
# -- Options for recommonmark output ----------------------------------------
import recommonmark
from recommonmark.transform import AutoStructify

# At the bottom of conf.py
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
{%- endif %}

"""



class SphinxExpress(object):
    default_templatedir = Path.home() / ".sphinx/templates/quickstart"
    default_configfile = Path.home() / ".sphinx/quickstartrc"
    default_user = os.getlogin()

    def __init__(self, configfile: Path = None):
        if configfile is None:
            self.configfile = self.default_configfile
        else:
            self.configfile = configfile
            self.default_configfile = configfile
        self.config_templatefile = self.default_templatedir  / 'conf.py_t'

    def load_config(self, defaults=None):
        if defaults:
            if isinstance(defaults, dict):
                config = defaults.copy()
            else:
                config = yaml.load(defaults, Loader=yaml.SafeLoader)
        else:
            config = dict()

        try:
            with open(self.configfile, "r") as f:
                template = Template(f.read())
                interpolated_config = template.safe_substitute(config)
                newconf = yaml.load(interpolated_config, Loader=yaml.SafeLoader)
                config.update(newconf)
        except:
            pass

        return config

    def save_config(self, config: dict):
        config_dir = os.path.dirname(self.configfile)
        os.makedirs(config_dir, exist_ok=True)
        with open(self.configfile, "w") as f:
            rv = yaml.dump(config, stream=f, default_flow_style=False, sort_keys=False)

    def replace_config_template(self, search_text, replace_text):
        with fileinput.input(self.config_templatefile, inplace=True) as f:
            for line in f:
                new_line = line.replace(search_text, replace_text)
                print(new_line, end='')

    def append_config_template(self, configs):
        f = open(self.config_templatefile, 'a')
        f.write(configs)
        f.close()


def initconfig():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = RECOMEND_MODULES - installed

    if missing:
        pkgs = " ".join(str(e) for e in missing)
        click.echo("\nYou should install follows packages.")
        click.echo("python -m pip install {}".format(pkgs))

    config = SphinxExpress()
    config_data = config.load_config(DEFAULT_CONFIG)
    config.save_config(config_data)

    os.makedirs(config.default_templatedir, exist_ok=True)
    sphinx_module_dir = os.path.dirname(sphinx.__file__)
    sphinx_template_dir = Path(sphinx_module_dir) / "templates/quickstart"
    files = sphinx_template_dir.glob("*")
    for f in files:
        shutil.copy(f, config.default_templatedir)

    for pattern in REPLACE_CONFIGS.keys():
        config.replace_config_template(pattern, REPLACE_CONFIGS[pattern])

    config.append_config_template(APPEND_CONFIGS)

    click.echo("\nyour configfile: {}".format(config.configfile))
    click.echo("your templatedir: {}".format(config.default_templatedir))
    click.echo("quickstart templates of sphinx into your templatedir.\n")


@click.command(help="Create required files for a Sphinx project.")
@click.option("--project", "-p", type=str, default=None,
    help="project name. default is basename of PROJECT_DIR.")
@click.option("--author", "-a",
    type=str,
    default=SphinxExpress.default_user,
    help='author name. default is "{}"'.format(SphinxExpress.default_user),
)
@click.option("--ver", "-v",
    type=str,
    default="0.0.1", help="version of project. default is '0.0.1'"
)
@click.option(
    "--lang", "-l",
    type=str,
    default="ja",
    help="document language. default is 'ja'"
)
@click.option(
    "--templatedir", "-t",
    type=click.Path(),
    default=SphinxExpress.default_templatedir,
    help="""
    template directory for template files.
    default: {}""".format( SphinxExpress.default_templatedir),
)
@click.option(
    "--define_value", "-d",
    type=str,
    multiple=True, default=[],
    help="define a template variable. NAME=VALUE"
)
@click.option(
    "--configfile", "-c",
    type=click.Path(),
    default=SphinxExpress.default_configfile,
    help="""
    sphinx-express configfile.
    default: {}""".format( SphinxExpress.default_configfile),
)
@click.option(
    "--new", "-N",
    is_flag=True, type=bool, default=False,
    help="Ignore least configures.",
)
@click.option(
    "--setup",
    is_flag=True, type=bool, default=False,
    help="Copy quickstart templates and exit."
)
@click.argument("project_dir", nargs=1, required=False)
@click.version_option(__VERSION__)
def quickstart(
    project, author, ver, lang,
    templatedir, define_value, configfile, new, setup, project_dir=None
):

    def parse_variables(variable_list):
        dummy = dict()
        for variable in variable_list:
            try:
                name, value = variable.split('=')
                dummy[name] = value
            except ValueError:
                print('Invalid template variable: {}'.format(variable))
        return  ['{}={}'.format(k,v) for k, v in dummy.items()]

    if setup:
        print('ii')
        initconfig()
        sys.exit()

    try:
        dir = Path(project_dir)
    except TypeError:
        click.echo("\nError: Missing argument 'PROJECT_DIR'.\n\n", err=True)
        sys.exit()

    if not dir.exists():
        dir.mkdir()
    elif dir.is_dir() is not True:
        click.echo("\nError: Your select  project root is already exists. file: {}".format(project_dir), err=True)
        sys.exit()

    d = DEFAULTS.copy()
    d["path"] = project_dir
    d["project"] = project or os.path.basename(project_dir)

    if lang not in ['en', 'ja']:
        try:
            test_import = "from sphinx.locale import {}".format(lang)
            eval(test_import)
        except ImportError:
            click.echo("{} is not supported language, using 'en'".format(lang))
            lang='en'

    if new:
        templatedir = None
        d["author"] = author
        d["version"] = ver
        d["lang"] = lang
        d["variables"] = parse_variables(list(define_value))
    else:
        config = SphinxExpress(configfile)
        least_config = config.load_config()
        least_variable = set(d.get("variables", []))
        define_value = set(define_value)
        d["variables"] = parse_variables(list(least_variable | define_value))
        d.update(**least_config)

    ask_user(d)

    generate(d, templatedir=templatedir)
    for key in IGNORE_OPTIONS:
        d.pop(key)

    config.save_config(d)


if __name__ == "__main__":
    quickstart()
