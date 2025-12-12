extends CharacterBody2D

@onready var animation_player = $AnimationPlayer
@onready var inventory_ui = $InventoryUI
@onready var interact_ui = $InteractUI
@onready var item_message_ui = $ItemMessage
@onready var item_message = $ItemMessage/ColorRect/RichTextLabel
@onready var hide_ui = $HideUITimer
@onready var game_manager = get_node("/root/Main/GameManager")
@onready var door_message_ui = $DoorMessage
@onready var door_message = $DoorMessage/ColorRect/Label


# Player moves at 50 pixels/second
var speed : float = 100.0
var step_time = 0.6
var timer = 0.0

# handling what sprite to use when pressing arrow keys
var face_direction = "down" 
var animation_to_play = "down_idle"

func _ready():
	Global.init_player_reference(self)
	process_mode = Node.PROCESS_MODE_ALWAYS
	animation_player.stop()
	animation_player.play("down_idle")
	inventory_ui.visible = false
	interact_ui.visible = false
	item_message_ui.visible = false
	door_message_ui.visible = false


func _input(event):
	if event.is_action_pressed("ui_inventory") and not game_manager.is_dialogue_active():
		inventory_ui.visible = !inventory_ui.visible
		get_tree().paused = inventory_ui.visible # pause while inventory is open 
		
	if event is InputEventMouseButton \
	and event.button_index == MOUSE_BUTTON_LEFT \
	and event.pressed \
	and item_message_ui.visible:
		hide_item_message()

func show_item_message(popup_message):
	item_message_ui.visible = true
	item_message.text = popup_message

	
# for setting velocity and performing other physics calculations
func _physics_process(delta):
	if GameManager.is_dialogue_active():
		return

	if get_tree().paused:
		return
	# Generates movement direction vector based on inputs we supply 
	var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	
	# player velocity set based on direction vector
	velocity = direction * speed
	
	# using 360 deg movement; cannot assume vertical motion so we take the biggest one 
	if direction.length() > 0:
		timer -= delta
		if abs(direction.x) > abs(direction.y):
			face_direction = "left" if direction.x < 0 else "right" 
		else:
			face_direction = "up" if direction.y < 0 else "down"
		
		if timer <= 0:
			$WalkingSound.play()
			timer = step_time
	else:
		timer = 0	
		
	animation_to_play = face_direction + "_" + ("walk" if velocity.length() > 0.0 else "idle")
	animation_player.play(animation_to_play)
	# applies velocity to move character
	move_and_slide()


func hide_item_message() -> void:
	item_message_ui.visible = false

var _door_prompt_sources := {}

func show_door_prompt(text: String, source: Node) -> void:
	_door_prompt_sources[source] = text
	door_message_ui.visible = true
	door_message.text = text

func hide_door_prompt(source: Node) -> void:
	_door_prompt_sources.erase(source)
	if _door_prompt_sources.is_empty():
		door_message_ui.visible = false
	else:
		var last_source = _door_prompt_sources.keys()[-1]
		door_message.text = _door_prompt_sources[last_source]
