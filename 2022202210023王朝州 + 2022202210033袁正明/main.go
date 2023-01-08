package main

import (
	cr "crypto/rand"
	"fmt"
	"math/big"
	"math/rand"
	"time"
)


type POINT struct {
	x int
	y int
	z int
}
type BOX struct {
	L int
	W int
	H int
	N int
	pos    POINT
	volume int
	next   *BOX
}

type SOLUTION struct {
	Seq []BOX
	SubCarriage *BOX	// 空闲车厢的头指针
	L_min int
	W_min int
	H_min int
}
//插入空闲车厢序列
func(s*SOLUTION) insertSubCarriage(boxs []*BOX){
	var p1*BOX
	var p2*BOX
	p1=s.SubCarriage
	p2=p1.next
	var flag []*BOX
	for i:=0;i<len(boxs);i++{
		flag=append(flag,nil)
	}
	for ;p2!=nil;{
		for i:=0;i<len(boxs);i++{
			// 先合并，再排序
			if isMerge(boxs[i],p2){
				//p3被摘下来
				p3:=p2
				p2=p3.next//p2可能变成nil
				p1.next=p2
				//合并p3与boxs[i]
				boxs[i]=merge(boxs[i],p3)
			}
			if p2==nil{
				//fmt.Println("NIL!")
				break
			}
			if flag[i]==nil&&p2.volume >boxs[i].volume {flag[i]=p1}
		}
		if p2==nil{break}
		p1=p2
		p2=p2.next
	}
	//已经合并并找到了插入点，进行插入
	for i:=0;i<len(flag);i++{
		if flag[i]!=nil{
			boxs[i].next=flag[i].next
			flag[i].next=boxs[i]
		}else{//插入到末尾
			if p1.next!=nil{p1=p1.next}
			boxs[i].next=nil
			p1.next=boxs[i]
		}
	}
}
//判断两个车厢是否可以合并
func isMerge(b1 ,b2 *BOX)bool{
	//x相同，y不同，y1+w1==y2或者y2+w2==y1 并且L1==L2，H1==H2
	if b1.L==b2.L&&b1.H==b2.H&&(b1.pos.x==b2.pos.x)&&(b1.W+b1.pos.y==b2.pos.y||b2.W+b2.pos.y==b1.pos.y){
		return true
	}
	//y相同，x不同，x1+L1==x2或者x2+L2==x1 并且W1==W2,H1==LH
	if b1.H==b2.H&&b1.W==b2.W&&(b1.pos.y==b2.pos.y)&&(b1.pos.x+b1.L==b2.pos.x||b2.pos.x+b2.L==b1.pos.x){
		return true
	}
	return false
}
func merge(b1,b2 *BOX)*BOX{
	if b1.pos.x==b2.pos.x{
		if b1.pos.y<b2.pos.y{
			b1.W+=b2.W
			return b1
		}else{
			b2.W+=b1.W
			return b2
		}
	}else{
		if b1.pos.x<b2.pos.x{
			b1.L+=b2.L
			return b1
		}else{
			b2.L+=b1.L
			return b2
		}
	}
}

