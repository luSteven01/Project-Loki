class_name Alice_NPC extends NPC

@onready var animation_player = $AnimationPlayer
@onready var iconNode := get_node("/root/DialogueBox/NPCIcons/Alice")

# replace with other animations from a sprite sheet
var animation_to_play = "front_idle"

func _ready():
	# animation_player.stop()
	# animation_player.play(animation_to_play)
	pass
