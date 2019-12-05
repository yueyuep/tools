import json
from Graph import ParseGraph
import networkx as nx


class ParseFile():
    fileName = ""
    Version = ""
    methodList = []
    MethodGraph = []
    path = ""

    def __init__(self, Path):
        self.path = Path
        self.Convert2Graph(path=Path)

    def Convert2Graph(self, path):
        headFile = {}
        with open(path, "rt", encoding="utf-8") as file:
            LineList = file.readlines()
            str1 = LineList[0]
            # 头文件行
            headFile = {}
            try:
                headFile = json.loads(LineList[0])
            except Exception:
                print("{url}：输入数据不符合json格式：", format(url=self.path))
                exit()
            # 下面的所有函数行
            methodLine = LineList[1:]
            self.fileinfo(headFile=headFile)
            self.methodGraph(methodLine=methodLine)

    def fileinfo(self, headFile):
        self.fileName = headFile["fileName"]
        self.Version = headFile["version"]
        self.methodList = headFile["hasMethodName"]

    def methodGraph(self, methodLine):
        flag = True
        tempList = []
        for method in methodLine:
            methoddic = {}
            try:
                methoddic = json.loads(method)
            except Exception:
                print("{url}：输入数据不符合json格式：", format(url=self.path))
                exit()
            singleGraph = []
            # 得到函数申明的函数名
            try:
                methodname = methoddic["methodName"]
            except Exception:
                print("the url is {url}:".format(url=self.path))

            # 得到函数的callMethodNameRederTo节点
            callMethodNameReferTo = methoddic["callMethodNameReferTo"]
            g = ParseGraph(methoddic)
            # 添加节点间关系
            graph = g.Parse1()
            # =============================增加节点的属性(后面会修改)========================
            # graph=self.addAttritude(methodname,graph)
            # ============================================================================
            singleGraph = [methodname, callMethodNameReferTo, graph]
            tempList.append(singleGraph)
        self.MethodGraph = tempList

    # def showSimRank(self):
    #     for methodgraph in self.MethodGraph:
    #         methodname = methodgraph[0]
    #         graph = methodgraph[2]
    #         sim = simrank(graph)
    #         print("methodName:{name}\n SimRank:\n{sim}".format(name=methodname, sim=sim))

    def addAttritude(self, methodname, graph):
        # 此处有bug，属性设置有问题
        attriDic = {"filename": self.fileName, "version": self.Version, "methodname": methodname}
        for node in graph.nodes():
            graph.add_node(node, attriDic)
        return graph

    def connectFile(self):
        # 将整个文件的节点连接起来
        # filel_node,filel_node_attri=self.fileName+"_"+self.Version,{"filename":self.fileName,"Version":self.Version}
        filel_node = self.fileName
        fileGraph = nx.DiGraph()
        fileGraph.add_node(filel_node)  # 文件根节点
        for methodgraph in self.MethodGraph:
            graph = methodgraph[2]
            # 从已知图的节点中构建新图
            # H.add_nodes_from(G.nodes(data=True))
            methodNode = methodgraph[0]
            fileGraph.add_edges_from(graph.edges(data=True))
            fileGraph.add_edge(filel_node, methodNode, connecting="include")
            print("{file}:connected! \n".format(file=methodgraph[0]))
        return fileGraph

    def getfileName(self):
        return self.fileName

    def getVersion(self):
        return self.Version

    def getMethodGraph(self):
        return self.MethodGraph


if __name__ == '__main__':
    path = "F:\GraphSim\jsondata\CWE190_Integer_Overflow__int_Environment_preinc_81a.java.txt"
    file = ParseFile(path)
    # 得到整个文件所有函数的节点间关系
    file_method_graph = file.connectFile()
    file.showSimRank()
    print("Done!")
