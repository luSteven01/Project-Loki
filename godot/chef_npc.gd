class_name Chef_NPC extends NPC


# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "chef"
	character_name = "The Chef"
	description = "Personal chef responsible for cooking food at the dinner party"
	# pass
