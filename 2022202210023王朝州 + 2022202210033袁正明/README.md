### 静态装箱

\1. 所有的参数为整数；2. 静态装箱，即从n个箱子中选取m个箱子，并实现m个箱子在车厢中的摆放（无需考虑装箱的顺序，即不需要考虑箱子从内向外，从下向上这种在车厢中的装箱顺序）；3. 所有的箱子全部平放，即箱子的最大面朝下摆放；4. 算法时间不做严格要求，只要1天内得出结果都可。

```
箱子：立方体，具有多种类型
子车厢：立方体，由于装载箱子而分割出的空闲空间

当箱子装入一个子车厢时，会分割子车厢，产生三个新的子车厢，新子车厢会按照体积大小，由小到大放入子车厢链表，体积过小的子车厢不能放入任何一种箱子而被丢弃。当要装入一个箱子时，会优先选择最小的子车厢进行装载。子车厢可能在空间上是邻近的，甚至是可以合并的，对于能够合并的子车厢会进行合并操作。	
```

```
//将空闲子车厢插入子车厢链表，并进行合并
Algorithm 1 Insert sub Carriage
Input：SubCarriage[],c[];SubCarriagelist,list
Output:SubCarriagelist
1:	procedure insertSubCarriage(list,c)
2:		pre=list
3:		while p do
4:			for item in c
5:				if canbemerged(p,item) then
6:					c[item]=merge(p,item)
7:				end if
8:				if Is the insertion point then
9:					pos[item]=pre
10:				end if
11:			end for
12:			p=p.next
13:		end while
14:		list.insert(pos,c)
15:		return list
16:	end procedure
```

```golang
//采用遗传算法获取最佳路径。
//以装入的箱子种类构造染色体序列
//如：[0,1,0,2,3,4,0,4,3,2,1,2,0]
//交叉时会产生非法解
//对非法解进行调整
func adjustment(c []int, arr []int,pivot int){
	//调整非法解为合法解
	//非法解产生，由于交叉改变了各类箱子的个数，有的多了，有的少了
	//调整：多了的（正），需要替换为少了的（负）
	//交叉是对后半部分进行交换，后半部分引起的非法，调整前半部分可以解决
	//例如，染色体1交换后3号箱子会变多，换言之，未交换之前，3号箱子集中在前半部分，
	//那么，将前半部分多余的3号箱子改为减少的箱子即可平衡
	//arr 数组用于标记id号箱子多了或欠缺的个数
	for i:=0;i<pivot;i++{
		if arr[c[i]]>0{//多余的
			arr[c[i]]-=1
			neg:=getneg(arr)//缺少的
			c[i]=neg
			arr[neg]+=1
		}
	}
}
```



```sh
//run
go run ./main.go
```

