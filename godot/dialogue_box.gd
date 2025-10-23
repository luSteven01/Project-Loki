extends Panel

var game_manager = null

@onready var dialogue_text = $DialogueText
@onready var talk_input = $PlayerTextInput
@onready var submit_button = $SubmitButton
@onready var leave_button = $LeaveButton
@onready var character_buttons_container = $CharacterButtons

var current_character = null
var chat_history = []

func _ready() -> void:
	print("DialogueBox _ready() called")
	print("dialogue_text: ", dialogue_text)
	print("npc_icon: ", npc_icon)
	print("talk_input: ", talk_input)
	print("submit_button: ", submit_button)
	print("leave_button: ", leave_button)
	print("character_buttons_container: ", character_buttons_container)

	# Initialize UI state
	submit_button.disabled = true
	talk_input.editable = false
	dialogue_text.text = "Connecting to investigation database..."
	print("Initial text set")

	# Find GameManager node
	game_manager = get_node_or_null("/root/Main/GameManager")
	print("GameManager found: ", game_manager)

	if not game_manager:
		dialogue_text.text = "Error: GameManager not found!"
		print("ERROR: Cannot find GameManager node at /root/Main/GameManager")
		return

	# Wait for GameManager to load characters
	print("Waiting for GameManager to load characters...")
	await get_tree().create_timer(2.0).timeout

	if game_manager.has_method("get_characters"):
		var chars = game_manager.call("get_characters")
		print("Characters loaded: ", chars.size())
		if chars.size() > 0:
			setup_character_buttons()
			dialogue_text.text = "Select a character to interview"
			print("Character buttons created")
		else:
			dialogue_text.text = "Failed to connect to server. Please check if backend is running at http://localhost:8000"
			print("No characters loaded - server connection failed")
	else:
		dialogue_text.text = "Error: GameManager script not loaded correctly"
		print("ERROR: GameManager does not have get_characters method")

# Handle input with Ctrl+Enter
func _input(event):
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_ENTER and event.ctrl_pressed:
			send_player_message()

func setup_character_buttons():
	print("=== setup_character_buttons() called ===")
	if character_buttons_container:
		print("✓ character_buttons_container exists")
		print("  Position: ", character_buttons_container.position)
		print("  Size: ", character_buttons_container.size)
		print("  Visible: ", character_buttons_container.visible)

		# Clear existing buttons
		for child in character_buttons_container.get_children():
			child.queue_free()

		# Create character buttons
		var characters = game_manager.call("get_characters")
		print("✓ Creating buttons for ", characters.size(), " characters")

		for i in range(characters.size()):
			var character = characters[i]
			var button = Button.new()
			button.text = character.avatar + " " + character.name
			button.custom_minimum_size = Vector2(120, 40)
			button.pressed.connect(_on_character_selected.bind(character))
			character_buttons_container.add_child(button)
			print("  [", i, "] Created button: ", button.text, " | Size: ", button.size)

		print("✓ All buttons added to container")
		print("  Total children: ", character_buttons_container.get_child_count())
	else:
		print("✗ ERROR: character_buttons_container is null!")

func _on_character_selected(character):
	current_character = character
	game_manager.call("select_character", character)
	chat_history.clear()

	# Initialize dialogue and show welcome message
	dialogue_text.text = "Now interviewing: " + character.avatar + " " + character.name + "\n"
	dialogue_text.text += character.description + "\n\n"

	# Enable input
	submit_button.disabled = false
	talk_input.editable = true
	talk_input.grab_focus()

func _on_submit_button_pressed() -> void:
	send_player_message()

func send_player_message():
	var message = talk_input.text.strip_edges()

	if message.is_empty() or not current_character:
		return

	# Display user message
	add_message_to_display("You", message)

	# Clear and disable input
	talk_input.text = ""
	submit_button.disabled = true
	talk_input.editable = false

	# Show loading indicator
	dialogue_text.text += "\n" + current_character.name + " is thinking...\n"

	# Send message to server
	game_manager.call("send_message", message, _on_message_received)

func _on_message_received(response: String, error):
	# Remove loading message
	var lines = dialogue_text.text.split("\n")
	if lines.size() > 0 and "thinking" in lines[-1]:
		lines.remove_at(lines.size() - 1)
		dialogue_text.text = "\n".join(lines)

	if error:
		add_message_to_display("System", "Error: " + error)
	else:
		add_message_to_display(current_character.name, response)

	# Re-enable input
	submit_button.disabled = false
	talk_input.editable = true
	talk_input.grab_focus()

func add_message_to_display(sender: String, message: String):
	dialogue_text.text += "\n[" + sender + "]: " + message + "\n"

func initialize_with_npc(npc):
	# Legacy function for backwards compatibility
	dialogue_text.text = ""
	submit_button.disabled = true

func _on_leave_button_pressed() -> void:
	dialogue_text.text = "Investigation session ended."
	submit_button.disabled = true
	talk_input.editable = false
	current_character = null
