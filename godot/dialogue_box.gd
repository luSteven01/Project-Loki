extends Panel

@onready var game_manager = get_node("/root/Main/GameManager")
@onready var dialogue_text = $DialogueText
@onready var talk_input = $PlayerTextInput
@onready var submit_button = $SubmitButton
@onready var leave_button = $LeaveButton
@onready var anim_npc_player = $NPCPortrait/AnimationPlayer
@onready var anim_player = $PlayerPortrait/AnimationPlayer

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Connect the TextEdit’s gui_input so Enter can be intercepted
	talk_input.connect("gui_input", Callable(self, "_on_text_input_gui_input"))
	talk_input.grab_focus()

func initialize_with_npc (npc):
	#NPC Icon
	dialogue_text.text = ""
	submit_button.disabled = true


func _on_submit_button_pressed() -> void:
	var player_message = talk_input.text.strip_edges()
	if player_message != "":
		
		start_player_talk()
		
		# Show player's message in dialogue window
		dialogue_text.text += "\n[right][b][Player]:[/b]"
		await type_text_slowly(player_message + "\n")
		dialogue_text.text += "[/right]"
		
		stop_player_talk()

		# Send player's message to GameManager → ChatGPT
		game_manager.dialogue_request(player_message)

		# Clear the input for the next line
		talk_input.text = ""

# Typewriter effect for NPC messages (clean version)
func type_text_slowly(full_text: String, speed := 0.03) -> void:
	# Add the NPC name once, no repetition
	dialogue_text.text += "\n"
	
	# Type each character sequentially
	for ch in full_text:
		dialogue_text.text += ch
		dialogue_text.scroll_to_line(dialogue_text.get_line_count() - 1)
		await get_tree().create_timer(speed).timeout


func _on_leave_button_pressed() -> void:
	hide() # Replace with function to return to game screen

# Play npc portrait animation
func start_npc_talk():
	anim_npc_player.play("talk")

# Stop npc portrait animation
func stop_npc_talk():
	anim_npc_player.stop()

# Play player portrait animation
func start_player_talk():
	anim_player.play("player_talk")

# Stop player portrait animation
func stop_player_talk():
	anim_player.stop()

# Reverse Enter and Shift + Enter function for fast typing
func _on_text_input_gui_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		# Shift + Enter → newline
		if event.keycode == KEY_ENTER and event.shift_pressed:
			talk_input.insert_text_at_caret("\n")
			get_viewport().set_input_as_handled()

		# Enter → submit
		elif event.keycode == KEY_ENTER and not event.shift_pressed:
			_on_submit_button_pressed()
			get_viewport().set_input_as_handled()

# Expand text field for multiple rows
func _process(_delta: float) -> void:
	var line_height = talk_input.get_line_height()
	var line_count = talk_input.get_line_count()
	var min_lines = 1
	var max_lines = 5  # limit so it doesn’t get huge

	var new_height = clamp(line_height * (line_count + 0.5), line_height * min_lines, line_height * max_lines)
	talk_input.custom_minimum_size.y = new_height
