import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['savefig.dpi']=150

N = 4
A = np.array([20, 30, 25, 25])
B = np.array([25, 30, 15, 30])
C = np.array([55, 40, 60, 45])
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

ind_p = ind + width/2
ind_m = ind - width/2
ind_line = np.sort(np.concatenate([ind_p,ind_m]))
A_line = (np.insert(A, np.arange(4), A))
B_line = (np.insert(B, np.arange(4), B)) + A_line
C_line = (np.insert(C, np.arange(4), C)) + B_line

fig, ax = plt.subplots()

p1 = ax.bar(ind, A, width,zorder=2)
p2 = ax.bar(ind, B, width,bottom=A,zorder=2)
p3 = ax.bar(ind, C, width,bottom=A+B,zorder=2)
print(A)
print(B)
print(A+B)

ax.plot(ind_line,A_line,'--k',zorder=1)
ax.plot(ind_line,B_line,'--k',zorder=1)
ax.plot(ind_line,C_line,'--k',zorder=1)

plt.ylabel('Scores')
plt.title('Scores by group')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4'))
plt.yticks(np.arange(0, 101, 20))
plt.legend((p1[0], p2[0],p3[0]), ('A', 'B','C'),
           bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=.1, fontsize=14)
# plt.savefig("stached_bar.png",bbox_inches = 'tight', pad_inches = 0)

plt.show()