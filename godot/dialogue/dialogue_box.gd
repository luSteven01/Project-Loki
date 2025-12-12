extends Panel
signal game_over

@onready var dialogue_text = $DialogueText
@onready var npc_icons = $NPCIcons
@onready var current_icon = null
@onready var talk_input = $PlayerTextInput
@onready var submit_button = $SubmitButton
@onready var leave_button = $LeaveButton
@onready var anim_player = $PlayerPortrait/AnimationPlayer
@onready var character_buttons_container = $CharacterButtons # To be removed
@onready var arrest_button = $ArrestButton
@onready var warning_popup = $WarningMessage

var current_character = null
var chat_history = []
var is_typing = false
var endgame_scripts = {}
var is_win = false
var game_manager = null
var dialogue_box = null
var keyboard_lock = false


func _ready() -> void:
	print("DialogueBox _ready() called")
	print("dialogue_text: ", dialogue_text)
	print("npc_icons: ", npc_icons)
	print("talk_input: ", talk_input)
	print("submit_button: ", submit_button)
	print("leave_button: ", leave_button)
	print("arrest_button: ", arrest_button)
	print("character_buttons_container: ", character_buttons_container)
	
	# $BGM.play()
	endgame_scripts = load_json("res://data/endgame_scripts.json")

	# Hide all NPC icons
	for icon in npc_icons.get_children():
		icon.visible = false

	# Initialize UI state
	# arrest_button.disabled = true
	# submit_button.disabled = true
	# talk_input.editable = false
	# warning_popup.hide()
	disable_interaction()
	leave_button.disabled = false
	talk_input.wrap_mode = TextEdit.LINE_WRAPPING_BOUNDARY
	dialogue_text.text = "Connecting to investigation database..."
	print("Initial text set")

	# Find GameManager node
	game_manager = get_node_or_null("/root/Main/GameManager")
	print("GameManager found: ", game_manager)

	if not game_manager:
		dialogue_text.text = "Error: GameManager not found!"
		print("ERROR: Cannot find GameManager node at /root/Main/GameManager")
		return
	

# Handle input with Ctrl+Enter
func _input(event):
	# Allow mouse wheel scrolling
	if event is InputEventMouse:
		return

	if keyboard_lock:
		get_viewport().set_input_as_handled()
		return
		
	if event is InputEventKey and event.pressed:
		# Shift + Enter → newline
		if (event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER) and event.shift_pressed:
			talk_input.insert_text_at_caret("\n")
			get_viewport().set_input_as_handled()

		# Enter → submit
		elif (event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER) and not event.shift_pressed:
			_on_submit_button_pressed()
			get_viewport().set_input_as_handled()

		elif event.is_action_pressed("escape"):
			_on_leave_button_pressed()
			get_viewport().set_input_as_handled()


func _on_character_selected(character):
	is_typing = false
	stop_npc_talk()
	stop_player_talk()
	current_character = character
	game_manager.call("select_character", character)
	chat_history.clear()

	# Hide all NPC icons
	for icon in npc_icons.get_children():
		icon.visible = false

	# Find icon node (by ID)
	current_icon = npc_icons.get_node_or_null(character.id.capitalize())

	if current_icon:
		current_icon.visible = true
	else:
		print("⚠️ No NPC icon found for:", character.id)

	# Initialize dialogue and show welcome message
	dialogue_text.text = "Now interviewing: " + character.avatar + " " + character.name + "\n"
	dialogue_text.text += character.description + "\n\n"

	# Enable input
	enable_interaction()
	talk_input.grab_focus()

func _on_submit_button_pressed() -> void:
	send_player_message()

func send_player_message():
	var player_message = talk_input.text.strip_edges()
	if player_message.is_empty() or not current_character:
		return
		
	start_player_talk()

	# Send message to server
	game_manager.call("send_message", player_message, _on_message_received)

	# Disable input
	disable_interaction()
	keyboard_lock = true
	
	# Show player's message in dialogue window
	dialogue_text.text += "\n\n[right][b]Me:[/b]"
	await type_text_slowly(player_message + "\n")
	dialogue_text.text += "[/right]"

	stop_player_talk()

	# Clear the input for the next line
	talk_input.text = ""

func _on_message_received(response: String, error):
	while is_typing:
		await get_tree().create_timer(0.5).timeout

	# Remove loading message
	var lines = dialogue_text.text.split("\n")
	if lines.size() > 0 and "thinking" in lines[-1]:
		lines.remove_at(lines.size() - 1)
		dialogue_text.text = "\n".join(lines)

	if error:
		add_message_to_display("System", "Error: " + error)
	else:
		await get_tree().create_timer(0.6).timeout
		add_message_to_display(current_character.name, response)


# Display NPC message with typewriter effect
func add_message_to_display(sender: String, message: String):
	disable_interaction()
	keyboard_lock = true
	dialogue_text.text += "\n[b]" + sender + ":[/b]"
	start_npc_talk()
	await type_text_slowly(message)
	stop_npc_talk()
	enable_interaction()
	keyboard_lock = false
	talk_input.grab_focus()


func _on_leave_button_pressed() -> void:
	dialogue_text.text = "Investigation session ended."		
	# disable_interaction()
	current_character = null
	$BGM.stop()

	if game_manager:
		game_manager.exit_dialogue()

	get_node(".").visible = false


# Typewriter effect for NPC messages (clean version)
func type_text_slowly(full_text: String, speed := 0.03) -> void:
	is_typing = true

	# Add the NPC name once, no repetition
	dialogue_text.text += "\n"
	
	# Type each character sequentially
	for ch in full_text:
		if not is_typing:
			return
		dialogue_text.text += ch
		dialogue_text.scroll_to_line(dialogue_text.get_line_count() - 1)
		await get_tree().create_timer(speed).timeout

	is_typing = false

