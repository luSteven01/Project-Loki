class_name Alice_NPC extends NPC

# replace with other animations from a sprite sheet
var animation_to_play = "down_idle"

# handling what sprite to use for NPC
var face_direction = "down" 

var last_position : Vector2

func _ready():
	npc_id = "alice"
	character_name = "Alice"
	animation_player.stop()
	animation_player.play(animation_to_play)
	#speed = 25.0
	#loop_path = true
	#position = path_follow.global_position
	#print("alice's position: ", position)
	#last_position = position
	# animation_to_play = face_direction + "_" + ("walk" if movement.length() > 0.0 else "idle")
	# print("NPC id: " + npc_id)
	# print("NPC name: " + character_name)

#func _physics_process(delta):
	#path_follow.progress += speed * delta
	#position = path_follow.global_position
	#
	#var movement := position - last_position
	#if movement.length() > 0.1:
		#_update_animation(movement)
	#last_position = position
#
#func _update_animation(movement: Vector2) -> void:	
	#if abs(movement.x) > abs(movement.y):
		#face_direction = "left" if movement.x < 0 else "right" 
	#else:
		#face_direction = "up" if movement.y < 0 else "down"
	#
	## if we get another sprite sheet thats a lot better for characters, uncomment this line
	#animation_to_play = face_direction + "_" + ("walk" if movement.length() > 0.0 else "idle")
	#animation_player.play(animation_to_play)
	
