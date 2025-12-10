class_name Professor_Schumacher_NPC extends NPC


# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "schumacher"
	character_name = "Professor Schumacher"
	description = "Professor Richards' colleague"
	# pass
