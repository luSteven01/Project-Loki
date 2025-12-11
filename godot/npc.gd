# abstract class for the NPCs

@abstract class_name NPC extends CharacterBody2D

@export var npc_id : String
@export var character_name : String
@export var speed : float
@export var loop_path : bool 
@export var path : Path2D 
@export var path_follow : PathFollow2D
@export var animation_player : AnimationPlayer
@export var description: String

@abstract func _ready()
