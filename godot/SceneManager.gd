extends Node

var player_start_position = Vector2(131.0, 220.0)

var transition_rect: ColorRect
var animation_player: AnimationPlayer

signal level_change_requested(new_scene_packed, target_position)

func _ready():
	var canvas = CanvasLayer.new()
	canvas.layer = 100
	
	transition_rect = ColorRect.new()
	transition_rect.name = "ColorRect"
	transition_rect.color = Color(0, 0, 0, 0) # Start fully transparent
	transition_rect.anchors_preset = Control.PRESET_FULL_RECT
	transition_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(transition_rect)
	
	animation_player = AnimationPlayer.new()
	canvas.add_child(animation_player)
	
	var library = AnimationLibrary.new()
	var fade_out = Animation.new()
	fade_out.length = 0.4
	# Track for the ColorRect's color property
	fade_out.add_track(Animation.TYPE_VALUE)
	fade_out.track_set_path(0, "ColorRect:color")
	# First frame is transparent
	fade_out.track_insert_key(0, 0.0, Color(0, 0, 0, 0))
	# Fade to black
	fade_out.track_insert_key(0, 0.4, Color(0, 0, 0, 1))
	
	var fade_in = Animation.new()
	fade_in.length = 0.4
	# Track for the ColorRect's color property
	fade_in.add_track(Animation.TYPE_VALUE)
	fade_in.track_set_path(0, "ColorRect:color")
	# First frame is black
	fade_in.track_insert_key(0, 0.0, Color(0, 0, 0, 1)) 
	# Fade back into the game
	fade_in.track_insert_key(0, 0.4, Color(0, 0, 0, 0))
	
	library.add_animation("fade_out", fade_out)
	library.add_animation("fade_in", fade_in)
	animation_player.add_animation_library("", library)
	get_tree().root.call_deferred("add_child", canvas)
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func switch_scene(scene_path: PackedScene, new_pos: Vector2):
	# Store the position for the player in the next scene
	player_start_position = new_pos
	
	# Fade to black
	#animation_player.play("fade_out")
	#await animation_player.animation_finished
	
	# Emit the signal to change the scene
	emit_signal("level_change_requested", scene_path, new_pos)
	
	## Fade back into the game
	#animation_player.play("fade_in")

	transition_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
