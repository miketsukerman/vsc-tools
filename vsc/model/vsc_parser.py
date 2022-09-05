# SPDX-License-Identifier: MPL-2.0
# ----------------------------------------------------------------------------
# (C) 2021 COVESA
# Reader/parser module
# To be used by all generators and other tools
# ----------------------------------------------------------------------------

"""
VSC parser/reader to be used by generators and other tools
"""

# This performs the following related functions:

# 1. Read a service description file from its YAML format into it simple
#    representation of dicts and lists.  This model the structure of the YAML
#    file, but contains basically the plain text items therein with no more
#    elaborate type information.  It is done using the standard 'yaml'
#    library of python.
#
# 2. Go through the tree and create a linked tree of Nodes (instances of
#    typed classes).  Each node gets a more specific type than
#    dict/list/string which can be used to evaluate the tree contents later.
#    In most parsers, this is referred to an Abstract Syntax Tree (AST)
#    representation of the program.
#    The nodes are also inheriting functionality from the base Node type of
#    the anytree library, which means convenience functions from anytree
#    can be used to manipulate the tree later.
#
# 3. Indirectly, when building the AST, it is done with knowledge about
#    which node types are expected and belong there, and so it can check
#    and report if certain conditions are not met.  It does not check all
#    possible rules however, and would be well complimented by a schema
#    checker.

import yaml, dacite
from typing import Dict, Any
from vsc.model.vsc_ast import Namespace

def read_yaml_file(filename) -> str:
    """
    Tries to read a file which contains yaml into a string
    FIXME: Might work slow on big YAML files.
    :param filename:
    :return: file contents as string
    """
    with open(filename, 'r') as yaml_file:
        return yaml_file.read()


def parse_yaml_file(yaml_string: str) -> Dict[Any, Any]:
    """
    Tries to parse yaml into a python dictionary
    :param yaml_string: String containing text in YAML format
    :return: Dictionary
    """
    return yaml.safe_load(yaml_string)


def read_ast_from_yaml_file(filename: str) -> Namespace:
    """
    Reads a yaml file and returns AST
    :param filename: path to a yaml file
    :return: abstract syntax tree (vehicle service catalog)
    """

    yaml_string = read_yaml_file(filename)

    yaml_dict = parse_yaml_file(yaml_string)

    ast = dacite.from_dict(data_class=Namespace, data=yaml_dict)

    return ast


def get_ast_from_file(filepath : str):
    """
    Wrapper over read_ast_from_yaml_file to keep API consistent
    Args:
        filepath (str): path to the YAML file

    Returns:
        _type_: AST root 
    """
    return read_ast_from_yaml_file(filepath)
