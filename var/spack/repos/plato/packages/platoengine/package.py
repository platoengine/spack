# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Platoengine(CMakePackage):
    """Plato Engine - Platform for Topology Optimization"""
    
    homepage = "https://www.sandia.gov/plato3d/"
    url      = "https://github.com/platoengine/platoengine/archive/v0.6.0.tar.gz"
    git      = "https://github.com/platoengine/platoengine.git"

    maintainers = ['rviertel', 'jrobbin']

    version('release', branch='release', preferred=True)
    version('0.6.0', sha256='893f9d6f05ef1d7ca563fcc585e92b2153eb6b9f203fb4cadc73a00da974ac20')
    version('0.5.0', sha256='dc394819026b173749f78ba3a66d0c32d4ec733b68a4d004a4acb70f7668eca2')
    version('0.4.0', sha256='642404480ea2e9b7a2bffcfcc2d526dea2f1b136d786e088a5d91a4ff21b8ef2')
    version('0.3.0', sha256='dfc362e9bb6aaa263ae21cb090bd5f816959e54277bc2488cd4f2830217de5a4')
    version('0.2.0', sha256='16619c21000f3fa5b0cc1b54b06ee60a691dd7cbce2c8c7baeb0881ab76d4d09')
    version('0.1.0', sha256='9bc3e2a89deeaf1c474c3109952d95c63cc027a1aafe272b97ee75bd876ac4b0')

    variant( 'platomain',      default=True,    description='Compile PlatoMain'         )
    variant( 'platostatics',   default=True,    description='Compile PlatoStatics'      )
    variant( 'unit_testing',   default=True,    description='Add unit testing'          )
    variant( 'regression',     default=True,    description='Add regression tests'      )
    variant( 'platoproxy',     default=False,   description='Compile PlatoProxy'        )
    variant( 'expy',           default=False,   description='Compile exodus/python API' )
    variant( 'geometry',       default=False,   description='Turn on Plato Geometry'    )
    variant( 'iso',            default=False,   description='Turn on iso extraction'    )
    variant( 'esp',            default=False,   description='Turn on esp'               )
    variant( 'stk',            default=False,   description='Turn on use of stk'        )
    variant( 'rol',            default=False,   description='Turn on use of rol'        )
    variant( 'cuda',           default=False,   description='Compile with cuda'         )
    variant( 'albany_tests',   default=False,   description='Configure Albany tests'    )
    variant( 'analyze_tests',  default=False,   description='Configure Analyze tests'   )
    variant( 'tpetra_tests',   default=False,   description='Configure Tpetra tests'    )

    conflicts( '+expy', when='-platomain')
    conflicts( '+iso',  when='-stk')

    depends_on( 'trilinos')
    depends_on( 'mpi',            type=('build','link','run'))
    depends_on( 'cmake@3.0.0:',   type='build')
    depends_on( 'trilinos+rol',                               when='+rol')
    depends_on( 'trilinos+zlib+pnetcdf+boost \
                                       +stk+gtest',           when='+stk')
    depends_on( 'trilinos+zlib+pnetcdf+boost+intrepid2 \
                             +minitensor+pamgen',             when='+geometry')
    depends_on( 'googletest',                                 when='+unit_testing' )
    depends_on( 'python@2.6:2.999',                           when='+expy'         )
    depends_on( 'nlopt',                                      when='+expy'         )
    depends_on( 'py-numpy@1.16.5',                            when='+expy'         )
    depends_on( 'nvccwrapper',                                when='+cuda')
    depends_on( 'trilinos+cuda',                              when='+cuda')

    depends_on( 'esp', when='+esp')


    def cmake_args(self):
        spec = self.spec

        options = []

        trilinos_dir = spec['trilinos'].prefix
        options.extend([ '-DSEACAS_PATH:FILEPATH={0}'.format(trilinos_dir) ])
        options.extend([ '-DTRILINOS_INSTALL_DIR:FILEPATH={0}'.format(trilinos_dir) ])

        if '+platomain' in spec:
          options.extend([ '-DPLATOMAIN=ON' ])

        if '+platoproxy' in spec:
          options.extend([ '-DPLATOPROXY=ON' ])

        if '+platostatics' in spec:
          options.extend([ '-DPLATOSTATICS=ON' ])

        if '+expy' in spec:
          options.extend([ '-DEXPY=ON' ])
          options.extend([ '-DPLATO_ENABLE_SERVICES_PYTHON=ON' ])

        if '+regression' in spec:
          options.extend([ '-DREGRESSION=ON' ])
          options.extend([ '-DSEACAS=ON' ])

        if '+unit_testing' in spec:
          options.extend([ '-DUNIT_TESTING=ON' ])
          gtest_dir = spec['googletest'].prefix
          options.extend([ '-DGTEST_HOME:FILEPATH={0}'.format(gtest_dir) ])

        if '+iso' in spec:
          options.extend([ '-DENABLE_ISO=ON' ])

        if '+geometry' in spec:
          options.extend([ '-DGEOMETRY=ON' ])

        if '+stk' in spec:
          options.extend([ '-DSTK_ENABLED=ON' ])

        if '+esp' in spec:
          options.extend([ '-DESP_ENABLED=ON' ])
          esp_lib_dir = spec['esp'].prefix+'/lib'
          esp_inc_dir = spec['esp'].prefix+'/include'
          options.extend([ '-DESP_LIB_DIR:PATH={0}'.format(esp_lib_dir) ])
          options.extend([ '-DESP_INC_DIR:PATH={0}'.format(esp_inc_dir) ])

        if '+rol' in spec:
          options.extend([ '-DENABLE_ROL=ON' ])

        if '-stk' in spec:
          options.extend([ '-DSTK_ENABLED=OFF' ])

        if '+albany_tests' in spec:
          options.extend([ '-DALBANY=ON' ])
          options.extend([ '-DALBANY_BINARY=AlbanyMPMD' ])

        if '+analyze_tests' in spec:
          options.extend([ '-DANALYZE=ON' ])
          options.extend([ '-DANALYZE_BINARY=analyze_MPMD' ])

        if '+tpetra_tests' in spec:
          options.extend([ '-DPLATO_TPETRA=ON' ])

        return options


    def setup_environment(self, spack_env, run_env):

        if '+expy' in self.spec:
          run_env.prepend_path('PYTHONPATH', self.prefix.lib)
          run_env.prepend_path('PYTHONPATH', self.prefix.etc)
