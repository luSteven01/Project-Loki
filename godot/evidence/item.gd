extends Area2D

@export var item_id: String = ""
@export var is_collected: bool = false
@export var description: String = ""

var player_in_range: bool = false

func _ready() -> void:
	if Global.inventory.has(item_id) and Global.inventory[item_id]["collected"]:
		queue_free()
	
func _process(delta: float) -> void:
	# add item to inventory when E is pressed
	if player_in_range and Input.is_action_just_pressed("ui_add") and not is_collected:
		pickup_item()

func pickup_item() -> void:
	is_collected = true
	
	if $PickUp:
		$PickUp.play()
		await $PickUp.finished

	if Global.player_node:
		Global.add_item(item_id, $Sprite2D.texture, description)
	
	$DeleteTimer.start()


func get_icon() -> Texture2D:
	return $Sprite2D.texture


func _on_delete_timer_timeout() -> void:
	queue_free()


func _on_body_entered(body: Node2D) -> void:
	print("I AM ENTERING enter")
	if body.is_in_group("Player"):
		player_in_range = true
		body.interact_ui.visible = true


func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = false
		body.interact_ui.visible = false
