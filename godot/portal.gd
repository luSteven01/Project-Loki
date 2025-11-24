extends Area2D

@export_file("*.tscn") var target_scene_path: String
@export var target_scene: PackedScene
@export var target_position: Vector2
@export var is_interactive: bool = false
var player_body: CharacterBody2D = null

# Called when the node enters the scene tree for the first time.
func _ready():
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	print("portal ready: monitoring:", monitoring)

func _on_body_entered(body):
	# We check if the body is in the "player" group.
	# (Make sure your player node is in the "player" group!)
	if body.is_in_group("player"):
		
		player_body = body
		if not is_interactive:
			teleport()


func _on_body_exited(body):
	if body == player_body:
		player_body = null

func teleport():
	
	if target_scene_path == "":
		print("Error: No target scene path set for this portal")
		return
		
	var scene_to_load = load(target_scene_path)
	SceneManager.switch_scene(scene_to_load, target_position)


func _process(delta):
	if player_body != null and is_interactive and Input.is_action_just_pressed("interact"):
		teleport()
	
