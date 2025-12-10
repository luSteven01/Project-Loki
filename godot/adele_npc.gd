class_name Adele_NPC extends NPC


# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "adele"
	character_name = "Adele"
	description = "Professor Richards' wife, party hostess"
	# pass
