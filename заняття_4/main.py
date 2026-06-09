import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 11)
y = 5 * x + 10

plt.figure(figsize=(10, 6))

plt.plot(x, y, color='darkgreen', linestyle='-', linewidth=4, label='y = 5 * x + 10', marker='o', markersize=10)
plt.plot(x, y + 20, color='darkblue', linestyle='--', linewidth=4, label='y = 5 * x + 30', marker='s', markersize=10)
plt.plot(x, y + 40, color='red', linestyle='-.', linewidth=4, label='y = 5 * x + 50', marker='+', markersize=10)
plt.plot(x, y + 60, color='orange', linestyle=':', linewidth=4, label='y = 5 * x + 70', marker='^', markersize=10)

plt.title('Lines', fontsize=14, fontweight='bold')
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(alpha=0.3, axis='x')
plt.legend()
plt.show()