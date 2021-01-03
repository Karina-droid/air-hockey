from scene import *
import math


sw, sh = get_screen_size()[0], get_screen_size()[1]

class Game(Scene):
	def setup(self):
		self.background_color = 'black'
		board_shape = ui.Path.rounded_rect(0, 0, sw-30, sh-30, 15)
		board_shape.line_width = 4
		self.board = ShapeNode(board_shape, position=(sw/2, sh/2), 
						  stroke_color='#723d04', fill_color='#acacac',
						  parent=self)
						  
		self.left_player = SpriteNode('pzl:PaddleBlue', position=(-420, 0),
									  parent=self.board)
		self.left_player.rotation = math.pi/2
		
		self.right_player = SpriteNode('pzl:PaddleRed', position=(420, 0),
									   parent=self.board)
		self.right_player.rotation = math.pi/2
		
		self.right_touch, self.left_touch = (0, 0), (0, 0)
		
		
	def touch_began(self, touch):
		touch_loc = self.board.point_from_scene(touch.location)
		if touch_loc in self.left_player.frame:
			self.left_touch = touch.touch_id
		elif touch_loc in self.right_player.frame:
			self.right_touch = touch.touch_id
		
		
	def touch_moved(self, touch):
		if self.right_touch != (0, 0) or self.left_touch != (0, 0):
			self.move_skateboard(touch)
				
	
	def touch_ended(self, touch):
		touch_id = touch.touch_id
		if touch_id == self.right_touch:
			self.right_touch = (0, 0)
		elif touch_id == self.left_touch:
			self.left_touch = (0, 0)
			
			
	def move_skateboard(self, user_touch):
		skateboard = None
		touch_id = user_touch.touch_id
		delta_y = user_touch.location.y - user_touch.prev_location.y
		if touch_id in self.left_touch:
			skateboard = self.left_player
		elif touch_id in self.right_touch:
			skateboard = self.right_player
			
		if skateboard:	
			x, y = skateboard.position
			if delta_y > 0:
				skateboard.position = x, min(y + delta_y, sh/2 - 70)
			elif delta_y < 0:
				skateboard.position = x, max(y + delta_y, -sh/2 + 70)
			
	
run(Game())
