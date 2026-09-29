from pathlib import Path

from gesture_viewer import GestureViewer


CSV_FILE = Path(
    r"C:\Users\Gaspard\Master_thesis\prepared_dataset\Participant_09\Iced\Iced_01.csv"
)

viewer = GestureViewer()

viewer.show(CSV_FILE)

print("Displaying:", CSV_FILE)
print("Close the figure window to exit.")

import matplotlib.pyplot as plt
plt.ioff()
plt.savefig("gesture.pdf")