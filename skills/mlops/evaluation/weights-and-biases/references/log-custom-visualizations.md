# Log custom visualizations
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y)
wandb.log({"custom_plot": wandb.Image(fig)})