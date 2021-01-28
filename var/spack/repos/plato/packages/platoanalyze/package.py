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

    maintainers = ['rviertel', 'jrobbin']

    version('release', branch='release', submodules=True)
    version('develop', branch='develop', submodules=True)

    variant( 'cuda',       default=True,     description='Compile with cuda'            )
    variant( 'mpmd',       default=True,     description='Compile with mpmd'            )
    variant( 'meshmap',    default=True,     description='Compile with MeshMap'         )
    variant( 'amgx',       default=True,     description='Compile with AMGX'            )
    variant( 'openmp',     default=False,    description='Compile with openmp'          )
    variant( 'python',     default=False,    description='Compile with python'          )
    variant( 'geometry',   default=False,    description='Compile with MLS geometry'    )
    variant( 'rocket',     default=False,    description='Builds ROCKET and ROCKET_MPMD')
    variant( 'esp',        default=False,    description='Compile with ESP'             )
    variant( 'tpetra',     default=False,    description='Compile with Tpetra'          )

    depends_on('trilinos+epetra')
    depends_on('trilinos+cuda',                             when='+cuda')
    depends_on('trilinos+openmp',                           when='+openmp')
    depends_on('trilinos+tpetra+belos+ifpack2+amesos2+superlu+muelu',     when='+tpetra')
    depends_on('cmake@3.0.0:', type='build')
    depends_on('python@2.6:2.999',                          when='+python')
    depends_on('platoengine+stk+iso+expy+analyze_tests',    when='+mpmd'  )
    depends_on('platoengine+stk+iso+expy+geometry',         when='+geometry')
    depends_on('platoengine+stk+iso+expy~geometry',         when='~geometry')
    depends_on('platoengine+stk+iso+expy@develop',          when='@develop' )
    depends_on('platoengine+stk+iso+expy@release',          when='@release' )
    depends_on('arborx~mpi~cuda~serial @header_only',       when='+meshmap')
    depends_on('platoengine+stk+iso+expy+esp',              when='+mpmd+esp')
    depends_on('amgx',                                      when='+amgx')
    depends_on('nvccwrapper',                               when='+cuda')
    depends_on('omega-h+trilinos+exodus+cuda @9.26.5',      when='+cuda', type=('build', 'link', 'run'))
    depends_on('omega-h+trilinos+exodus~cuda @9.26.5',      when='~cuda', type=('build', 'link', 'run'))
    depends_on('esp',                                       when='+esp')

    conflicts('+geometry', when='~mpmd')
    conflicts('+meshmap',  when='~mpmd')
    conflicts('+amgx',     when='~cuda')

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

        if '+meshmap' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_MESHMAP=ON' ])

        if '+tpetra' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_TPETRA=ON' ])
          superlu_dir = spec['superlu'].prefix
          options.extend([ '-DSuperLU_PREFIX:PATH={0}'.format(superlu_dir) ])

        if '+esp' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ESP=ON' ])
          esp_lib_dir = spec['esp'].prefix+'/lib'
          esp_inc_dir = spec['esp'].prefix+'/include'
          options.extend([ '-DESP_LIB_DIR:PATH={0}'.format(esp_lib_dir) ])
          options.extend([ '-DESP_INC_DIR:PATH={0}'.format(esp_inc_dir) ])

        if '+amgx' in spec:
          amgx_dir = spec['amgx'].prefix
          options.extend([ '-DAMGX_PREFIX:PATH={0}'.format(amgx_dir) ])

        if '+rocket' in spec:
          options.extend([ '-DPLATOANALYZE_ENABLE_ROCKET=ON' ])


        return options

    def setup_environment(self, spack_env, run_env):

        if '+python' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
