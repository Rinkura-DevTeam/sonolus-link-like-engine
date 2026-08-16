from rinkura.lib.buckets import Buckets
from rinkura.lib.effect import Effects
from rinkura.lib.particle import Particles
from rinkura.lib.skin import Skin
from rinkura.watch.update_spawn import update_spawn
from sonolus.script.engine import WatchMode

watch_mode = WatchMode(
    archetypes=[],
    skin=Skin,
    effects=Effects,
    particles=Particles,
    buckets=Buckets,
    update_spawn=update_spawn,
)
