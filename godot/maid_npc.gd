class_name Maid_NPC extends NPC

var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
	npc_id = "maid"
	character_name = "The Maid"
	description = "Maid that greets everyone at the party and tends to household tasks"
