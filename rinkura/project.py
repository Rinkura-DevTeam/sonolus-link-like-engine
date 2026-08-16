from sonolus.script.engine import Engine, EngineData
from sonolus.script.project import Project

from rinkura.lib.options import Options
from rinkura.lib.ui import ui_config
from rinkura.level import load_levels
from rinkura.play.mode import play_mode
from rinkura.preview.mode import preview_mode
from rinkura.tutorial.mode import tutorial_mode
from rinkura.watch.mode import watch_mode

engine = Engine(
    name="rinkura",
    title="Link! Like!",
    skin="pixel",
    particle="pixel",
    background="vanilla",
    effect="8bit",
    data=EngineData(
        ui=ui_config,
        options=Options,
        play=play_mode,
        watch=watch_mode,
        preview=preview_mode,
        tutorial=tutorial_mode,
    ),
)

project = Project(
    engine=engine,
    levels=load_levels,
)
