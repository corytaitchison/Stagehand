import numpy as np

class Spring:
	def __init__(self, x, v = np.array([0., 0.]), k = 1, gamma = 1, t_step = 1e-1):
		self.x, self.v, self.k, self.gamma, self.t_step = x, v, k, gamma, t_step
		self.orig = x

	def set_spring(self, orig):
		self.orig = orig

	def get_x(self):
		return np.int64(np.round(self.x))

	def dist(self, x1, x2):
		return np.sqrt(sum((x1 - x2)**2))

	def get_acc(self):
		a = -1 * self.k * (self.x - self.orig) - self.gamma * self.v
		return a

	def update(self):
		a = self.get_acc()
		self.x += self.v * self.t_step + 0.5 * a * self.t_step ** 2
		self.v += a * self.t_step

def main():
	global s
	s = Spring(np.array([0., 0.]))
	s.set_spring(np.array([1., 0.]))
	s.get_acc()
	s.update()
	print(s.x, s.v)

if __name__ == '__main__':
	main()
