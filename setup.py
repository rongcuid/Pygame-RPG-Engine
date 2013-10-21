import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

name = 'Game'
base = 'Console'

if sys.platform == 'win32':
  name = name + '.exe'
 
if sys.platform == "win32":
    base = "Win32GUI"
executables = [
    Executable('Game.py', base = base, targetName = name, compress = True)
]

setup(name='pygame-rpg-engine',
      version = '0.1',
      description = 'Pygame RPG Engine',
      options = dict(build_exe = buildOptions),
      executables = executables)
