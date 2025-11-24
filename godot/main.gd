extends Node

@onready var current_level_node = $WorldContext/CurrentLevel
@onready var player = $WorldContext/Player
@export var starting_scene: PackedScene
@export var starting_position: Vector2 = Vector2(127, 213)

func _ready():
	# Connect to SceneManager for the signal
	SceneManager.level_change_requested.connect(_on_level_change_requested)
	if starting_scene == null:
		starting_scene = load("res://living_room.tscn")
	_on_level_change_requested(starting_scene, starting_position)
	
func _on_level_change_requested(new_scene_packed: PackedScene, new_pos: Vector2):
	# Clear the old room
	# We look at the children of the container. If there's a room there, remove it.
	for child in current_level_node.get_children():
		child.queue_free()
	
	# Add the new room
	var new_level = new_scene_packed.instantiate()
	current_level_node.add_child(new_level)
	
	# Move the player
	# Since the player is a child of Main, we can just move them directly.
	player.global_position = new_pos
