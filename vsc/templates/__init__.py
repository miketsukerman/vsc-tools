import os

from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined
from jinja2 import Template as VscTemplate
from typing import Any

from vsc.templates.simple_doc import SimpleDocTemplatePath
from vsc.templates.protobuf import ProtobufTemplatePath
from vsc.templates.sds import SdsBammAspectModelTemplatePath
from vsc.templates.dtdl import DtdlTemplatePath
from vsc.templates.test import TestTemplatePath

BaseTemplatePath = os.path.dirname(os.path.realpath(__file__))

TemplatePaths = [BaseTemplatePath
                , SimpleDocTemplatePath
                , ProtobufTemplatePath
                , SdsBammAspectModelTemplatePath
                , DtdlTemplatePath
                , TestTemplatePath
                ]

# Set up Jinja
vsc_tpl_env = Environment(
        # Use the subdirectory 'templates' relative to this file's location
        loader=FileSystemLoader(TemplatePaths),

        # Templates with these extension gets automatic auto escape for HTML
        # It's more annoying for code generation, so passing empty list for now.
        autoescape=select_autoescape([])
        )

# We want the control blocks in the template to NOT result in any extra
# white space when rendering templates. However, this might be a choice
# made by each generator, so we need to export the ability to keep these
# settings public for other code to modify them.
vsc_tpl_env.trim_blocks = True
vsc_tpl_env.lstrip_blocks = True
vsc_tpl_env.undefined = StrictUndefined

# This is a default definition for our current generation tests.
# It may need to be changed, or defined differently in a custom generator
default_templates = {
        'Argument': 'Argument-simple_doc.html.j2',
        'Error': 'Error-simple_doc.html.j2',
        'Member': 'Member-simple_doc.html.j2',
        'Namespace': 'Namespace-simple_doc.html.j2',
        'Argument': 'Argument-simple_doc.html.j2'
        }

# Get template with given name (search path should be handled by the loader)
def get_template(filename):
    return vsc_tpl_env.get_template(filename)

# Update global environment for templates
def set_template_env(**kwargs: Any):
    vsc_tpl_env.globals.update(kwargs)
    