// PutCarriage 把箱子放进车厢
func (s *SOLUTION)PutCarriage(b,c BOX){
	//将箱子b 放进车厢c中，放置后分割生成新的小车厢，将小车厢返回
	b.pos=c.pos
	s.Seq=append(s.Seq, b)
	//分割生成3个小车厢
	//第一个
	var boxes []*BOX
	if c.L-b.L>=s.L_min||c.L-b.L>=s.W_min||c.L-b.L>=s.H_min{
		c1:=&BOX{
			L:   c.L-b.L,
			W:   c.W,
			H:   c.H,
			pos: POINT{
				x: c.pos.x+b.L,
				y: c.pos.y,
				z: c.pos.z,
			},
		}
		if s.isSuitableSize(c1){
			boxes =append(boxes, c1)
		}
	}
	//第二个
	if c.W-b.W>=s.W_min||c.W-b.W>=s.L_min||c.W-b.W>=s.H_min{
		c2:=&BOX{
			L:   b.L,
			W:   c.W-b.W,
			H:   c.H,
			pos: POINT{
				x: c.pos.x,
				y: c.pos.y+b.W,
				z: c.pos.z,
			},
		}
		if s.isSuitableSize(c2){
			boxes =append(boxes, c2)
		}
	}
	//第三个
	if c.H-b.H>=s.H_min||c.H-b.H>=s.L_min||c.H-b.H>=s.W_min{
		c3:=&BOX{
			L:   b.L,
			W:   b.W,
			H:   c.H-b.H,
			pos: POINT{
				x: c.pos.x,
				y: c.pos.y,
				z: c.pos.z+b.H,
			},
		}
		if s.isSuitableSize(c3){
			boxes =append(boxes, c3)
		}
	}
	for i:=0;i<len(boxes);i++{
		boxes[i].volume = boxes[i].L * boxes[i].W * boxes[i].H
	}
	//对boxes升序
	for i:=0;i<len(boxes);i++{
		for j:=i+1;j<len(boxes);j++{
			if boxes[j].volume < boxes[i].volume {
				temp:= boxes[j]
				boxes[j]= boxes[i]
				boxes[i]=temp
			}
		}
	}
	//插入boxes
	s.insertSubCarriage(boxes)
}
//检查车厢是否符合最小大小
func (s*SOLUTION) isSuitableSize(b*BOX)bool{
	if b.L>=s.L_min&&b.W>=s.W_min&&b.H>=s.H_min{
		return true
	}
	return false
}

// Select 给箱子选择一个合适的车厢
func(s*SOLUTION)Select(b BOX)error{
	if s.SubCarriage.next==nil{
		return fmt.Errorf("没有空余车厢")
	}

	p1:=s.SubCarriage
	p2:=p1.next
	var p3 *BOX
	for ;p2!=nil;{
		//判断是否合适
		if isSuitableFit(&b,p2){
			//删除p2节点
			p1.next=p2.next
			//装箱
			s.PutCarriage(b,*p2)
			return nil
		}

		p2=p2.next
		if p2==nil{p3=p1}
		p1=p1.next
	}
	if p1!=s.SubCarriage&&isSuitableFit(&b,p1){
		//删除p1节点
		p3.next=p1.next
		//装箱
		s.PutCarriage(b,*p1)
		return nil
	}
	return fmt.Errorf("没找到合适的车厢")
}

//检查空闲车厢c是否足够放置箱子b
func isSuitableFit(b,c *BOX)bool{

	if c.L<b.L||c.W<b.W||c.H<b.H{
		return false
	}
	return true
}

// Evaluate 评估，计算空间利用率
func(s *SOLUTION)Evaluate()float64{
	sum:=0
	for _,item:=range s.Seq {
		sum+=item.L*item.W*item.H
	}
	x:=587*233*220

	//fmt.Println("空间利用率",float64(sum)/float64(x))
	return float64(sum)/float64(x)
}

//排序
type array []BOX
func (a array) Len() int {
	return len(a)
}
func (a array) Swap(i, j int) {
	a[i], a[j] = a[j], a[i]
}
func (a array) Less(i, j int) bool {
	return a[i].volume < a[j].volume
}
//end 排序


