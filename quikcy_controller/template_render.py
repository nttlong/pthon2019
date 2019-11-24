from mako.template import Template
from .apps import get_root_dir
import os
def render(template_file_path):
    full_path_of_html = os.path.join(get_root_dir(),template_file_path)
    render_template = Template(
        filename= template_file_path,
        module_directory='/tmp/mako_modules')
    return render_template.render()

