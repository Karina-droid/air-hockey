from scene import *
import math
import random


sw, sh = get_screen_size()[0], get_screen_size()[1]
padding = 30


class Ball(SpriteNode):
	def __init__(self, r=11, v=(1, 1), parent=None, *args, **kwargs):
		self.size = (r*2, r*2)
		self.v = Vector2(*v)
		self.r = r
		self.ball_speed = 10
		self.angle = random.uniform(0, 2*math.pi)
		super().__init__('pzl:BallGray', color='purple', parent=parent, *args, **kwargs)



class Game(Scene):
	def setup(self):
		
		self.background_color = 'black'
		board_shape = ui.Path.rounded_rect(0, 0, sw-padding, sh-padding, 15)
		board_shape.line_width = 4
		self.board = ShapeNode(board_shape, position=(sw/2, sh/2), 
							   stroke_color='#723d04', fill_color='#acacac',
							   z_position=-1, parent=self)
		
		top_wall = (0, sh/2, sw, 35)
		left_wall = (-sw/2, 0, sh, 35)
		right_wall = (sw/2, 0, sh, 35)
		bottom_wall = (0, -sh/2, sw, 35)
		rects = [top_wall, right_wall, bottom_wall, left_wall]
		walls = [SpriteNode(position=(rects[i][0], rects[i][1]), 
								 size=(rects[i][2], rects[i][3]),
								 alpha=0, parent=self.board) for i in range(len(rects))]
								 
		walls[1].rotation, walls[3].rotation = math.pi/2, math.pi/2
							   
		self.left_player = SpriteNode('pzl:PaddleBlue', position=(-420, 0), parent=self.board)
		self.left_player.rotation = math.pi/2
		
		self.right_player = SpriteNode('pzl:PaddleRed', position=(420, 0), parent=self.board)
		self.right_player.rotation = math.pi/2
		
		self.right_touch, self.left_touch = (0, 0), (0, 0)
		self.obstacles = walls + [self.right_player, self.left_player]
		
		self.spawn_ball()


	def update(self):
		dx, dy = self.ball.v 
		self.ball.position += (dx*2.5, dy*2.5) 
		self.check_collisions()


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
			paddle = self.left_player
		elif touch_id in self.right_touch:
			paddle = self.right_player

		if paddle:  
			x, y = paddle.position
			if delta_y > 0:
				paddle.position = x, min(y + delta_y, sh/2 - 70)
			elif delta_y < 0:
				paddle.position = x, max(y + delta_y, -sh/2 + 70)


	def spawn_ball(self):
		self.ball = Ball(position=(0, 0), parent=self.board)
		self.ball.v = (math.cos(self.ball.angle), math.sin(self.ball.angle))
		
		
	def check_collisions(self):
		for obs in self.obstacles:
			if self.ball.frame.intersects(obs.frame):
				vx, vy = self.ball.v
				if obs.rotation == math.pi/2:
					self.ball.v = (-1*vx, vy)
				elif obs.rotation == 0:
					self.ball.v = (vx, -1*vy)
					
					
					
					
run(Game())
