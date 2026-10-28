import numpy as np
from scipy.spatial import distance
from collections import deque


def Algorithm1(X,k,metric='euclidean'):
    """Gonzalez贪心k-center算法（无公平约束，不公平版本）
    输入：
    X   数据集二维数组
    k   需要选取的中心点数量
    metric 距离度量
    输出：
    C: 选出的中心点下标列表
    kDistance: 保存每个中心点到全部样本的距离向量，供后续fair-shift使用"""

    C = np.array([])  #用于保存k个中心点下标的集合C
    k_distance = np.array([]) #集合X各个点到集合C中各个距离，形状kxn
    if k == 0:
        return C,k_distance
    n = X.shape([0])
    d = X.shape([1])    #矩阵的行和列
    candidate = np.random.randint(0,n)
    C = np.append(C,candidate)
    min_distance = distance.cdist(X[candidate],X,metric)
    k_distance = np.append(k_distance,min_distance)
    kk = 1  #kk表示集合C中元素的个数
    while kk < k:
        candidate = np.argmax(min_distance)
        C = np.append(candidate)
        new_distance = distance.cdist(X[candidate],X,metric)
        k_distance = np.vstack((k_distance,new_distance))
        min_distance = min(np.vstack((min_distance,new_distance)),axis=0)
        kk += 1
    return C,k_distance
#############################################################################


def Algorithm3(X,k_distance,A,h,group,d,neighbors,f_distance,metric='euclidean'):
    """
    算法3用于对公平约束的检测，若满足 h=max_flow，则返回满足
    最大流的边集，若不满足，则返回空集
    X   数据集
    A   算法1选出的中心点集合
    h   当前集合A的长度
    d   用于约束平移点距离不可以超过d
    group   group[i]表示群体i在X最后一个群体的下标
    neighbors   len(A) × m 数组，每个点记录【每个分组中离它最近的样本下标】
    f_distance    len(A) × m 数组，对应上面最近样本的距离
    """
    class Edge:
        """边类"""
        def __init__(self,to,capacity,rev):
            self.to = to    #指向弧尾的顶点
            self.cap = capacity #边的容量
            self.rev = rev  #反向边，该顶点在弧尾顶点的邻接边的位置
        


    class BuiltGraph:
        """构建邻接矩阵"""
        def __init__(self,n):
            self.n = n  #顶点个数
            self.graph = [[] for _ in range(n)] #邻接表


        def add_edge(self,u,v,cap):
            """"
            添加一条边
            u   弧头顶点
            v   弧尾顶点
            cap 容量
            """
            self.graph[u].append(Edge(v,cap,len(self.graph[v])))
            self.graph[v].append(Edge(u,0,len(self.graph[u]-1)))


    def BFS(G,s,t):
        """
        找水平图，返回水平图level,否则返回空集[]
        s   源点
        t   汇点
        G   邻接表
        """
        level = [-1]*G.graph.n  #初始化水平图
        level[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for edge in G.graph[u]:
                if level[edge.to] < 0 and edge.cap > 0:
                    level[edge.to] = level[u] + 1
                    queue.append(edge.to)
        if level[t] >=0:
            return level
        return []


    def DFS(G,level,v,t,f,iter):
        """
        G   邻接表
        level 水平图
        v   当前节点
        t   汇点t
        f   流量
        iter    对顶点v从它的第(iter)条边开始遍历
        """
        if v == t:
            return f
        for i in range(iter[v],len(G.graph)):
            edge = G.graph[v][i]
            if edge.cap > 0 and level[v] < level[edge.to]:
                d = DFS(G,level,edge.to,t,min(f,edge.cap),iter)
                if d > 0:
                    edge.cap -= d
                    G.graph[edge.to][edge.rev].cap += d
                    return d
            iter[v] += 1
        return 0    

    def max_flow(G,s,t):
        flow = 0
        while True:
            level = BFS(G,s,t)
            if len(level) == 0:
                return flow
            iter = [0] * G.graph.n
            while True:
                f = DFS(G,level,s,t,flow('inf'),iter)
                if f == 0:
                    break
                flow += f


    def a_to_X_min_distance(X,A,a,k_distance,group,m):
        """
        求中心点a到各个群体的最小矩阵，返回f_distance,vertex
        a   为集合A的下标,表示A[a]里面的顶点
        m   群体个数
        """
        f_distance = np.array([])
        vertex = np.array([])
        if X.shape[0] == 0:
            return f_distance,vertex
        mask = [True] * X.shape[0]
        mask[A] = False
        start = 0
        for i in range(0,m):
            end = group[i] + 1
            mask_group = mask[start:end]
            mask_index = np.arange(start,end)
            i_distance = k_distance[a,start:end]
            i_index = np.where(mask_group)
            min_value_index = np.argmin(i_distance[mask_group])
            min_value = np.min(i_distance[mask_group])
            f_distance[i] = min_value
            vertex[i] = start + i_index[min_value_index]
            start = end





    m = len(group)  #群体个数
    G = BuiltGraph(h+m+2)
    s = h + m  #源点
    t = h + m + 1   #汇点

    #构建v_f群体点-> t的边
    for u in range(h,h+m):
        G.add_edge(u,t,group[u-h])

    #构建s —> V_A中心点的边
    for u in range(0,h):
        G.add_edge(s,u,1)

    #构建v_a -> v_f 的边
    mask = np.ones(len(A),dtype=bool)
    
    for v_a in range(0,h):
        



    


    
        
        

    


