from sonolus.script.engine import TutorialMode

from rinkura.lib.effect import Effects
from rinkura.lib.particle import Particles
from rinkura.lib.skin import Skin
from rinkura.tutorial.instructions import InstructionIcons, Instructions
from rinkura.tutorial.navigate import navigate
from rinkura.tutorial.preprocess import preprocess
from rinkura.tutorial.update import update

tutorial_mode = TutorialMode(
    skin=Skin,
    effects=Effects,
    particles=Particles,
    instructions=Instructions,
    instruction_icons=InstructionIcons,
    preprocess=preprocess,
    navigate=navigate,
    update=update,
)
