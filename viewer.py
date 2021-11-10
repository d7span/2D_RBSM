import numpy as np
import matplotlib.pyplot as plt

class ElementData:
    #クラスの初期化はファイルの読み込みと同時に行う
    def __init__(self,filename):
        f = open(filename, 'r', encoding = "utf-8_sig")
        text = f.readline() #要素数 最大頂点数
        text = f.readline() 
        text = text.strip()
        text = text.split()
        self.nelm = int(text[0])
        self.maxnode = int(text[1])

        #配列の作成&初期化
        self.xelm = np.zeros(self.nelm,dtype=np.float64)
        self.yelm = np.zeros(self.nelm,dtype=np.float64)
        self.ten = np.zeros(self.nelm,dtype=np.int64)
        self.node = np.zeros([self.nelm,self.maxnode],dtype=np.int64)

        text = f.readline() #頂点数, 節点番号
        for i in range(0,self.nelm):
            text = f.readline()     
            text = text.strip()
            text = text.split()
            self.xelm[i] = text[1]
            self.yelm[i] = text[2]
            self.ten[i] = int(text[3])
            for j in range(0,self.ten[i]):
                self.node[i][j] = int(text[j+4])

        text = f.readline() #節点数
        text = f.readline()
        text = text.strip()
        self.nnode = int(text)

        #配列の作成&初期化
        self.xnode = np.zeros(self.nnode,dtype=np.float64)
        self.ynode = np.zeros(self.nnode,dtype=np.float64)

        text = f.readline() #X座標, #Y座標
        for i in range(0,self.nnode):
            text = f.readline() 
            text = text.strip() 
            text = text.split()
            self.xnode[i] = text[1]
            self.ynode[i] = text[2]
            
def plot_figure(ELEM):
    fig, ax = plt.subplots(figsize=(16, 12.0))
    ax.set_aspect("equal")
    color=(0.85,0.85,0.85,0.9)  

    #temporaryなリスト作成
    _x = [] 
    _y = []
    for i in range(0,ELEM.nelm):
        for j in range(0,ELEM.ten[i]):
            node = ELEM.node[i][j]
            _x.append(ELEM.xnode[node-1])
            _y.append(ELEM.ynode[node-1]) 

        ax.fill(_x,_y,edgecolor="black",facecolor="white")
        _x.clear()
        _y.clear()
        #要素母点の表示(option化)
        plt.plot(ELEM.xelm[i],ELEM.yelm[i], marker='.', color="k")

    for i in range(0,ELEM.nnode):
        #節点の表示(option化)
        plt.plot(ELEM.xnode[i],ELEM.ynode[i], marker='.', color="k")

    plt.show()

#クラスの初期化
ELEM = ElementData("ELEMENT.INDAT")

print("ELEMENT.INDAT 読み込み")
print("NELM=",ELEM.nelm,"NNODE=",ELEM.nnode)

#要素を描画
plot_figure(ELEM)