//加载箱子数据
func loadData()[][]BOX{
	var E1_1 =[]BOX{{L: 108,W: 76,H: 30,N: 40},{L: 110,W: 43,H: 25,N: 33},{L: 92,W: 81,H: 55,N: 39}}
	var E1_2 =[]BOX{{L: 91,W: 54,H: 45,N: 32},{L: 105,W: 77,H: 72,N: 24},{L: 79,W: 78,H: 48,N: 30}}
	var E1_3=[]BOX{{L: 91,W: 54,H: 45,N: 32},{L: 105,W: 77,H: 72,N: 24},{L: 79,W: 78,H: 48,N: 30}}
	var E1_4=[]BOX{{L:60,W:40,H:32,N:64},{L:98,W:75,H:55,N:40},{L:60,W:59,H:39,N:64}}
	var E1_5=[]BOX{{L:78,W:37,H:27,N:63},{L:89,W:70,H:25,N:52},{L:90,W:84,H:41,N:55}}
	var E2_1 =[]BOX{{L: 108,W: 76,H: 30,N: 24},{L: 110,W: 43,H: 25,N: 7},{L: 92,W: 81,H: 55,N: 22},{L: 81,W: 33,H: 28,N: 13},{L: 120,W: 99,H: 73,N: 15}}
	var E2_2=[]BOX{{L:49,W:25,H:21,N:22},{L:60,W:51,H:41,N:22},{L:103,W:76,H:64,N:28},{L:95,W:70,H:62,N:25},{L:111,W:49,H:26,N:17}}
	var E2_3=[]BOX{{L:88,W:54,H:39,N:25},{L:94,W:54,H:36,N:27},{L:87,W:77,H:43,N:21},{L:100,W:80,H:72,N:20},{L:83,W:40,H:36,N:24}}
	var E2_4=[]BOX{{L:90,W:70,H:63,N:16},{L:84,W:78,H:28,N:28},{L:94,W:85,H:39,N:20},{L:80,W:76,H:54,N:23},{L:69,W:50,H:45,N:31}}
	var E2_5=[]BOX{{L:74,W:63,H:61,N:22},{L:71,W:60,H:25,N:12},{L:106,W:80,H:59,N:25},{L:109,W:76,H:42,N:24},{L:118,W:56,H:22,N:11}}
	var E3_1=[]BOX{{L:108,W: 76,H: 30,N: 24},{L:110,W: 43,H: 25,N: 9},{L: 92,W: 81,H: 55,N: 8},{L: 81,W: 33,H: 28,N: 11},{L: 120, W: 99,H: 73,N: 11},{L: 111,W: 70,H: 48,N: 10},{L: 98,W: 72,H: 46,N: 12},{L: 95,W: 66,H: 31,N: 9}}
	var E3_2=[]BOX{{L:97,W:81,H:27,N:10},{L:102,W:78,H:39,N:20},{L:113,W:46,H:36,N:18},{L:66,W:50,H:42,N:21},{L:101,W:30,H:26,N:16},{L:100,W:56,H:35,N:17},{L:91,W:50,H:40,N:22},{L:106,W:61,H:56,N:19}}
	var E3_3=[]BOX{{L:88,W:54,H:39,N:16},{L:94,W:54,H:36,N:14},{L:87,W:77,H:43,N:20},{L:100,W:80,H:72,N:16},{L:83,W:40,H:36,N:6},{L:91,W:54,H:22,N:15},{L:109,W:58,H:54,N:17},{L:94,W:55,H:30,N:9}}
	var E3_4=[]BOX{{L:49,W:25,H:21,N:16},{L:60,W:51,H:41,N:8},{L:103,W:76,H:64,N:16},{L:95,W:70,H:62,N:18},{L:111,W:49,H:26,N:18},{L:85,W:84,H:72,N:16},{L:48,W:36,H:31,N:17},{L:86,W:76,H:38,N:6}}
	var E3_5=[]BOX{{L:113,W:92,H:33,N:23},{L:52,W:37,H:28,N:22},{L:57,W:33,H:29,N:26},{L:99,W:37,H:30,N:17},{L:92,W:64,H:33,N:23},{L:119,W:59,H:39,N:26},{L:54,W:52,H:49,N:18},{L:75,W:45,H:35,N:30}}
	var E4_1=[]BOX{{L:49,W:25,H:21,N:13},{L:60,W:51,H:41,N:9},{L:103,W:76,H:64,N:11},{L:95,W:70,H:62,N:14},{L:111,W:49,H:26,N:13},{L:85,W:84,H:72,N:16},{L:48,W:36,H:31,N:12},{L:86,W:76,H:38,N:11},{L:71,W:48,H:47,N:16},{L:90,W:43,H:33,N:8}}
	var E4_2=[]BOX{{L:97,W:81,H:27,N:8},{L:102,W:78,H:39,N:16},{L:113,W:46,H:36,N:12},{L:66,W:50,H:42,N:12},{L:101,W:30,H:26,N:18},{L:100,W:56,H:35,N:13},{L:91,W:50,H:40,N:14},{L:106,W:61,H:56,N:17},{L:103,W:63,H:58,N:12},{L:75,W:57,H:41,N:13}}
	var E4_3=[]BOX{{L:86,W:84,H:45,N:18},{L:81,W:45,H:34,N:19},{L:70,W:54,H:37,N:13},{L:71,W:61,H:52,N:16},{L:78,W:73,H:40,N:10},{L:69,W:63,H:46,N:13},{L:72,W:67,H:56,N:10},{L:75,W:75,H:36,N:8},{L:94,W:88,H:50,N:12},{L:65,W:51,H:50,N:13}}
	var E4_4=[]BOX{{L:113,W:92,H:33,N:15},{L:52,W:37,H:28,N:17},{L:57,W:33,H:29,N:17},{L:99,W:37,H:30,N:19},{L:92,W:64,H:33,N:13},{L:119,W:59,H:39,N:19},{L:54,W:52,H:49,N:13},{L:75,W:45,H:35,N:21},{L:79,W:68,H:44,N:13},{L:116,W:49,H:47,N:22}}
	var E4_5=[]BOX{{L:118,W:79,H:51,N:16},{L:86,W:32,H:31,N:8},{L:64,W:58,H:52,N:14},{L:42,W:42,H:32,N:14},{L:64,W:55,H:43,N:16},{L:84,W:70,H:35,N:10},{L:76,W:57,H:36,N:14},{L:95,W:60,H:55,N:14},{L:80,W:66,H:52,N:14},{L:109,W:73,H:23,N:18}}
	var E5_1=[]BOX{{L:98,W:73,H:44,N:6},{L:60,W:60,H:38,N:7},{L:105,W:73,H:60,N:10},{L:90,W:77,H:52,N:3},{L:66,W:58,H:24,N:5},{L:106,W:76,H:55,N:10},{L:55,W:44,H:36,N:12},{L:82,W:58,H:23,N:7},{L:74,W:61,H:58,N:6},{L:81,W:39,H:24,N:8},{L:71,W:65,H:39,N:11},{L:105,W:97,H:47,N:4},{L:114,W:97,H:69,N:5},{L:103,W:78,H:55,N:6},{L:93,W:66,H:55,N:6}}
	var E5_2=[]BOX{{L:108,W:76,H:30,N:12},{L:110,W:43,H:25,N:12},{L:92,W:81,H:55,N:6},{L:81,W:33,H:28,N:9},{L:120,W:99,H:73,N:5},{L:111,W:70,H:48,N:12},{L:98,W:72,H:46,N:9},{L:95,W:66,H:31,N:10},{L:85,W:84,H:30,N:8},{L:71,W:32,H:25,N:3},{L:36,W:34,H:25,N:10},{L:97,W:67,H:62,N:7},{L:33,W:25,H:23,N:7},{L:95,W:27,H:26,N:10},{L:94,W:81,H:44,N:9}}
	var E5_3=[]BOX{{L:49,W:25,H:21,N:13},{L:60,W:51,H:41,N:9},{L:103,W:76,H:64,N:8},{L:95,W:70,H:62,N:6},{L:111,W:49,H:26,N:10},{L:74,W:42,H:40,N:4},{L:85,W:84,H:72,N:10},{L:48,W:36,H:31,N:10},{L:86,W:76,H:38,N:12},{L:71,W:48,H:47,N:14},{L:90,W:43,H:33,N:9},{L:98,W:52,H:44,N:9},{L:73,W:37,H:23,N:10},{L:61,W:48,H:39,N:14},{L:75,W:75,H:63,N:11}}
	var E5_4=[]BOX{{L:97,W:81,H:27,N:6},{L:102,W:78,H:39,N:6},{L:113,W:46,H:36,N:15},{L:66,W:50,H:42,N:8},{L:101,W:30,H:26,N:6},{L:100,W:56,H:35,N:7},{L:91,W:50,H:40,N:12},{L:106,W:61,H:56,N:10},{L:103,W:63,H:58,N:8},{L:75,W:57,H:41,N:11},{L:71,W:68,H:64,N:6},{L:85,W:67,H:39,N:14},{L:97,W:63,H:56,N:9},{L:61,W:48,H:30,N:11},{L:80,W:54,H:35,N:9}}
	var E5_5 =[]BOX{{L: 113,W: 92,H: 33,N: 8},{L: 52,W: 37,H: 28,N: 12},{L: 57,W: 33,H: 29,N: 5},{L: 99,W: 37,H: 30,N: 12}, {L: 92,W: 64,H: 33,N: 9},{L: 119,W: 59,H: 39,N: 12},{L: 54,W: 52,H: 49,N: 8},{L: 75,W: 45,H: 35,N: 6}, {L: 79,W: 68,H: 44,N: 12},{L: 116,W: 49,H: 47,N: 9},{L: 83,W: 44,H: 23,N: 11},{L: 98,W: 96,H: 56,N: 10},{L: 78,W: 72,H: 57,N: 8}, {L: 98,W: 88,H: 47,N: 9},{L: 41,W: 33,H: 31,N: 13}}

	var Boxlist [][]BOX
	Boxlist=append(Boxlist, E1_1)
	Boxlist=append(Boxlist, E1_2)
	Boxlist=append(Boxlist, E1_3)
	Boxlist=append(Boxlist, E1_4)
	Boxlist=append(Boxlist, E1_5)
	Boxlist=append(Boxlist, E2_1)
	Boxlist=append(Boxlist, E2_2)
	Boxlist=append(Boxlist, E2_3)
	Boxlist=append(Boxlist, E2_4)
	Boxlist=append(Boxlist, E2_5)
	Boxlist=append(Boxlist, E3_1)
	Boxlist=append(Boxlist, E3_2)
	Boxlist=append(Boxlist, E3_3)
	Boxlist=append(Boxlist, E3_4)
	Boxlist=append(Boxlist, E3_5)
	Boxlist=append(Boxlist, E4_1)
	Boxlist=append(Boxlist, E4_2)
	Boxlist=append(Boxlist, E4_3)
	Boxlist=append(Boxlist, E4_4)
	Boxlist=append(Boxlist, E4_5)
	Boxlist=append(Boxlist, E5_1)
	Boxlist=append(Boxlist, E5_2)
	Boxlist=append(Boxlist, E5_3)
	Boxlist=append(Boxlist, E5_4)
	Boxlist=append(Boxlist, E5_5)

	return Boxlist
}

