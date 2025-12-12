class_name Alice_NPC extends NPC

# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

# handling what sprite to use for NPC
var face_direction = "down" 

var last_position : Vector2

func _ready():
	npc_id = "alice"
	character_name = "Alice"
	description = "Professor Richards' Teaching Assistant"
	animation_player.stop()
	animation_player.play(animation_to_play)
