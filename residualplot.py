import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
import pandas as pd

import sys
sys.path.append('C:/reasearch/Ba5Er2Al2SnO13/')

from impedance.validation import linKK
from impedance import preprocessing
from impedance.visualization import plot_residuals

# 読み取るCSVの絶対pathを指定,/で区切ること！
#保存場所にもなる
csvpath = "C:/reasearch/Ba5Er2Al2SnO13/AC_Zr/test.csv"
# fcutmin以上fcutmax以下の周波数の領域を採用。
fcutmax = 1E7
fcutmin = 10
# 入力項はここまで。

# Load data from the example EIS result
f, Z = preprocessing.readCSV(csvpath)

# keep only the impedance data in the first quandrant
f, Z = preprocessing.ignoreBelowX(f, Z)

mask = f <= fcutmax
f = f[mask]
Z = Z[mask]

mask = f >= fcutmin
f = f[mask]
Z = Z[mask]


M, mu, Z_linKK, res_real, res_imag = linKK(f, Z, c=0.85, max_M=1000, fit_type='complex', add_cap=True)

print('\nCompleted Lin-KK Fit\nM = {:d}\nmu = {:.2f}'.format(M, mu))

fig = plt.figure(figsize=(5,5))
ax2 = fig.add_subplot(111)

# Plot residuals
plot_residuals(ax2, f, res_real, res_imag, y_limits=(-2,2))

plt.tight_layout()
plt.show()

ret = messagebox.askyesno("csv保存","csvファイルを保存しますか？")
if ret == True:
    #保存場所の作成
    csvpath=csvpath[0:-4]
    csvpath += "_res.csv"
    data = np.array([f,res_real,res_imag])
    df_np_array = pd.DataFrame(data)
    df_np_arrayt = df_np_array.T
    exportdata = df_np_arrayt.rename(columns={0:"freq",1:"res_real",2:"res_img"})
    exportdata.to_csv(csvpath,index=False)