import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class GestureViewer:

    def __init__(self):

        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection="3d")

        plt.ion()
        plt.show(block=False)


    def show(self, csv_file):

        df = pd.read_csv(csv_file)

        left = df[["LeftPosX", "LeftPosY", "LeftPosZ"]].to_numpy()
        right = df[["RightPosX", "RightPosY", "RightPosZ"]].to_numpy()

        n = len(df)
        self.ax.clear()

        # LEFT CONTROLLER
        colors = plt.cm.Blues(np.linspace(0.2, 1.0, n - 1))
        for i in range(n - 1):

            self.ax.plot(left[i:i+2, 0], left[i:i+2, 1], left[i:i+2, 2],
                color=colors[i], linewidth=3
            )

        # RIGHT CONTROLLER
        colors = plt.cm.Oranges(np.linspace(0.2, 1.0, n - 1))

        for i in range(n - 1):

            self.ax.plot(right[i:i+2, 0], right[i:i+2, 1], right[i:i+2, 2],
                color=colors[i], linewidth=3
            )

        # START / END
        self.ax.scatter(left[0,0], left[0,1], left[0,2], color="green",
            s=80, label="Left Start"
        )

        self.ax.scatter(left[-1,0], left[-1,1], left[-1,2], color="red",
            s=80, label="Left End"
        )

        self.ax.scatter(right[0,0], right[0,1], right[0,2], color="lime",
            s=80, label="Right Start"
        )

        self.ax.scatter(right[-1,0], right[-1,1], right[-1,2], color="darkred",
            s=80, label="Right End"
        )

        # SAME SCALE
        points = np.vstack((left, right))

        mins = points.min(axis=0)
        maxs = points.max(axis=0)

        center = (mins + maxs) / 2
        radius = (maxs - mins).max() / 2

        self.ax.set_xlim(center[0]-radius, center[0]+radius)
        self.ax.set_ylim(center[1]-radius, center[1]+radius)
        self.ax.set_zlim(center[2]-radius, center[2]+radius)

        # LABELS
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        #self.ax.set_title(csv_file)

        self.ax.legend()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()