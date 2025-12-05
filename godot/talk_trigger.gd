extends Area2D

@onready var game_manager = get_node("/root/Main/GameManager")

var current_npc

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("NPC"):
		current_npc = body

func _on_body_exited(body: Node2D) -> void:
	if current_npc == body:
		current_npc = null

func _input(event):
	if Input.is_key_pressed(KEY_F): # and game_manager.is_dialogue_active() == false
		if current_npc != null:
			game_manager.enter_new_dialogue(current_npc)
			#game_manager.inventory_check()
			#game_manager.dialogue_box.inventory_ui.visible = true;
			get_viewport().set_input_as_handled()
