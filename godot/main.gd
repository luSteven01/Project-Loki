extends Node

@onready var current_level_node = $WorldContext/CurrentLevel
@onready var player = $WorldContext/Player

@export var starting_scene: PackedScene
@export var starting_position: Vector2 = Vector2(127, 213)

func _ready():
	# $WorldContext.visible = false
	# player.hide()
	# SceneManager.level_change_requested.connect(_on_level_change_requested)
	# get_viewport().set_input_as_handled()

	# Hide world
	$WorldContext.visible = false
	player.hide()

	SceneManager.level_change_requested.connect(_on_level_change_requested)

	# Freeze all gameplay
	get_tree().paused = true
	$CanvasLayer/MainMenu.process_mode = Node.PROCESS_MODE_WHEN_PAUSED

	# Allow MainMenu UI to still receive input
	# $CanvasLayer/MainMenu.pause_mode = Node.PAUSE_MODE_PROCESS


func _on_level_change_requested(new_scene_packed: PackedScene, new_pos: Vector2):
	# Wait for the frame to finish to avoid "Flushing Queries" crash
	call_deferred("_perform_level_change", new_scene_packed, new_pos)

func _perform_level_change(new_scene_packed: PackedScene, new_pos: Vector2):
	print("Main: performing level change...")
	
	if new_scene_packed == null:
		print("CRITICAL ERROR: Main received a NULL scene! The Portal failed to load the file.")
		return

	print("Main: Scene is valid. Swapping rooms now.")

	# 1. Remove the Old Room
	for child in current_level_node.get_children():
		child.queue_free()

	# 2. Add the New Room
	var new_level = new_scene_packed.instantiate()
	current_level_node.add_child(new_level)

	# 3. REPARENT PLAYER
	if player.get_parent() != new_level:
		player.get_parent().remove_child(player)
		new_level.add_child(player)
	print("Player parent after change:", player.get_parent().name)

	# 4. Move Player
	player.global_position = new_pos


func _on_main_menu_start_game() -> void:
	# hide menu
	$CanvasLayer/MainMenu.visible = false
		
	# show world
	$WorldContext.visible = true
	player.show()
	get_tree().paused = false
	
	
	#if starting_scene == null:
		#starting_scene = load("res://living_room.tscn")
	#
	
	# Load the first level immediately (safe to do here)
	_perform_level_change(starting_scene, starting_position)
	# GameManager.init_dialogue_box($CanvasLayer/DialogueBox)
