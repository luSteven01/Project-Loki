extends Area2D

@export_file("*.tscn") var target_scene_path: String
@export var target_position: Vector2
@export var is_interactive: bool = false

var player_inside := false
var cooldown := true

func _ready():
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	print("portal ready: monitoring:", monitoring)

	# cooldown so the player doesn't instantly trigger portals when scene loads
	await get_tree().create_timer(0.5).timeout
	cooldown = false
	print("Portal Cooldown Finished - Ready to Teleport")


func _on_body_entered(body):
	if body.is_in_group("Player"):
		player_inside = true
		if not is_interactive:
			try_teleport()


func _on_body_exited(body):
	if body.is_in_group("Player"):
		player_inside = false


func try_teleport():
	if cooldown:
		return
	if not player_inside:
		return
	if target_scene_path == "":
		print("Error: No target scene path set for this portal")
		return

	cooldown = true  # prevent re-triggering while switching
	SceneManager.switch_scene(load(target_scene_path), target_position)


func _process(delta):
	if is_interactive and player_inside and Input.is_action_just_pressed("interact"):
		try_teleport()
