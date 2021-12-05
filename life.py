import pygame, copy, time, random
def cut(color):
	color=int(color)
	if color>255:
		color=255
	elif color<0:
		color=0
	return color
def loop(x, y):
		xmax=life.x
		ymax=life.y
		if x>=xmax:
			x=x-xmax
		elif x<0:
			x=x+xmax
		if y>=ymax:
			y=y-ymax
		elif y<0:
			y=y+ymax
		return x, y
class cell():
	alive=False
	food=False
	food_energy=0
	genome=None
	active_gene=0
	energy=None
	x, y=None, None
	genes_registered=[25, 7, 9, 10]
	def tick(self, screen):
		rules=self.rules
		if self.alive:
			if random.randint(0, rules.telomeres_resistance)==0:
				self.alive=False
				self.food=True
				return
			if self.active_gene>=len(self.genome):
				self.active_gene=0
			self.energy-=rules.energy.entropy
			self.food_energy+=rules.energy.entropy*rules.food.from_energy_multiplier
			gene=self.genome[self.active_gene]
			if gene==25:
				self.energy+=rules.energy.actions.photosynteses
			elif gene==9:
				dx=random.randint(-1, 1)
				dy=random.randint(-1, 1)
				if dy==0 and dx==0:
					dy-=1
				ax, ay=loop(self.x+dx, self.y+dy)
				pretendor_cell=life.game_grid[ay][ax]
				if pretendor_cell.food:
					pretendor_cell.food=False
					self.energy+=pretendor_cell.food_energy
					pretendor_cell.food_energy=0	
			elif gene==7:
				if self.energy>=rules.energy.max//2:
					dx=random.randint(-1, 1)
					dy=random.randint(-1, 1)
					if dy==0 and dx==0:
						dy+=1
					ax, ay=loop(self.x+dx, self.y+dy)
					pretendor_cell=life.game_grid[ay][ax]
					if not (pretendor_cell.alive or pretendor_cell.food):
						self.energy=self.energy/2
						life.game_grid[ay][ax]=copy.deepcopy(self)
						life.game_grid[ay][ax].x=ax
						life.game_grid[ay][ax].y=ay
						life.game_grid[ay][ax].active_gene=0
						life.game_grid[ay][ax].genome=self.mutate(copy.deepcopy(self.genome))
			elif gene==10:
				positions=[
				(-1, -1),
				(-1, 0),
				(-1, 1),
				(0, -1),
				(0, 1),
				(1, -1),
				(1, 0),
				(1, 1)
				]
				for pos in positions:
					dx, dy=pos
					ax, ay=loop(self.x+dx, self.y+dy)
					pretendor_cell=life.game_grid[ay][ax]
					if pretendor_cell.alive:
						if self.get_genomes_diff(self.genome, pretendor_cell.genome)>rules.specie_member_difference:
							pretendor_cell.energy-=rules.fight.damage
			self.active_gene+=1
			if self.energy<=0:
				self.alive=False
				self.food=True
			c=cut(self.energy*255/rules.energy.max)
			pygame.draw.rect(screen, (cut(255-c), c, 0), (self.x*life.size, self.y*life.size, life.size, life.size))
		elif self.food:
			if self.food_energy<=0:
				self.food=False
			self.food_energy-=rules.food.decay
			pygame.draw.rect(screen, (80, 80, 120), (self.x*life.size, self.y*life.size, life.size, life.size))
	def mutate(self, genome):
		if random.randint(0, self.rules.mutation.defence)==0:
			if random.randint(0, 5)==0:
				adress=random.randint(0, len(genome)-1)
				genome[adress]=random.choice(self.genes_registered)
			elif random.randint(0, 1)==0:
				genome.append(0)
			elif len(genome)>1:
				genome.pop(random.randint(0, len(genome)-1))
		return genome
	def get_genomes_diff(self, genome1, genome2):
		diff=0
		while len(genome1)>len(genome2):
			genome1.pop(len(genome1)-1)
			diff+=1
		while len(genome1)<len(genome2):
			genome2.pop(len(genome2)-1)
			diff+=1
		for i in range(len(genome1)):
			g1=genome1[i]
			g2=genome2[i]
			if g1!=g2:
				diff+=1
		return diff
	class rules():
		specie_member_difference=1
		telomeres_resistance=500
		class energy():
			entropy=2
			max=100
			class actions():
				multiplier=1
				photosynteses=3
				consume_food=-1
		class food():
			decay=1
			from_energy_multiplier=0.95
		class mutation():
			defence=10
		class fight():
			damage=50
class app():
	size=None
	x, y=None, None
	game_grid=None
	def create_grid(self, starting_cell):
		cells=[]
		for y in range(self.y):
			xcells=[]
			for x in range(self.x):
				cell0=cell
				cell0.x=x
				cell0.y=y
				cell0=cell0()
				xcells.append(cell0)
			cells.append(xcells)
		starting_cell.x=self.x//2
		starting_cell.y=0
		cells[0][self.x//2]=starting_cell
		return cells
	def run(self):
		screen=self.display(100, 200, 10)
		starting_cell=cell()
		starting_cell.alive=True
		starting_cell.genome=[25, 25, 25, 25, 25, 25, 25, 25, 7]
		starting_cell.energy=starting_cell.rules.energy.max
		self.game_grid=self.create_grid(starting_cell)
		while True:
			#time.sleep(0.1)
			screen.fill((0, 0, 0))
			for array_part in self.game_grid:
				for ccell in array_part:
					ccell.tick(screen)
			pygame.display.update()
	def display(self, x, y, size):
		sc=pygame.display.set_mode((x, y))
		self.x, self.y=x, y
		self.size=size
		return sc

life=app()
life.run()
