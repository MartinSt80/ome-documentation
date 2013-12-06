#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ome documentation build configuration file, created by
# sphinx-quickstart on Wed Feb 22 20:24:38 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# Append the top level directory of the docs, so we can import from the config dir.
sys.path.insert(0, os.path.abspath('../common'))
from conf import *


# -- General configuration -----------------------------------------------------

# General information about the project.
project = u'OMERO'
title = project + u' Documentation'

def split_release(release):
    import re
    split_release =  re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", release)
    return (int(split_release[1]), int(split_release[2]), int(split_release[3]))

def get_previous_version(majornumber):
    # Return the previous version number for the first minor versions of a
    # major series i.e. x.0.y
    # Implemented as an hard-coded list until we work out an automated way to
    # upgrade the database without specifying version numbers e.g.
    # bin/omero db upgrade
    if majornumber == 5:
        return "4.4"
    elif majornumber == 4:
        return "3.2"
    else:
        raise Exception("No previous version defined for the major release number %s" % majornumber)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
if "OMERO_RELEASE" in os.environ:
    release = os.environ.get('OMERO_RELEASE')
    [majornumber, minornumber, patchnumber] = split_release(release)

    # Define Sphinx version and release variables and development branch
    version = ".".join(str(x) for x in (majornumber, minornumber))
    devbranch = "dev_" + "_".join(str(x) for x in (majornumber, minornumber))

    if patchnumber > 0:
        tags.add('point_release')
    if minornumber > 0:
        previousversion = ".".join(str(x) for x in (majornumber, minornumber - 1))
    else:
        previousversion = get_previous_version(majornumber)
else:
    version = 'UNKNOWN'
    previousversion = 'UNKNOWN'
    release = 'UNKNOWN'
    devbranch = 'develop'

rst_epilog += """
.. |OmeroPy| replace:: :doc:`/developers/Python`
.. |OmeroCpp| replace:: :doc:`/developers/Cpp`
.. |OmeroJava| replace:: :doc:`/developers/Java`
.. |OmeroMatlab| replace:: :doc:`/developers/Matlab`
.. |OmeroApi| replace:: :doc:`/developers/Modules/Api`
.. |OmeroWeb| replace:: :doc:`/developers/Web`
.. |OmeroClients| replace:: :doc:`/developers/GettingStarted`
.. |OmeroGrid| replace:: :doc:`/sysadmins/grid`
.. |OmeroSessions| replace:: :doc:`/developers/Server/Sessions`
.. |OmeroModel| replace:: :doc:`/developers/Model`
.. |ExtendingOmero| replace:: :doc:`/developers/Server/ExtendingOmero`
.. |BlitzGateway| replace:: :doc:`/developers/Python`
.. |DevelopingOmeroClients| replace:: :doc:`/developers/GettingStarted/AdvancedClientDevelopment`
.. _Spring: http://spring.io
.. |previousversion| replace:: %s
.. |devbranch| replace:: %s
.. |iceversion| replace:: 3.5.0
""" % (previousversion, devbranch)

# Variables used to define OMERO Jenkins extlinks
if "JENKINS_JOB" in os.environ:
    jenkins_job = os.environ.get('JENKINS_JOB')
else:
    jenkins_job = 'OMERO-trunk'

omero_job_root = jenkins_job_root + '/' + jenkins_job
virtual_job_root = jenkins_job_root + '/' + jenkins_job + '-virtualbox'

# OMERO-specific extlinks
omero_extlinks = {
    # Github links
    'source' : (omero_github_root + 'blob/'+ branch + '/%s', ''),
    'sourcedir' : (omero_github_root + 'tree/'+ branch + '/%s', ''),   
    'commit' : (omero_github_root + 'commit/%s', ''),
    'omedocs' : (doc_github_root + '%s', ''),
    # Jenkins links
    'omerojob' : (omero_job_root + '/%s', ''),
    'javadoc' : (omero_job_root + '/javadoc/%s', ''),
    'virtualjob' : (virtual_job_root + '/%s', ''),
    # Miscellaneous links
    'springdoc' : ('http://docs.spring.io/spring/docs/%s', ''),
    }
extlinks.update(omero_extlinks)

# -- Options for HTML output ---------------------------------------------------

# Custom sidebar templates, maps document names to template names.
html_sidebars['**'].insert(0, 'globalomerotoc.html')

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path.extend(['themes'])

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
target = project + '-' + release + '.tex'
latex_documents = [
  (master_doc, target, title, author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'images/omero-logo.pdf'


# -- Options for the linkcheck builder ----------------------------------------

# Regular expressions that match URIs that should not be checked when doing a linkcheck build
linkcheck_ignore += [r'http://localhost:\d+/?', 'http://localhost/',
    'http://www.hibernate.org',
    r'^https?://www\.openmicroscopy\.org/site/team/.*',
    r'.*[.]?example\.com/.*',
    r'^https?://www\.openmicroscopy\.org/site/support/faq.*',
    r'^https://spreadsheets.google.com/.*']


# -- Custom roles for the OMERO documentation -----------------------------------------------

from docutils import nodes
from sphinx import addnodes

def omero_command_role(typ, rawtext, etext, lineno, inliner,
                     options={}, content=[]):
    """Role for CLI commands that generates an index entry."""

    env = inliner.document.settings.env
    targetid = 'cmd-%s' % env.new_serialno('index')

    # Create index and target nodes
    indexnode = addnodes.index()
    targetnode = nodes.target('', '', ids=[targetid])
    inliner.document.note_explicit_target(targetnode)
    indexnode['entries'] = [('single', "omero " + "; ".join(etext.split(" ")), targetid, '')]

    # Mark the text using literal node
    sn = nodes.literal('omero ' + etext, 'omero ' +  etext)
    return [indexnode, targetnode, sn], []

def setup(app):
    app.add_role('omerocmd', omero_command_role)
