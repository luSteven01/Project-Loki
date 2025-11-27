extends Panel

# var game_manager = null

@onready var dialogue_text = $DialogueText
@onready var npc_icons = $NPCIcons
@onready var current_icon = null
@onready var talk_input = $PlayerTextInput
@onready var submit_button = $SubmitButton
@onready var leave_button = $LeaveButton
@onready var anim_player = $PlayerPortrait/AnimationPlayer
@onready var character_buttons_container = $CharacterButtons # To be removed
@onready var game_manager = get_node_or_null("/root/Main/GameManager")


# Option #1: have button that appears when player has a piece of evidence collected
# We can add more buttons that appear based on the # of evidence we have (I think we have 5?)
@onready var evidence_button = $EvidenceButton

# Option #2 for evidence-related mechanisms, where we just have a smaller version of the inventory on the side
# we can click on and click the "Show" option and show the button that way 
@onready var inventory_ui = $InventoryUI

var current_character = null
var chat_history = []

func _ready() -> void:	
	# Find GameManager node
	if not game_manager:
		dialogue_text.text = "Error: GameManager not found!"
		print("ERROR: Cannot find GameManager node at /root/Main/GameManager")
		return
				
	print("DialogueBox _ready() called")
	print("dialogue_text: ", dialogue_text)
	print("npc_icons: ", npc_icons)
	print("talk_input: ", talk_input)
	print("submit_button: ", submit_button)
	print("leave_button: ", leave_button)
	print("character_buttons_container: ", character_buttons_container)
	
	# Hide the evidence button(s) if we are doing my approach
	evidence_button.visible = false
		
	# Hide all NPC icons
	for icon in npc_icons.get_children():
		icon.visible = false
	
	# Initialize UI state
	submit_button.disabled = true
	talk_input.editable = false
	talk_input.wrap_mode = TextEdit.LINE_WRAPPING_BOUNDARY
	dialogue_text.text = "Connecting to investigation database..."
	print("Initial text set")
	
	# Wait for GameManager to load characters
	print("Waiting for GameManager to load characters...")
	await get_tree().create_timer(3.0).timeout
	
	if game_manager.has_method("get_characters"):
		var chars = game_manager.call("get_characters")
		print("Characters loaded: ", chars.size())
		if chars.size() > 0:
			setup_character_buttons()
			dialogue_text.text = "Select a character to interview"
			print("Character buttons created")
		else:
			dialogue_text.text = "Failed to connect to server. Please check if backend is running at http://127.0.0.1:8000"
			print("No characters loaded - server connection failed")
	else:
		dialogue_text.text = "Error: GameManager script not loaded correctly"
		print("ERROR: GameManager does not have get_characters method")
	
	# just testing if item exists when we use option #1
		
	#if(Global.item_exists("Berry")):
		#print("I have a berry")
		#evidence_button.visible = true;
		#for item in Global.inventory:
			#if item != null and item["name"] == "Berry":
				#evidence_button.text = "Button will be visible when player has the item; replace w/ question" + item["hashcode"]
	#else:
		#print("no berry")
		#evidence_button.visible = false;
	

# Handle input with Ctrl+Enter
func _input(event):
	if event is InputEventKey and event.pressed:
		# Shift + Enter → newline
		if (event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER) and event.shift_pressed:
			talk_input.insert_text_at_caret("\n")
			get_viewport().set_input_as_handled()

		# Enter → submit
		elif (event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER) and not event.shift_pressed:
			_on_submit_button_pressed()
			get_viewport().set_input_as_handled()
			
func get_player_reference():
	return Global.player_node

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
	submit_button.disabled = false
	talk_input.editable = true
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
	submit_button.disabled = true
	talk_input.editable = false
	
	# Show player's message in dialogue window
	dialogue_text.text += "\n[right][b][Player]:[/b]"
	await type_text_slowly(player_message + "\n")
	dialogue_text.text += "[/right]"

	stop_player_talk()

	# Clear the input for the next line
	talk_input.text = ""

func _on_message_received(response: String, error):
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

	# Re-enable input
	submit_button.disabled = false
	talk_input.editable = true
	talk_input.grab_focus()


func add_message_to_display(sender: String, message: String):
	dialogue_text.text += "\n[b]" + sender + ":[/b]"
	start_npc_talk()
	await type_text_slowly(message)
	stop_npc_talk()

func initialize_with_npc(npc):
	# Legacy function for backwards compatibility
	dialogue_text.text = ""
	submit_button.disabled = true

func _on_leave_button_pressed() -> void:
	dialogue_text.text = "Investigation session ended."
	submit_button.disabled = true
	talk_input.editable = false
	current_character = null
	inventory_ui.visible = false
	game_manager.exit_dialogue()

# Typewriter effect for NPC messages (clean version)
func type_text_slowly(full_text: String, speed := 0.03) -> void:
	# Add the NPC name once, no repetition
	dialogue_text.text += "\n"
	
	# Type each character sequentially
	for ch in full_text:
		dialogue_text.text += ch
		dialogue_text.scroll_to_line(dialogue_text.get_line_count() - 1)
		await get_tree().create_timer(speed).timeout

# Expand text field for multiple rows
func _process(_delta: float) -> void:
	var line_height = talk_input.get_line_height()
	var line_count = talk_input.get_total_visible_line_count()
	var min_lines = 1
	var max_lines = 5  # limit so it doesn’t get huge

	var new_height = clamp(line_height * (line_count + 0.5), line_height * min_lines, line_height * max_lines)
	talk_input.custom_minimum_size.y = new_height

# Play npc portrait animation
func start_npc_talk():
	if not current_icon:
		return
	
	var anim_npc_player = current_icon.get_node_or_null("AnimationPlayer")
	if not anim_npc_player:
		return
	anim_npc_player.play("talk")

# Stop npc portrait animation
func stop_npc_talk():
	if not current_icon:
		return
	
	var anim_npc_player = current_icon.get_node_or_null("AnimationPlayer")
	anim_npc_player.stop()

# Play player portrait animation
func start_player_talk():
	anim_player.play("player_talk")

# Stop player portrait animation
func stop_player_talk():
	anim_player.stop()