# Expand text field for multiple rows
func _process(_delta: float) -> void:
	var line_height = talk_input.get_line_height()
	var line_count = talk_input.get_total_visible_line_count()
	var min_lines = 1
	var max_lines = 5  # limit so it doesn’t get huge

	var new_height = clamp(line_height * (line_count + 0.5), line_height * min_lines, line_height * max_lines)
	talk_input.custom_minimum_size.y = new_height

# Play npc portrait animation
func start_npc_talk(action: String = "talk"):
	if not current_icon:
		return
	
	var anim_npc_player = current_icon.get_node_or_null("AnimationPlayer")
	if not anim_npc_player:
		return
	anim_npc_player.play(action)

# Stop npc portrait animation
func stop_npc_talk():
	if not current_icon:
		return
	
	var anim_npc_player = current_icon.get_node_or_null("AnimationPlayer")
	if not anim_npc_player:
		return
	anim_npc_player.stop()

# Play player portrait animation
func start_player_talk():
	anim_player.play("player_talk")

# Stop player portrait animation
func stop_player_talk():
	anim_player.stop()


func _on_arrest_button_pressed() -> void:
	if not current_character:
		return
	
	# Play arrest sound
	$ArrestSound.play()
	# disable_interaction()
	# 	arrest_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	# submit_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	talk_input.editable = false
	submit_button.disabled = true
	leave_button.disabled = true
	# arrest_button.disabled = true
	keyboard_lock = true

	# Show endgame script based on arrested character
	var char_id = current_character["npc_id"]
	var script = endgame_scripts.get(char_id, "No ending found.")
	var time = 2.0 + script.length() * 0.03

	# Special case: if Abel is arrested, stop BGM and play endgame music
	if char_id == "abel" and Global.inventory["shirt"]["collected"] and Global.inventory["button"]["collected"]:
		is_win = true
		$BGM.stop()
		$Endgame.play()
		script = endgame_scripts.get("winner", "No script found.")		

	start_npc_talk("endgame")
	dialogue_text.text += "\n\n[b]" + current_character["npc_id"].capitalize() + ":[/b]"
	await type_text_slowly(script)
	stop_npc_talk()

	# WAIT 3 SECONDS BEFORE CONTINUING
	await get_tree().create_timer(3).timeout

	if is_win:
		# Abel arrested - WIN
		dialogue_text.text = "\n\n[center][b]You have successfully arrested the culprit! Congratulations, Detective![/b]\n\n"
		script = load_credits()
		await type_text_slowly(script)
		dialogue_text.text += "[/center]"
		time = min(script.length() * 0.03, 6.0)
	else:
		# Others arrested - LOSE
		dialogue_text.text = "\n\n[center][b]You have arrested the wrong person. The real culprit remains at large... Game Over.[/b][/center]"		
		# await get_tree().create_timer(time).timeout
		
	# Leave chat dialogue and triggers endgame sequence
	current_character = null
	await get_tree().create_timer(time).timeout
	
	# Unlock interaction
	arrest_button.disabled = true
	enable_interaction()
	keyboard_lock = false
	self.visible = false
	$BGM.stop()
	game_over.emit()


func _on_arrest_button_mouse_entered() -> void:
	if arrest_button.disabled:
		return
	# Hover = bright cold silver (blue-shifted & higher contrast)
	arrest_button.modulate = Color(1.55, 1.55, 1.7, 1.0)
	warning_popup.show()


func _on_arrest_button_mouse_exited() -> void:
	if arrest_button.disabled:
		return	
	# Normal color
	arrest_button.modulate = Color(1.0, 1.0, 1.0, 1.0)
	warning_popup.hide()

# Lock all input interaction
func disable_interaction() -> void:
	arrest_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	submit_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	talk_input.editable = false
	submit_button.disabled = true
	leave_button.disabled = true
	arrest_button.disabled = true
	warning_popup.hide()

# Unlock all input interaction
func enable_interaction():
	arrest_button.mouse_filter = Control.MOUSE_FILTER_STOP
	submit_button.mouse_filter = Control.MOUSE_FILTER_STOP
	talk_input.editable = true
	submit_button.disabled = false
	leave_button.disabled = false
	arrest_button.disabled = false


func load_json(path) -> Dictionary:
	var file = FileAccess.open(path, FileAccess.READ)
	return JSON.parse_string(file.get_as_text())

func load_credits():
	return FileAccess.get_file_as_string("res://data/credits.txt")

func start_dialogue_bgm():
	$Endgame.stop()
	$BGM.play()


func reset():
	# Reset internal state
	current_character = null
	current_icon = null
	chat_history.clear()
	is_typing = false
	is_win = false
	keyboard_lock = false

	# Reset UI
	dialogue_text.text = "Connecting to investigation database..."
	talk_input.text = ""
	talk_input.editable = false
	submit_button.disabled = true
	leave_button.disabled = false  # matches your initial _ready()
	
	# Reset Arrest button
	arrest_button.disabled = true
	arrest_button.modulate = Color(1, 1, 1, 1)
	warning_popup.hide()

	# Hide NPC icons
	for icon in npc_icons.get_children():
		icon.visible = false

	# Stop animations
	stop_npc_talk()
	stop_player_talk()

	# Stop audio
	$BGM.stop()
	$Endgame.stop()

	# Hide the dialogue box itself
	self.visible = false
