from sonolus.script.bucket import Bucket, bucket, bucket_sprite, buckets
from sonolus.script.text import StandardText

from rinkura.lib.skin import Skin


@buckets
class Buckets:
    tap: Bucket = bucket(
        sprites=[
            bucket_sprite(
                sprite=Skin.tap,
                x=0,
                y=0,
                w=2,
                h=2,
            )
        ],
        unit=StandardText.MILLISECOND_UNIT,
    )
    flick: Bucket = bucket(
        sprites=[
            bucket_sprite(
                sprite=Skin.flick,
                x=0,
                y=0,
                w=2,
                h=2,
            ),
            bucket_sprite(
                sprite=Skin.flick_arrow,
                x=0,
                y=1.3,
                w=1.2,
                h=1.2,
            ),
        ],
        unit=StandardText.MILLISECOND_UNIT,
    )
    trace: Bucket = bucket(
        sprites=[
            bucket_sprite(
                sprite=Skin.trace,
                x=0,
                y=0,
                w=2,
                h=2,
            )
        ],
        unit=StandardText.MILLISECOND_UNIT,
    )
    hold: Bucket = bucket(
        sprites=[
            bucket_sprite(
                sprite=Skin.hold_head,
                x=0,
                y=0,
                w=2,
                h=2,
            )
        ],
        unit=StandardText.MILLISECOND_UNIT,
    )