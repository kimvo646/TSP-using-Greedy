#Nho cai dat pip install networkx
#Nho cai dat pip install matplotlib
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import string

class Canh:
    def __init__(self, do_dai: float, dau: int, cuoi: int):
        self.do_dai = do_dai
        self.dau = dau
        self.cuoi = cuoi
  
#ĐỌC DỮ LIỆU từ ma trận đối xứng      
def read_file(file_name: str) -> Tuple[List[Canh], int]:
    edges = []
    with open(file_name, 'r') as f:
        n = int(f.readline())
        for i in range(n):
            line = f.readline()
            nums = list(map(float, line.split()))
            for j in range(i + 1, n + 1):  
                if j > i and nums[j - 1]!=0:
                    do_dai = nums[j - 1]
                    edge = Canh(do_dai, i, j - 1) 
                    edges.append(edge)
    return edges, n

#IN DANH SÁCH các cạnh và tính tổng độ dài của chúng
def in_ds_canh(a, la_PA): 
    tong = 0.0
    for i, canh in enumerate(a):
        if canh is not None:
            print("{:<3d} {}{}={:>8.2f}".format(i+1, chr(canh.dau+65), chr(canh.cuoi+65), canh.do_dai))
            if la_PA:
                tong += canh.do_dai
    if la_PA:
        print("Tổng độ dài các cạnh = {:>8.2f}".format(tong))

#SẮP XẾP các cạnh theo thứ tự từ nhỏ tới lớn
def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if a[j].do_dai < a[min_index].do_dai:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a

#KIỂM TRA cạnh mới có tạo thành đỉnh cấp 3 
def dinh_cap3(PA, k, moi):
    #Kiểm tra đỉnh đầu của cạnh
    i = 0
    dem = 1
    while i < k and dem < 3:
        if moi.dau == PA[i].dau or moi.dau == PA[i].cuoi:
            dem += 1
        i += 1
    if dem == 3:
        return 1
    #Kiểm tra đỉnh cuối của cạnh
    i = 0
    dem = 1
    while i < k and dem < 3:
        if moi.cuoi == PA[i].dau or moi.cuoi == PA[i].cuoi:
            dem += 1
        i += 1
    return dem == 3

#KHỞI TẠO gốc cây ban đầu -> mỗi đỉnh là 1 cây con độc lập:
def init_forest(parent, n):
    for i in range(n):
        parent.append(i)

def find_root(parent, u):
    while u != parent[u]:
        u = parent[u]
    return u

def chu_trinh (r_dau,r_cuoi):
  return r_dau == r_cuoi

def update_forest(parent, r1, r2):
    parent[r2] = r1

#GIẢI THUẬT THAM ĂN
def greedy(dscanh , n , PA):
    parent = []
    init_forest(parent, n)
    j = 0
    for i in range(len(dscanh)):
        if j >= n - 1:
            break
        r_dau = find_root(parent, dscanh[i].dau) # tìm đỉnh đầu
        r_cuoi = find_root(parent, dscanh[i].cuoi) # tìm đỉnh cuối
        if (dinh_cap3(PA, j, dscanh[i]) == False) and (chu_trinh(r_dau, r_cuoi) == False): #KIỂM TRA cạnh có tạo thành đỉnh 3 cấp và thành chu trình Hamilton
            PA[j] = dscanh[i]
            j += 1
            update_forest(parent, r_dau, r_cuoi)
    temp = 0
    for temp in range(len(dscanh)):
        r_dau = find_root(parent, dscanh[temp].dau)
        r_cuoi = find_root(parent, dscanh[temp].cuoi)
        if (dinh_cap3(PA, n-1, dscanh[temp]) == False) and (chu_trinh(r_dau, r_cuoi) == True):
            PA[n-1] = dscanh[temp]
            break

#VẼ ĐỒ THỊ vô hướng
def create_undirected_graph(PA):
    G = nx.Graph()
    for edge in PA:
        if edge is not None:
            dau = string.ascii_uppercase[edge.dau]  # Chuyển đỉnh thành chữ cái
            cuoi = string.ascii_uppercase[edge.cuoi]  # Chuyển đỉnh thành chữ cái
            do_dai = edge.do_dai
            G.add_edge(dau, cuoi, weight=do_dai)
    return G


if __name__ == "__main__":
    n = 0

#ĐỀ BÀI
    ds_canh, n = read_file("input10.txt") #vd tên file input10 -> n=10; input20 -> n=20
    print("Danh sách các cạnh của đồ thị:")
    in_ds_canh(ds_canh, 0)
#VẼ ĐỒ THỊ VÔ HƯỚNG
    # Tạo đồ thị vô hướng với độ dài nằm giữa các cạnh
    undirected_graph = create_undirected_graph(ds_canh)
    # Lấy độ dài của một cạnh
    weight = undirected_graph.get_edge_data('A', 'B')['weight']  # Sử dụng các chữ cái làm đỉnh
    # Vẽ đồ thị minh hoạ
    pos = nx.spring_layout(undirected_graph)  # Xác định vị trí các đỉnh
    nx.draw(undirected_graph, pos, with_labels=True)
    # Điền độ dài của các cạnh
    labels = nx.get_edge_attributes(undirected_graph, 'weight')
    nx.draw_networkx_edge_labels(undirected_graph, pos, edge_labels=labels)

#SẮP XẾP TỪ NHỎ TỚI LỚN
    selection_sort(ds_canh)
    print("\nDanh sách các cạnh đồ thị đã sắp xếp: ")
    in_ds_canh(ds_canh, 0)

#PHƯƠNG ÁN GIẢI CỦA GREEDY ALGORITHM
    PA = [None] * n
    greedy(ds_canh, n, PA)
    print("\nPhương Án: ")
    in_ds_canh(PA, 1)

# VẼ ĐỒ THỊ ĐƯỜNG ĐI
    # Tạo đồ thị cho phương án PA
    PA_graph = create_undirected_graph(PA)
    # Vẽ đồ thị cho phương án PA
    plt.figure()
    nx.draw(PA_graph, pos, with_labels=True)
    # Vẽ trọng số của các cạnh trong phương án PA
    labels_PA = nx.get_edge_attributes(PA_graph, 'weight')
    nx.draw_networkx_edge_labels(PA_graph, pos, edge_labels=labels_PA)
    plt.show()