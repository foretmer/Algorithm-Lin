class Box:
  def __init__(self, l, w, h) -> None:
    self.l, self.w, self.h = l, w, h
    self.real_l, self.real_w, self.real_h = l, w, h
    self.x, self.y, self.z = l, w, h
    self.state = 0
    self.states = [
      (l, w, h), (l, h, w), 
      (w, l, h), (w, h, l),
      (h, l, w), (h, w, l)
    ]

  def revolve(self):
    self.state = (self.state + 1) % 6
    (self.l, self.w, self.h) = self.states[self.state]
    (self.x, self.y, self.z) = self.states[self.state]
    return self.state