from distutils.dir_util import copy_tree
from spack import *

class Esp(Package):
    """Engineering SketchPad by Bob Haimes at MIT"""

    homepage = "https://acdl.mit.edu/ESP/"
    url      = "https://acdl.mit.edu/ESP/archive/ESP117Lin.tgz"

    version('117Lin', sha256='bd6418ee9dafabdc17c58449c379535f4f148f1f67730074297c605b5e10e1a0')

    depends_on( 'python@2.6:2.999', type=('run') )

    phases = ['install']


    def install(self, spec, prefix):

      copy_tree('EngSketchPad/lib', prefix.lib)

      copy_tree('OpenCASCADE-7.3.1/lib', prefix.lib)

      copy_tree('EngSketchPad/include', prefix.include)

      copy_tree('EngSketchPad/bin', prefix.bin)

      copy_tree('EngSketchPad/src', prefix.src)

      copy_tree('EngSketchPad/ESP', prefix.ESP)


    def setup_environment(self, spack_env, run_env):

      run_env.prepend_path('PYTHONPATH', self.prefix.lib)
      run_env.set('ESP_START', 'google-chrome '+self.prefix.ESP+'/ESP-localhost7681.html')
      run_env.set('UDUNITS2_XML_PATH', self.prefix+'/src/CAPS/udunits/udunits2.xml')
      run_env.set('ESP_ROOT', self.prefix)
