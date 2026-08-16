"""
rinkura/lib/skin.py

Sprite identifiers mapped to confirmed LLL texture assets.
All filenames below verified directly against extracted asset dump
(~/rinkura_assets/textures/), stripped of the trailing UnityPy path_id
suffix (e.g. "_510") since that suffix is an artifact of the extraction
pipeline, not part of the in-game asset name.

Resource packaging note: whatever name is registered here via sprite(...)
must exactly match the filename used when building the Sonolus resource
package (i.e. the file placed under the engine's resources directory).
If the packaging step keeps the numeric suffix, update the names below
to match.
"""

from sonolus.script.sprite import Sprite, skin, sprite


@skin
class Skin:
    # Note textures - confirmed 1:1 against extracted assets
    tap: Sprite = sprite("ui_sc2_ingame_notes_tap")
    flick: Sprite = sprite("ui_sc2_ingame_notes_flick")
    flick_arrow: Sprite = sprite("ui_sc2_ingame_notes_texture_arrow")
    hold_head: Sprite = sprite("ui_sc2_ingame_notes_hold")
    trace: Sprite = sprite("ui_sc2_ingame_notes_trace")

    # Hold body and lane line: NOT present in LLL assets (procedural mesh
    # in the original game). These are custom rinkura-authored textures
    # approximating the mesh gradient as a static sprite, since Sonolus
    # can only draw textured quads, not generate custom meshes.
    hold_body: Sprite = sprite("rinkura_hold_body_gradient")
    lane_line: Sprite = sprite("rinkura_lane_line_fade")

    # Judgment line: CONFIRMED source is sc2_ingame_tap_line (168x54),
    # not ui_sc2_ingame_end_line (that asset is unrelated, likely a
    # different UI element - visual mismatch confirmed, no chevrons).
    #
    # Sonolus Sprite.draw() always stretches the full source image into
    # the given layout quad - there is no runtime UV/crop parameter.
    # To get a fixed-size-caps + stretchable-center line, the source
    # texture was physically pre-cropped into three separate PNG files
    # (see rinkura_custom_sprites/), each registered as its own sprite:
    #   left cap:     x 0-84 of source   (contains 3 converging chevrons)
    #   right cap:    x 84-168 of source (mirror of left cap)
    #   center strip: x 83-85 of source  (2px sliver, drawn stretched
    #                                     to fill the gap between caps)
    # Confirmed via mockup render - produces a seamless line with
    # fixed-size arrows and a smoothly stretched center.
    judgment_line_left: Sprite = sprite("rinkura_judgment_line_left")
    judgment_line_right: Sprite = sprite("rinkura_judgment_line_right")
    judgment_line_center: Sprite = sprite("rinkura_judgment_line_center")

    # Judgment result sprites - confirmed 1:1
    judgment_perfect_plus: Sprite = sprite("ui_sc2_ingame_hantei_perfect_plus")
    judgment_perfect: Sprite = sprite("ui_sc2_ingame_hantei_perfect")
    judgment_great: Sprite = sprite("ui_sc2_ingame_hantei_great")
    judgment_good: Sprite = sprite("ui_sc2_ingame_hantei_good")
    judgment_bad: Sprite = sprite("ui_sc2_ingame_hantei_bad")
    judgment_miss: Sprite = sprite("ui_sc2_ingame_hantei_miss")

    # Combo digits - confirmed present as individual 0-9 sprites
    combo_digit_0: Sprite = sprite("ui_sc2_ingame_num_combo_0")
    combo_digit_1: Sprite = sprite("ui_sc2_ingame_num_combo_1")
    combo_digit_2: Sprite = sprite("ui_sc2_ingame_num_combo_2")
    combo_digit_3: Sprite = sprite("ui_sc2_ingame_num_combo_3")
    combo_digit_4: Sprite = sprite("ui_sc2_ingame_num_combo_4")
    combo_digit_5: Sprite = sprite("ui_sc2_ingame_num_combo_5")
    combo_digit_6: Sprite = sprite("ui_sc2_ingame_num_combo_6")
    combo_digit_7: Sprite = sprite("ui_sc2_ingame_num_combo_7")
    combo_digit_8: Sprite = sprite("ui_sc2_ingame_num_combo_8")
    combo_digit_9: Sprite = sprite("ui_sc2_ingame_num_combo_9")
    combo_label: Sprite = sprite("ui_sc2_ingame_combo")


HOLD_BODY_CENTER_COLOR = (0.18039216, 0.77647060, 1.0, 0.2)
HOLD_BODY_SIDE_COLOR = (0.17647059, 0.97254902, 1.0, 0.6)
LANE_LINE_COLOR = (1.0, 1.0, 1.0, 0.3)
