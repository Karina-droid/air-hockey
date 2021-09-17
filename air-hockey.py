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
		self.ball_speed = 30
		self.angle = random.uniform(0, 2*math.pi)
		super().__init__('pzl:BallGray', parent=parent, *args, **kwargs)



class Game(Scene):
	def setup(self):
		self.background_color = '#ffffff'
		board_shape = ui.Path.rounded_rect(0, 0, 
																		sw-padding+10, 
																		sh-padding, 									padding/2)
		board_shape.line_width = 4
		self.board = ShapeNode(board_shape, 
													 position=(sw/2, sh/2), 
													 stroke_color='#723d04', fill_color='#d5d5cd',
													 z_position=-1, parent=self)
		
		top_wall = (0, sh/2, sw, 35)
		left_wall = (-sw/2, 0, sh, 35)
		right_wall = (sw/2, 0, sh, 35)
		bottom_wall = (0, -sh/2, sw, 35)
		rects = [top_wall, right_wall, bottom_wall, left_wall]
		walls = [SpriteNode(position=(rects[i][0], 	rects[i][1]), 
								 size=(rects[i][2], rects[i][3]),
								 alpha=0, parent=self.board) for i in range(len(rects))]
								 
		walls[1].rotation, walls[3].rotation = math.pi/2, math.pi/2
							   
		self.blue_player = SpriteNode('pzl:PaddleBlue', position=(0, sh/2.7), parent=self.board)
		
		self.red_player = SpriteNode('pzl:PaddleRed', position=(0, -sh/2.7), parent=self.board)
		
		self.right_touch, self.left_touch = (0, 0), (0, 0)
		self.obstacles = walls + [self.red_player, self.blue_player]
		
		xb, yb = -sw/2 + padding*1.6, sh/2 - padding*1.6
		xr, yr = -sw/2 + padding*1.6, -sh/2 + padding*1.6
		
		while xb < sw/2:
			blue_spikes = SpriteNode(
					'plf:Tile_Spikes', position=(xb, yb), 
					color='black', 
					parent=self.board)
			blue_spikes.rotation = math.pi
			xb += blue_spikes.size.w
			
		while xr < sw/2:
			r_spikes = SpriteNode('plf:Tile_Spikes',
					position=(xr, yr), color='black', 
					parent=self.board)
			xr += r_spikes.size.w
		
		self.spawn_ball()


	def update(self):
		dx, dy = self.ball.v 
		self.ball.position += (dx*2.5, dy*2.5) 
		self.check_collisions()


	def touch_began(self, touch):
		touch_loc = self.board.point_from_scene(touch.location)
		if touch_loc in self.blue_player.frame:
			self.left_touch = touch.touch_id
		elif touch_loc in self.red_player.frame:
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
		delta_x = user_touch.location.x - user_touch.prev_location.x
		if touch_id in self.left_touch:
			paddle = self.blue_player
		elif touch_id in self.right_touch:
			paddle = self.red_player

		if paddle:  
			x, y = paddle.position
			if delta_x > 0:
				paddle.position = min(x + delta_x, sw/2 - 69), y
			elif delta_x < 0:
				paddle.position = max(x + delta_x, -sw/2 + 69), y


	def spawn_ball(self):
		self.ball = Ball(position=(0, 0), 							parent=self.board)
		self.ball.v = (math.cos(self.ball.angle), 												 math.sin(self.ball.angle))
		
		
	def check_collisions(self):
		for obs in self.obstacles:
			if self.ball.frame.intersects(obs.frame):
				
				if obs == self.red_player:
					self.paddle_collision(self.red_player)
				elif obs == self.blue_player:
					self.paddle_collision(self.blue_player)
					
				vx, vy = self.ball.v
				if obs.rotation == math.pi/2:
					self.ball.v = (-1*vx, vy)
				elif obs.rotation == 0:
					self.ball.v = (vx, -1*vy)
					
					
	def paddle_collision(self, paddle):
		cos = (self.ball.position.x - paddle.position.x)/					 (paddle.size[0]*0.75)
		sin = math.sin(math.acos(cos))
		if self.ball.position.y >= 0:
			self.ball.v = (cos, sin)
		else:
			self.ball.v = (cos, -sin)
		
					
					
					
run(Game())
