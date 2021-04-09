import pkg_resources
import shutil
import pathlib
import typer
import sphinx
from .configs import RECOMEND_MODULES, DEFAULT_CONFIG
from .templates import REPLACE_CONFIGS, APPEND_CONFIGS

def initconfig(config):
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = RECOMEND_MODULES - installed

    if missing:
        pkgs = " ".join(str(e) for e in missing)
        typer.echo("\nYou should install follows packages.")
        typer.echo("python -m pip install {}".format(pkgs))

    config_data = config.load_config(DEFAULT_CONFIG)
    config.save_config(config_data)

    pathlib.Path(config.default_templatedir).mkdir(parents=True, exist_ok=True)
    sphinx_module_dir = pathlib.Path(sphinx.__file__).parent()
    sphinx_template_dir = pathlib.Path(sphinx_module_dir) / "templates/quickstart"
    files = sphinx_template_dir.glob("*")
    for f in files:
        shutil.copy(f, config.default_templatedir)

    for pattern in REPLACE_CONFIGS.keys():
        config.replace_config_template(pattern, REPLACE_CONFIGS[pattern])

    config.append_config_template(APPEND_CONFIGS)

    typer.echo("\nyour configfile: {}".format(config.configfile))
    typer.echo("your templatedir: {}".format(config.default_templatedir))
    typer.echo("quickstart templates of sphinx into your templatedir.\n")

