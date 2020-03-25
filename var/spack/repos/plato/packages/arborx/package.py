# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arborx(CMakePackage):
    """ArborX is a performance-portable library for geometric search"""

    homepage = "http://github.com/arborx/arborx"
    url      = "https://github.com/arborx/arborx/archive/v0.8-beta2.tar.gz"
    git      = "https://github.com/arborx/arborx.git"

    version('master', branch='master')
    version('header_only', commit='3158660351d69456cc9310c7b325cff7859b90a8')
    version('0.8-beta2', sha256='e68733bc77fbb84313f3ff059f746fa79ab2ffe24a0a391126eefa47ec4fd2df')

    variant('cuda', default=False, description='enable Cuda backend')
    variant('openmp', default=False, description='enable OpenMP backend')
    variant('serial', default=True, description='enable Serial backend (default)')
    variant('mpi', default=True, description='enable MPI')

    depends_on('cmake@3.12:', type='build')
    depends_on('cuda', when='+cuda')
    depends_on('mpi', when='+mpi')

    # ArborX relies on Kokkos to provide devices, thus having one-to-one match
    # The only way to disable those devices is to make sure Kokkos does not
    # provide them
    depends_on('kokkos@2.7.00:+cuda+enable_lambda cxxstd=c++14', when='+cuda')
    depends_on('kokkos@2.7.00:+openmp cxxstd=c++14', when='+openmp')
    depends_on('kokkos@2.7.00:+serial cxxstd=c++14', when='+serial')

    patch('header_only.patch')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DARBORX_ENABLE_TESTS=OFF',
            '-DARBORX_ENABLE_EXAMPLES=OFF',
            '-DARBORX_ENABLE_BENCHMARKS=OFF',
            '-DARBORX_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF')
        ]

        if '+cuda' in spec or '+serial' in spec or '+openmp' in spec:
            '-DCMAKE_PREFIX_PATH=%s' % spec['kokkos'].prefix,
            nvcc_wrapper_path = spec['kokkos'].prefix.bin.nvcc_wrapper
            options.append('-DCMAKE_CXX_COMPILER=%s' % nvcc_wrapper_path)
        else:
            options.append('-DARBORX_ENABLE_HEADERONLY=ON')

        return options

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('CPATH', join_path(self.prefix, 'include', 'details'))
        spack_env.prepend_path('CPATH', join_path(self.prefix, 'include'))
        spack_env.prepend_path('CPATH', join_path(self.prefix, 'include', 'details'))
