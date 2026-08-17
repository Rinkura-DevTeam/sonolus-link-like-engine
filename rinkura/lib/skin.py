from sonolus.script.sprite import Sprite, skin, sprite


@skin
class Skin:
    tap: Sprite = sprite("ui_sc2_ingame_notes_tap")
    flick: Sprite = sprite("ui_sc2_ingame_notes_flick")
    flick_arrow: Sprite = sprite("ui_sc2_ingame_notes_texture_arrow")
    hold_head: Sprite = sprite("ui_sc2_ingame_notes_hold")
    trace: Sprite = sprite("ui_sc2_ingame_notes_trace")

    hold_body: Sprite = sprite("rinkura_hold_body_gradient")

    stage: Sprite = sprite("rinkura_stage")

    judgment_line_left: Sprite = sprite("rinkura_judgment_line_left")
    judgment_line_right: Sprite = sprite("rinkura_judgment_line_right")
    judgment_line_center: Sprite = sprite("rinkura_judgment_line_center")

    judgment_perfect_plus: Sprite = sprite("ui_sc2_ingame_hantei_perfect_plus")
    judgment_perfect: Sprite = sprite("ui_sc2_ingame_hantei_perfect")
    judgment_great: Sprite = sprite("ui_sc2_ingame_hantei_great")
    judgment_good: Sprite = sprite("ui_sc2_ingame_hantei_good")
    judgment_bad: Sprite = sprite("ui_sc2_ingame_hantei_bad")
    judgment_miss: Sprite = sprite("ui_sc2_ingame_hantei_miss")

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
