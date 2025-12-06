extends Area2D

@export var id: String = ""
@export var is_collected: bool = false

var player_in_range: bool = false

func _ready() -> void:
	pass
	


func _on_delete_timer_timeout() -> void:
	queue_free()


func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = true
		body.interact_ui.visible = true


func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = false
		body.interact_ui.visible = false
