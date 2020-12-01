import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt
# 폰트 설정
mpl.rc('font', family='Malgun Gothic')
# 유니코드에서  음수 부호설정
mpl.rc('axes', unicode_minus=False)
# 그래프 크기 고정
plt.rcParams['figure.figsize'] = [10, 10]


class Cartogram:
    def __init__(self):
        pass

    def drawKorea(targetData, blockedMap, cmapname):
        gamma = 0.75

        whitelabelmin = (max(blockedMap[targetData]) -
                         min(blockedMap[targetData]))*0.25 + \
            min(blockedMap[targetData])

        datalabel = targetData

        vmin = min(blockedMap[targetData])
        vmax = max(blockedMap[targetData])

        mapdata = blockedMap.pivot_table(
            index='y', columns='x', values=targetData)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)

        # 지역 이름 표시
        for idx, row in blockedMap.iterrows():
            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다.
            #(중구, 서구)
            if len(row[2].split()) == 2:
                dispname = '{}\n{}'.format(
                    row[2].split()[0], row[2].split()[1])
            elif row[2][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row[2]

            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.

            annocolor = 'white' if row[targetData] > whitelabelmin else 'black'
            plt.annotate(dispname, (row[1]+0.5, row[0]+0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        # 시도 경계 그린다.
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)

        plt.gca().invert_yaxis()

        plt.axis('off')

        cb = plt.colorbar(shrink=.1, aspect=10)
        cb.set_label(datalabel)

        plt.tight_layout()
        plt.show()
