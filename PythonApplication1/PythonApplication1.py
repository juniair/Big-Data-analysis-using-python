
import platform
import matplotlib.pyplot as plt


from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Linux':
    path = "/opt/conda/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf/NanumGothic.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)    
else:
    print('Unknown system')

import pandas as pd

col_names = ['스트레스', '스트레스남학생', '스트레스여학생', '우울감경험률', 
             '우울남학생', '우울여학생','자살생각율', '자살남학생', '자살여학생']

raw_data = pd.read_excel("teenage_mental.xlsx", 
                         header=1, 
                         usecols="C:K",
                         names=col_names)

raw_data.loc[1] = 100. - raw_data.loc[0]
raw_data['응답'] = ['그렇다','아니다']
raw_data.set_index('응답',drop=True, inplace=True)

raw_data



labels = '그렇다', '아니다'

