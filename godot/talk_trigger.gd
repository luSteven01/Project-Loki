extends Area2D

@onready var game_manager = get_node("/root/Main/GameManager")
@onready var inventory_ui = get_node("/root/Main/CanvasLayer/Inventory_UI")

var current_npc

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("NPC"):
		current_npc = body

func _on_body_exited(body: Node2D) -> void:
	if current_npc == body:
		current_npc = null

func _input(event):
	if Input.is_key_pressed(KEY_F) and not game_manager.is_dialogue_active():
		if current_npc != null:
			game_manager.enter_new_dialogue(current_npc)
			#game_manager.inventory_check()
			get_viewport().set_input_as_handled()
		
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_I and not game_manager.is_dialogue_active():
			print("open inventory ui")
			print(inventory_ui.visible)
			inventory_ui.visible = !inventory_ui.visible
			get_tree().paused = inventory_ui.visible # pause while inventory is open 
	
