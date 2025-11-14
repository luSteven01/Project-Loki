extends CharacterBody2D

@onready var animation_player = $AnimationPlayer
# @export var inventory : Inventory

# Player moves at 50 pixels/second
var speed : float = 100.0

# handling what sprite to use when pressing arrow keys
var face_direction = "down"
var animation_to_play = "down_idle"

func _ready():
	animation_player.stop()
	animation_player.play("down_idle")
	
# for setting velocity and performing other physics calculations
func _physics_process(delta):
	# Generates movement direction vector based on inputs we supply 
	var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	
	# player velocity set based on direction vector
	velocity = direction * speed
	
	# using 360 deg movement; cannot assume vertical motion so we take the biggest one 
	if direction.length() > 0:
		if abs(direction.x) > abs(direction.y):
			face_direction = "left" if direction.x < 0 else "right" 
		else:
			face_direction = "up" if direction.y < 0 else "down"
	
	# if we get another sprite sheet thats a lot better for characters, uncomment this line
	animation_to_play = face_direction + "_" + ("walk" if velocity.length() > 0.0 else "idle")
	animation_player.play(animation_to_play)
	# applies velocity to move character
	move_and_slide()
	# pass
