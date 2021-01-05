from scene import *
import math
import random


sw, sh = get_screen_size()[0], get_screen_size()[1]
bottom = -sh/2 + 30
top = sh/2 - 30
left = -sw/2 + 30
right = sw/2 - 30



class Ball(SpriteNode):
	def __init__(self, position=(sw/2, sh/2), texture=None, 
				 r=11, v=(1, 1), parent=None, 
				 *args, **kwargs):
		
		self.size = (r*2, r*2)
		self.v = Vector2(*v)
		self.r = r
		self.ball_speed = 10
		self.angle = random.uniform(0, 2*math.pi)
		
		SpriteNode('pzl:BallGray', position,
					color='purple', parent=parent, 
					*args, **kwargs)



class Game(Scene):
	def setup(self):
		bottom_wall = Rect(left, bottom, sw-30, 0)
		top_wall = Rect(left, top, sw-30, 0)
		left_wall = Rect(left, top, 0, sh-30)
		right_wall = Rect(right, top, 0, sh-30)
		self.walls = [bottom_wall, top_wall, left_wall, right_wall]
		
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
		
		self.spawn_ball()
		
		
	def update(self):
		self.rush_ball()
		print(self.ball.position, self.ball.v)
		
		
	def touch_began(self, touch):
		touch_loc = self.board.point_from_scene(touch.location)
		if touch_loc in self.left_player.frame:
			self.left_touch = touch.touch_id
		elif touch_loc in self.right_player.frame:
			self.right_touch = touch.touch_id
		
		
	def touch_moved(self, touch):
		if self.right_touch != (0, 0) or self.left_touch != (0, 0):
			self.move_paddle(touch)
				
	
	def touch_ended(self, touch):
		touch_id = touch.touch_id
		if touch_id == self.right_touch:
			self.right_touch = (0, 0)
		elif touch_id == self.left_touch:
			self.left_touch = (0, 0)
			
			
	def move_paddle(self, user_touch):
		paddle = None
		touch_id = user_touch.touch_id
		delta_y = user_touch.location.y - user_touch.prev_location.y
		if touch_id in self.left_touch:
			paddle= self.left_player
		elif touch_id in self.right_touch:
			paddle = self.right_player
			
		if paddle:	
			x, y = paddle.position
			if delta_y > 0:
				paddle.position = x, min(y + delta_y, sh/2 - 70)
			elif delta_y < 0:
				paddle.position = x, max(y + delta_y, -sh/2 + 70)
				
				
	def spawn_ball(self):
		self.ball = Ball(parent=self)
		self.ball.v = (math.cos(self.ball.angle), math.sin(self.ball.angle))
		
		
	def rush_ball(self):
		dx = self.ball.v[0]
		dy = self.ball.v[1]
		self.ball.run_action(Action.move_by(dx, dy, 1))
						
	
	
run(Game())
