import matplotlib.pyplot as plt
from court import Court

court_nba = Court(court_type="nba", court_color="black", paint_color="firebrick", line_color="white")
court_nba.draw(figsize=(12, 6.5), )
plt.show()