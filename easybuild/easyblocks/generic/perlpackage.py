##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for Perl packages, implemented as an easyblock

@author: Jens Timmerman (Ghent University)
"""
import os

from easybuild.easyblocks.perl import EXTS_FILTER_PERL_PACKAGES
from easybuild.framework.easyconfig import CUSTOM
from easybuild.framework.extensioneasyblock import ExtensionEasyBlock
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.filetools import run_cmd


class PerlPackage(ExtensionEasyBlock, ConfigureMake):
    """Builds and installs a Perl package, and provides a dedicated module file."""

    @staticmethod
    def extra_options():
        """Easyconfig parameters specific to Python packages."""
        extra_vars = [
            ('runtest', [True, "Run unit tests.", CUSTOM]),  # overrides default
        ]
        return ExtensionEasyBlock.extra_options(extra_vars)

    def __init__(self, *args, **kwargs):
        """Initialize custom class variables."""
        super(PerlPackage, self).__init__(*args, **kwargs)
        self.testcmd = None

    def configure_step(self):
        """Configure Python package build."""


    def run(self):
        """Perform the actual Python package build/installation procedure"""

        if not self.src:
            self.log.error("No source found for Perl package %s, required for installation. (src: %s)" %
                           (self.name, self.src))
        ExtensionEasyBlock.run(self, unpack_src=True)

        # Perl packages have to possible installations, Makefile.PL and Build.PL

        # configure, build, test, install
        if os.path.exists('Makefile.PL'):
            run_cmd('perl Makefile.PL PREFIX=%s' % self.installdir)
            ConfigureMake.build_step(self)
            ConfigureMake.test_step(self)
            ConfigureMake.install_step(self)
        elif os.path.exists('Build.PL'):
            run_cmd('perl Build.PL --prefix %s' % self.installdir)
            out, ec  = run_cmd('./Build test')
            out, ec  = run_cmd('./Build install')



    def sanity_check_step(self, *args, **kwargs):
        """
        Custom sanity check for Perl packages
        """
        ExtensionEasyBlock.sanity_check_step(self, EXTS_FILTER_PERL_PACKAGES, *args, **kwargs)

    def make_module_extra(self):
        """Add install path to PYTHONPATH"""
        txt = self.moduleGenerator.prepend_paths("PERL5LIB", [self.installdir])
        return ExtensionEasyBlock.make_module_extra(self, txt)
