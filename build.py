import os
import shutil
import sys
import sass
import yaml
from pathlib import Path
from staticjinja import Site


def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file.read(), Loader=yaml.Loader)


def print_stage_header(header):
    sys.stderr.write('=== {} === \n'.format(header))


class DocSiteBuilder:
    def __init__(self, build_dir='build'):
        self.build_dir = build_dir

    def build(self, clean=True):
        if clean:
            self.clean()

        self.build_html()
        self.build_assets()
        self.build_stylesheets()

    def build_html(self):
        print_stage_header('rendering jinja templates')
        site = Site.make_site(
            searchpath=os.path.abspath('templates'),
            outpath=os.path.abspath(self.build_dir),
            contexts=[(".*.html", self.jinja_globals)]
        )
        site.render()

    def build_assets(self):
        print_stage_header('copying static assets')
        shutil.copytree('static', os.path.join(self.build_dir, 'static'), dirs_exist_ok=True)

    def build_stylesheets(self):
        print_stage_header('compiling stylesheets')
        sass.compile(dirname=('sass', os.path.join(self.build_dir, 'static/css')))

    def clean(self):
        buildpath = Path(self.build_dir)
        if buildpath.exists() and buildpath.is_dir():
            shutil.rmtree(self.build_dir)

    def jinja_globals(self):
        return {
            "base": load_yaml_file("data/base.yaml"),
            "links": load_yaml_file("data/links.yaml"),
            "pages": load_yaml_file("data/pages.yaml"),
            "projects": load_yaml_file("data/projects.yaml")
        }


if __name__ == "__main__":
    builder = DocSiteBuilder()
    builder.build()
