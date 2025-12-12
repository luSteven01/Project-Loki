extends Control
signal start_game
signal credits

var credits_scene: Control

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	credits_scene = $CanvasLayer/CreditsScene
	credits_scene.visible = false


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_just_pressed("interact") or Input.is_key_pressed(KEY_ENTER) or Input.is_key_pressed(KEY_KP_ENTER):
		_on_start_button_pressed()


func _on_start_button_pressed() -> void:
	start_game.emit()


func _on_credits_button_pressed() -> void:
	credits.emit()


func _on_exit_button_pressed() -> void:
	get_tree().quit()


func _on_credits() -> void:
	credits_scene.visible = true


func _on_credits_scene_close() -> void:
	credits_scene.visible = false
