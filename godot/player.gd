extends CharacterBody2D

@export var speed: float = 100.0

var can_move: bool = true

func _ready():
	pass

func _physics_process(delta: float) -> void:
	var direction = Vector2.ZERO
	if Input.is_action_pressed("move_right"):
		direction.x += 1
	if Input.is_action_pressed("move_left"):
		direction.x -= 1
	if Input.is_action_pressed("move_down"):
		direction.y += 1
	if Input.is_action_pressed("move_up"):
		direction.y -= 1
		
	if direction.length() > 0:
		direction = direction.normalized()
		$AnimatedSprite2D.play()
	else:
		$AnimatedSprite2D.stop()
		
	if direction.x < 0: # Moving Left
		$AnimatedSprite2D.animation = "walk_left"
	elif direction.x > 0: # Moving Right
		$AnimatedSprite2D.animation = "walk_right"
	elif direction.y < 0: # Moving Up (only if not moving left or right)
		$AnimatedSprite2D.animation = "walk_up"
	elif direction.y > 0: # Moving Down (only if not moving left or right)
		$AnimatedSprite2D.animation = "walk_down"
	
	velocity = direction * speed

	move_and_slide()
