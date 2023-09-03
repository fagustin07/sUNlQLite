from modules.SunQLite import SunQLite
from modules.compiler import Compiler
from modules.vm import VirtualMachine

compiler = Compiler()
vm = VirtualMachine()
sunqlite = SunQLite(compiler, vm)

sunqlite.start()
