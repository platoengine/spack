##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Platoanalyze(CMakePackage):
    """Plato Analyze"""

    homepage = "https://github.com/platoengine/platoanalyze"
    url      = "https://github.com/platoengine/platoanalyze"
    git      = "https://github.com/platoengine/platoanalyze.git"

    maintainers = ['rvierte@sandia.gov', 'jrobbin@sandia.gov']

    version('master', branch='master', submodules=True)

    variant( 'cuda',       default=True,     description='Compile with cuda'            )
    variant( 'mpmd',       default=True,     description='Compile with mpmd'            )
    variant( 'python',     default=False,    description='Compile with python'          )
    variant( 'geometry',   default=False,    description='Compile with MLS geometry'    )
    variant( 'rocket',     default=False,    description='Builds ROCKET and ROCKET_MPMD')

    depends_on('cmake@3.0.0:', type='build')
    depends_on('python@2.6:2.999',                          when='+python')
    depends_on('platoengine+analyze_tests',                 when='+mpmd'  )
    depends_on('platoengine+geometry',                      when='+geometry')
    depends_on('platoengine~geometry',                      when='~geometry')
    depends_on('platoengine+cuda',                          when='+cuda+mpmd')
    depends_on('platoengine~cuda',                          when='~cuda+mpmd')
    depends_on('amgx',                                      when='+cuda')
    depends_on('nvccwrapper',                               when='+cuda')
    depends_on('omega-h+trilinos+exodus+cuda @9.26.5',      when='+cuda')
    depends_on('omega-h+trilinos+exodus~cuda @9.26.5',      when='~cuda')

    conflicts('+geometry', when='~mpmd')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([ '-DBUILD_SHARED_LIBS:BOOL=ON' ])

        trilinos_dir = spec['trilinos'].prefix
        options.extend([ '-DTrilinos_PREFIX:PATH={0}'.format(trilinos_dir) ])

        if '+mpmd' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MPMD=ON' ])

          platoengine_dir = spec['platoengine'].prefix
          options.extend([ '-DPLATOENGINE_PREFIX:PATH={0}'.format(platoengine_dir) ])

          omega_h_dir = spec['omega-h'].prefix
          options.extend([ '-DOMEGA_H_PREFIX:PATH={0}'.format(omega_h_dir) ])

        if '~mpmd' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MPMD=OFF' ])

        if '+python' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_PYTHON=ON' ])

        if '+geometry' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_GEOMETRY=ON' ])

        if '+cuda' in spec:
          amgx_dir = spec['amgx'].prefix
          options.extend([ '-DAMGX_PREFIX:PATH={0}'.format(amgx_dir) ])

        if '+rocket' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ROCKET=ON' ])


        return options

    def setup_environment(self, spack_env, run_env):

        if '+python' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
