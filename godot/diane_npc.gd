class_name Diane_NPC extends NPC


# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "diane"
	character_name = "Diane"
	description = "Abel's mother, dean of the university"
	# pass
