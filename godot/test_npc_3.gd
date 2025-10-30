extends CharacterBody2D

@onready var animation_player = $AnimationPlayer
@export var icon : Texture # Holds icon for NPC shown in the dialogue box
@export_multiline var physical_description : String # Describes the character's appearance
@export_multiline var location_description : String # Handles the description of the current area
@export_multiline var personality : String # Handles the character's personality

# replace this with what we need to get from the backend
@export_multiline var secret_knowledge : String 

# replace with other animations from a sprite sheet
var animation_to_play = "front_idle"

func _ready():
	animation_player.stop()
	animation_player.play(animation_to_play)
