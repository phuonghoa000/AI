import pdb

def aprioriGen(freq_sets, k):
    "tao cac moi ket hop tu cac tap ung vien"
    List = []
    lenLk = len(freq_sets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                List.append(freq_sets[i] | freq_sets[j])
    return List

def generateRules(L, support_data, k, min_confidence, output):
    """Tao ra cac luat ket hop
    L: DS cac luat pho bien
    support_data: support cho cac hang muc
    k: so phan tu trong cac hang muc
    """
    g = open(output,"w")
    rules = []
    #pdb.set_trace()
    if (k == 1):
        k = len(L)
    for i in range(1, k):
        for Set in L[i]:
            "freqSet: la cac tap pho bien"
            "tach 1 tap pho bien lon ra cac tap pho bien nho hon"
            H1 = [frozenset([item]) for item in Set]
            if (i > 1):
                rules_from_conseq(Set, H1, support_data, rules, min_confidence,g)
            else:
                calc_confidence(Set, H1, support_data, rules, min_confidence, g)
    return rules


def calc_confidence(Set, H, support_data, rules, min_confidence, output):
    "xac thu luat pho bien phu hop va in ra"
    pruned = []
    for conseq in H:
        conf = support_data[Set] / support_data[Set - conseq]
        if conf >= min_confidence:
            x = list(Set - conseq)
            z = list(Set)
            conf = round(conf,2)
            tmp = str(conf)
            string = tmp
            for i in range(0,len(x)):
                tmp = str(x[i])
                string =  string +  ' ' + tmp
            string = string + ' -> '
            for i in range(0,len(z)):
                tmp = str(z[i])
                string = string + ' ' + tmp
            output.write(string)
            output.write('\n')
            rules.append((Set - conseq, conseq, conf))
            pruned.append(conseq)
    return pruned


def rules_from_conseq(Set, H, support_data, rules, min_confidence, output):
    "tao ra cac tap ung vien va xac thuc luat pho bien"
    m = len(H[0])
    if (len(Set) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(Set, Hmp1,  support_data, rules, min_confidence,output)
        if len(Hmp1) > 1:
            rules_from_conseq(Set, Hmp1, support_data, rules, min_confidence, output)

class pattern:
    """de luu cac phan tu cua luat pho bien
    total: tat ca cac phan tu ke ca item va FP
    FP: frequence Pattern
    item: cac phan tu cua luat pho bien
    
    """
    def __init__(self, total):
        self.total = total
        self.FP = total[0]
        self.item = []
        
        for i in range(1,len(total)):
            self.item.append(total[i])

        
        self.k = len(self.total) - 1
        
    def exportItem(self):
        "export ra tuple de co the phan ra cac phan tu ra"
        return(tuple(self.item))
    
    def exportFP(self):
        return self.FP
    
    def exportK(self):
        return self.k
        
from sys import argv

script, inp, out, min_conf,k = argv
"Dict chua support data"
supData ={}
"List chua cac tap ung vien"
Data = []
k = int(k)
min_conf = float(min_conf)
"khoi tao mang 2 chieu"
for i in range(0,50):
    Data.append([])
    
with open(inp,"r") as f:
    for line in f:
        itemSet ={}
        number = line.split()
        number[0] = float(number[0])
        
        for i in range(1,len(number)):
            number[i] = int(number[i])
            
        "tao mot bien tam de luu luat pho bien "
        temp = pattern(number)  
        "itemSet la bien tam de luu du lieu cua luat pho bien"
        itemSet.update({frozenset(temp.exportItem()): temp.exportFP()})
        "m la so item cua luat pho bien"
        m = temp.exportK()  
        supData.update(itemSet)
        Data[m-1].append(frozenset(temp.exportItem()))



a = []        
a = generateRules(Data,supData,k,min_conf, out)