//遗传算法选择输入序列（静态装箱）
//染色体
type chrom struct {
	//箱子种类
	numtype int
	//染色体
	chromosome []int
	//适应度
	fitness float64
}
//初始化生成群体population
func generatePopulation(args []int)[]chrom{
	popsize:=1000
	//染色体长度
	chromlength:=0
	for i:=0;i<len(args);i++{
		chromlength+=args[i]
	}
	//群体pop
	var pop []chrom
	for i:=0;i<popsize;i++{
		var chromosome []int
		t:=copyarr(args)
		//随机生成一个染色体序列
		for j:=0;j<chromlength;j++{
			//随机生成一个数
			chromosome=append(chromosome,randboxid(args,t))
		}
		//染色体
		temp:=chrom{
			numtype:    len(args),
			chromosome: chromosome,
			fitness:    0,
		}
		//染色体加入群体
		pop=append(pop, temp)
	}
	return pop
}
func randnum(arr []int)int{
	//依据各类箱子数量的多寡，生成随机数，多的更容易被选中
	total:=0
	for i:=0;i<len(arr);i++{
		total+=arr[i]
	}
	//r:=realrand(total)
	rand.Seed(time.Now().UnixNano())
	r:=rand.Intn(total)
	for k:=0;k<len(arr);k++{
		r-=arr[k]
		if r<0{
			r=k
			break
		}
	}
	return r
}
func copyarr(src []int)(dst []int){
	dst = make([]int, len(src))
	copy(dst,src)
	return dst
}
func randboxid(args []int,t []int)int{
	//选择一个箱子
	for ;;{
		r:=randnum(args)
		if t[r]>0{
			t[r]-=1
			return r
		}
	}
}
//交叉
func crossover(pop []chrom){
	pc:=0.2
	for i:=0;i<len(pop);i++{
		res,_:= cr.Int(cr.Reader, big.NewInt(100))
		r:=int(res.Int64())
		if float64(r)/100<pc{
			r:=realrand(len(pop))
			if r==i{continue}
			_crossover(pop[i].chromosome,pop[r].chromosome,pop[i].numtype)
		}
	}
}
func _crossover(c1,c2 []int, numtype int){
	arr1:=make([]int,numtype)
	arr2:=make([]int,numtype)
	l:=len(c1)

	res,_:= cr.Int(cr.Reader, big.NewInt(int64(l-1)))
	r:=int(res.Int64())
	pivot :=r+1
	for i:= pivot;i<len(c1);i++{
		arr1[c1[i]]+=1
		arr2[c2[i]]+=1
	}
	for i:=0;i<len(arr1);i++{
		arr1[i]=arr2[i]-arr1[i]
		arr2[i]=-arr1[i]
	}
	//交叉后半部分，出现非法解，修改
	adjustment(c1,arr1,pivot)
	adjustment(c2,arr2,pivot)
	//交叉
	for i:=pivot;i<len(c1);i++{
		t:=c1[i]
		c1[i]=c2[i]
		c2[i]=t
	}
}
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
func getneg(arr []int)int{
	for i:=0;i<len(arr);i++{
		if arr[i]<0{return i}
	}
	return -1
}
//变异
func mutation(pop []chrom){
	pm:=0.01
	for i:=0;i<len(pop);i++{
		if rand.Float64()<pm{
			_mutation(pop[i].chromosome)
		}
	}
}
func _mutation(c []int){
	for i:=0;i<realrand(15)/5+1;i++{
		r1:=realrand(len(c))
		r2:=realrand(len(c))
		t:=c[r1]
		c[r1]=c[r2]
		c[r2]=t
	}
}
//选择
func selection(pop []chrom,boxs []BOX)([]chrom,float64,[]BOX){
	var max=0.0
	var max_path []BOX
	var totalfitness=0.0
	for i:=0;i<len(pop);i++{
		//装箱并获取装填率
		var e float64
		var L_m ,W_m,H_m int=999,999,999
		for _,item :=range boxs{
			if item.L<L_m{L_m=item.L}
			if item.W<W_m{W_m=item.W}
			if item.H<H_m{H_m=item.H}
		}
		s:=SOLUTION{
			Seq:         nil,
			SubCarriage: &BOX{},
			L_min: L_m,
			W_min: W_m,
			H_min: H_m,
		}
		var Car =BOX{L: 587, W: 233, H: 220,next: nil, volume: 587*233*220}
		s.SubCarriage.next=&Car
		for j:=0;j<len(pop[i].chromosome);j++{
			id:=pop[i].chromosome[j]
			s.Select(boxs[id])
		}
		e=s.Evaluate()
		pop[i].fitness=e

		if e>max{
			max=e
			max_path=s.Seq
		}
		//计算适应度和
		totalfitness+=e
	}
	var probability []float64
	for i:=0;i<len(pop);i++{
		probability=append(probability, pop[i].fitness/totalfitness)
	}
	sumsort(probability)
	var newpop []chrom
	for i:=0;i<len(pop);i++{
		r:=float64(realrand(100000))/100000.0
		id:=BinarySearch(probability,r)
		newpop=append(newpop, pop[id])
	}
	return newpop,max,max_path
}
func sumsort(probability []float64){
	for i:=1;i<len(probability);i++{
		probability[i]+=probability[i-1]
	}
}
func BinarySearch(arr []float64,target float64)int{
	left:=0
	right:=len(arr)
	for;left<right;{
		mid:=left+(right-left)/2
		if target>arr[mid]{
			left=mid
		}else{
			right=mid
		}
		if left+1==right{break}
	}
	return left
}
//迭代
func start(arr []int,boxs []BOX){
	pop:=generatePopulation(arr)
	epoch:=100
	//fmt.Println(pop)
	var max float64
	var best_path []BOX
	for i:=0;i<epoch;i++{
		//pop=generatePopulation(arr)
		newpop,bestfitness,path:=selection(pop,boxs)
		if max<bestfitness{
			max=bestfitness
			best_path =path
		}

		pop=newpop
		//交叉
		crossover(pop)
		//变异
		mutation(pop)
	}
	fmt.Println("filling ratio:",max)
	fmt.Println("path:")
	for i:=0;i<len(best_path);i++{
		fmt.Print("{[",best_path[i].L,best_path[i].W,best_path[i].H,"]","(",best_path[i].pos.x,best_path[i].pos.y,best_path[i].pos.z,")}  ")
		if (i+1)%5==0{fmt.Print("\n")}
	}
}
//随机数生成器
func realrand(max int)int{
	res,_:= cr.Int(cr.Reader, big.NewInt(int64(max)))
	r:=int(res.Int64())
	return r
}

func main() {
	boxlist:=loadData()
	for i:=0;i<len(boxlist);i++{
		var arr []int
		for j:=0;j<len(boxlist[i]);j++{
			arr=append(arr, boxlist[i][j].N)
		}
		fmt.Println("\nE",(i)/5+1,"_",i%5+1)
		start(arr,boxlist[i])
	}

}