extends Node2D

@export var item : InventoryItem
var player = null

var axe = preload("res://inventory/items/axe.tres")
var player_in_area = false
var state = "axe1" # switch between axe1 and axe2; for testing 

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if state == "axe2":
		$AnimatedSprite2D.play("axe1")
	if state == "axe1":
		$AnimatedSprite2D.play("axe2")
		if Input.is_action_just_pressed("collect_item") and player_in_area == true:
			interact_with_item()

func interact_with_item():
	state == "axe2"
	player.collect_item(item)

#func _on_area_2d_body_entered(body: Node2D) -> void:
	#if body.has_method("Player"):
		#player_in_area = true
		#player = body


#func _on_area_2d_body_exited(body: Node2D) -> void:
	#if body.has_method("Player"):
		#player_in_area = false
	


func _on_pickable_area_body_entered(body: Node2D) -> void:
	if body.has_method("Player"):
		player_in_area = true
		player = body
 
func _on_pickable_area_body_exited(body: Node2D) -> void:
	if body.has_method("Player"):
		player_in_area = false
