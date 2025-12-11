class_name Abel_NPC extends NPC


# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "abel"
	character_name = "Abel"
	description = "Professor Richards' former student, ambitious Software Engineering student"
	# pass
