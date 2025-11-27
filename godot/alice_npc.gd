class_name Alice_NPC extends NPC

# replace with other animations from a sprite sheet
var animation_to_play = "front_idle"

func _ready():
	npc_id = "alice"
	character_name = "Alice"
	# print("NPC id: " + npc_id)
	# print("NPC name: " + character_name)
	
