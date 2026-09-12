# -*- coding: utf-8 -*-
"""转换数据 Part2：need_go（Python 源码 → Go），题目 139–1143。

结构: CONV2[pid][fname][idx] = {"go": "..."}，idx = 丢弃前代码组序号。
"""

CONV2 = {}

CONV2["128"] = {
    "1.md": {0: {"go": """func longestConsecutive(nums []int) int {
	hashDict := map[int]int{}
	maxLength := 0
	for _, num := range nums {
		if _, ok := hashDict[num]; !ok {
			left := hashDict[num-1]
			right := hashDict[num+1]
			curLength := 1 + left + right
			if curLength > maxLength {
				maxLength = curLength
			}
			hashDict[num] = curLength
			hashDict[num-left] = curLength
			hashDict[num+right] = curLength
		}
	}
	return maxLength
}"""}},
}

CONV2["139"] = {
    "2.md": {
        0: {"go": """func wordBreak(s string, wordDict []string) bool {
	wordMap := map[string]bool{}
	for _, w := range wordDict {
		wordMap[w] = true
	}
	n := len(s)
	dp := make([]bool, n+1)
	dp[0] = true
	for i := 0; i < n; i++ {
		for j := i + 1; j <= n; j++ {
			if dp[i] && wordMap[s[i:j]] {
				dp[j] = true
			}
		}
	}
	return dp[n]
}"""},
        1: {"go": """func wordBreak(s string, wordDict []string) bool {
	wordMap := map[string]bool{}
	for _, w := range wordDict {
		wordMap[w] = true
	}
	memo := map[string]bool{}
	var backTrack func(sub string) bool
	backTrack = func(sub string) bool {
		if sub == "" {
			return true
		}
		if v, ok := memo[sub]; ok {
			return v
		}
		res := false
		for i := 1; i <= len(sub); i++ {
			if wordMap[sub[:i]] {
				res = backTrack(sub[i:]) || res
			}
		}
		memo[sub] = res
		return res
	}
	return backTrack(s)
}"""},
    },
}

CONV2["142"] = {
    "1.md": {0: {"go": """func detectCycle(head *ListNode) *ListNode {
	fast, slow := head, head
	for {
		if fast == nil || fast.Next == nil {
			return nil
		}
		fast = fast.Next.Next
		slow = slow.Next
		if fast == slow {
			break
		}
	}
	fast = head
	for fast != slow {
		fast = fast.Next
		slow = slow.Next
	}
	return fast
}"""}},
}

CONV2["146"] = {
    "Official.md": {0: {"go": """type entry struct {
	key   int
	value int
}

type LRUCache struct {
	capacity int
	cache    map[int]*list.Element
	ll       *list.List
}

func Constructor(capacity int) LRUCache {
	return LRUCache{
		capacity: capacity,
		cache:    make(map[int]*list.Element),
		ll:       list.New(),
	}
}

func (this *LRUCache) Get(key int) int {
	if elem, ok := this.cache[key]; ok {
		// 将最近使用的元素移动到末尾
		this.ll.MoveToBack(elem)
		return elem.Value.(*entry).value
	}
	return -1
}

func (this *LRUCache) Put(key int, value int) {
	if elem, ok := this.cache[key]; ok {
		elem.Value.(*entry).value = value
		this.ll.MoveToBack(elem)
		return
	}
	elem := this.ll.PushBack(&entry{key, value})
	this.cache[key] = elem
	if this.ll.Len() > this.capacity {
		// 删除最久未使用的元素（队首）
		front := this.ll.Front()
		this.ll.Remove(front)
		delete(this.cache, front.Value.(*entry).key)
	}
}"""}},
}

CONV2["148"] = {
    "1.md": {
        0: {"go": """func sortList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head // termination.
	}
	// cut the LinkedList at the mid index.
	slow, fast := head, head.Next
	for fast != nil && fast.Next != nil {
		fast = fast.Next.Next
		slow = slow.Next
	}
	mid := slow.Next
	slow.Next = nil // save and cut.
	// recursive for cutting.
	left, right := sortList(head), sortList(mid)
	// merge `left` and `right` linked list and return it.
	h := &ListNode{}
	res := h
	for left != nil && right != nil {
		if left.Val < right.Val {
			h.Next = left
			left = left.Next
		} else {
			h.Next = right
			right = right.Next
		}
		h = h.Next
	}
	if left != nil {
		h.Next = left
	} else {
		h.Next = right
	}
	return res.Next
}"""},
        1: {"go": """func sortList(head *ListNode) *ListNode {
	h, length, intv := head, 0, 1
	for h != nil {
		h = h.Next
		length++
	}
	res := &ListNode{}
	res.Next = head
	// merge the list in different intv.
	for intv < length {
		pre, h := res, res.Next
		for h != nil {
			// get the two merge head `h1`, `h2`
			h1, i := h, intv
			for i > 0 && h != nil {
				h = h.Next
				i--
			}
			if i > 0 {
				break // no need to merge because the `h2` is None.
			}
			h2, i := h, intv
			for i > 0 && h != nil {
				h = h.Next
				i--
			}
			c1, c2 := intv, intv-i // the `c2`: length of `h2` can be smaller than the `intv`.
			// merge the `h1` and `h2`.
			for c1 > 0 && c2 > 0 {
				if h1.Val < h2.Val {
					pre.Next = h1
					h1 = h1.Next
					c1--
				} else {
					pre.Next = h2
					h2 = h2.Next
					c2--
				}
				pre = pre.Next
			}
			if c1 > 0 {
				pre.Next = h1
			} else {
				pre.Next = h2
			}
			for c1 > 0 || c2 > 0 {
				pre = pre.Next
				c1--
				c2--
			}
			pre.Next = h
		}
		intv *= 2
	}
	return res.Next
}"""},
    },
}

CONV2["153"] = {
    "1.md": {0: {"go": """func findMin(nums []int) int {
	left, right := 0, len(nums)-1
	if nums[left] < nums[right] {
		return nums[left]
	}
	for left < right {
		mid := (left + right) >> 1
		if nums[0] > nums[mid] {
			right = mid
		} else {
			left = mid + 1
		}
	}
	return nums[left]
}"""}},
}

CONV2["155"] = {
    "2.md": {0: {"go": """type MinStack struct {
	// stack 中的每个元素为 [值, 当前栈内最小值]
	stack [][2]int
}

func Constructor() MinStack {
	return MinStack{}
}

func (this *MinStack) Push(x int) {
	if len(this.stack) == 0 {
		this.stack = append(this.stack, [2]int{x, x})
	} else {
		curMin := this.stack[len(this.stack)-1][1]
		if x < curMin {
			curMin = x
		}
		this.stack = append(this.stack, [2]int{x, curMin})
	}
}

func (this *MinStack) Pop() {
	this.stack = this.stack[:len(this.stack)-1]
}

func (this *MinStack) Top() int {
	return this.stack[len(this.stack)-1][0]
}

func (this *MinStack) GetMin() int {
	return this.stack[len(this.stack)-1][1]
}"""}},
}

CONV2["160"] = {
    "2.md": {0: {"go": """func getIntersectionNode(headA, headB *ListNode) *ListNode {
	A, B := headA, headB
	for A != B {
		if A == nil {
			A = headB
		} else {
			A = A.Next
		}
		if B == nil {
			B = headA
		} else {
			B = B.Next
		}
	}
	return A
}"""}},
}

CONV2["169"] = {
    "Official.md": {
        0: {"go": """func majorityElement(nums []int) int {
	counts := map[int]int{}
	for _, num := range nums {
		counts[num]++
	}
	majority, maxCount := 0, 0
	for k, v := range counts {
		if v > maxCount {
			majority, maxCount = k, v
		}
	}
	return majority
}"""},
        1: {"go": """func majorityElement(nums []int) int {
	sort.Ints(nums)
	return nums[len(nums)/2]
}"""},
        2: {"go": """func majorityElement(nums []int) int {
	majorityCount := len(nums) / 2
	for {
		candidate := nums[rand.Intn(len(nums))]
		count := 0
		for _, elem := range nums {
			if elem == candidate {
				count++
			}
		}
		if count > majorityCount {
			return candidate
		}
	}
}"""},
        3: {"go": """func majorityElement(nums []int) int {
	var majorityElementRec func(lo, hi int) int
	majorityElementRec = func(lo, hi int) int {
		// base case; the only element in an array of size 1 is the majority
		// element.
		if lo == hi {
			return nums[lo]
		}
		// recurse on left and right halves of this slice.
		mid := (hi-lo)/2 + lo
		left := majorityElementRec(lo, mid)
		right := majorityElementRec(mid+1, hi)
		// if the two halves agree on the majority element, return it.
		if left == right {
			return left
		}
		// otherwise, count each element and return the "winner".
		leftCount := 0
		for i := lo; i <= hi; i++ {
			if nums[i] == left {
				leftCount++
			}
		}
		rightCount := 0
		for i := lo; i <= hi; i++ {
			if nums[i] == right {
				rightCount++
			}
		}
		if leftCount > rightCount {
			return left
		}
		return right
	}
	return majorityElementRec(0, len(nums)-1)
}"""},
        4: {"go": """func majorityElement(nums []int) int {
	count, candidate := 0, 0
	for _, num := range nums {
		if count == 0 {
			candidate = num
		}
		if num == candidate {
			count++
		} else {
			count--
		}
	}
	return candidate
}"""},
    },
}

CONV2["198"] = {
    "1.md": {
        0: {"go": """func rob(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	// 子问题：
	// f(k) = 偷 [0..k) 房间中的最大金额
	// f(0) = 0
	// f(1) = nums[0]
	// f(k) = max{ rob(k-1), nums[k-1] + rob(k-2) }
	N := len(nums)
	dp := make([]int, N+1)
	dp[0] = 0
	dp[1] = nums[0]
	for k := 2; k <= N; k++ {
		if dp[k-1] > nums[k-1]+dp[k-2] {
			dp[k] = dp[k-1]
		} else {
			dp[k] = nums[k-1] + dp[k-2]
		}
	}
	return dp[N]
}"""},
        1: {"go": """func rob(nums []int) int {
	prev, curr := 0, 0
	// 每次循环，计算"偷到当前房子为止的最大金额"
	for _, i := range nums {
		// 循环开始时，curr 表示 dp[k-1]，prev 表示 dp[k-2]
		// dp[k] = max{ dp[k-1], dp[k-2] + i }
		tmp := curr
		if prev+i > curr {
			curr = prev + i
		}
		prev = tmp
		// 循环结束时，curr 表示 dp[k]，prev 表示 dp[k-1]
	}
	return curr
}"""},
    },
}

CONV2["199"] = {
    "Official.md": {
        0: {"go": """func rightSideView(root *TreeNode) []int {
	rightmostValueAtDepth := map[int]int{} // 深度为索引，存放节点的值
	maxDepth := -1
	type item struct {
		node  *TreeNode
		depth int
	}
	stack := []item{{root, 0}}
	for len(stack) > 0 {
		it := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if it.node != nil {
			// 维护二叉树的最大深度
			if it.depth > maxDepth {
				maxDepth = it.depth
			}
			// 如果不存在对应深度的节点我们才插入
			if _, ok := rightmostValueAtDepth[it.depth]; !ok {
				rightmostValueAtDepth[it.depth] = it.node.Val
			}
			stack = append(stack, item{it.node.Left, it.depth + 1})
			stack = append(stack, item{it.node.Right, it.depth + 1})
		}
	}
	res := []int{}
	for depth := 0; depth <= maxDepth; depth++ {
		res = append(res, rightmostValueAtDepth[depth])
	}
	return res
}"""},
        1: {"go": """func rightSideView(root *TreeNode) []int {
	rightmostValueAtDepth := map[int]int{} // 深度为索引，存放节点的值
	maxDepth := -1
	type item struct {
		node  *TreeNode
		depth int
	}
	queue := []item{{root, 0}}
	for len(queue) > 0 {
		it := queue[0]
		queue = queue[1:]
		if it.node != nil {
			// 维护二叉树的最大深度
			if it.depth > maxDepth {
				maxDepth = it.depth
			}
			// 由于每一层最后一个访问到的节点才是我们要的答案，因此不断更新对应深度的信息即可
			rightmostValueAtDepth[it.depth] = it.node.Val
			queue = append(queue, item{it.node.Left, it.depth + 1})
			queue = append(queue, item{it.node.Right, it.depth + 1})
		}
	}
	res := []int{}
	for depth := 0; depth <= maxDepth; depth++ {
		res = append(res, rightmostValueAtDepth[depth])
	}
	return res
}"""},
    },
}

CONV2["206"] = {
    "1.md": {
        0: {"go": """func reverseList(head *ListNode) *ListNode {
	// 申请两个节点，pre 和 cur，pre 指向 nil
	var pre *ListNode
	cur := head
	// 遍历链表
	for cur != nil {
		// 记录当前节点的下一个节点
		tmp := cur.Next
		// 然后将当前节点指向 pre
		cur.Next = pre
		// pre 和 cur 节点都前进一位
		pre = cur
		cur = tmp
	}
	return pre
}"""},
        1: {"go": """func reverseList(head *ListNode) *ListNode {
	// 递归终止条件是当前为空，或者下一个节点为空
	if head == nil || head.Next == nil {
		return head
	}
	// 这里的 cur 就是最后一个节点
	cur := reverseList(head.Next)
	// 这里请配合动画演示理解
	// 如果链表是 1->2->3->4->5，那么此时的 cur 就是 5
	// 而 head 是 4，head 的下一个是 5，下下一个是空
	// 所以 head.Next.Next 就是 5->4
	head.Next.Next = head
	// 防止链表循环，需要将 head.Next 设置为空
	head.Next = nil
	// 每层递归函数都返回 cur，也就是最后一个节点
	return cur
}"""},
    },
}

CONV2["207"] = {
    "2.md": {0: {"go": """func canFinish(numCourses int, prerequisites [][]int) bool {
	var dfs func(i int, adjacency [][]int, flags []int) bool
	dfs = func(i int, adjacency [][]int, flags []int) bool {
		if flags[i] == -1 {
			return true
		}
		if flags[i] == 1 {
			return false
		}
		flags[i] = 1
		for _, j := range adjacency[i] {
			if !dfs(j, adjacency, flags) {
				return false
			}
		}
		flags[i] = -1
		return true
	}
	adjacency := make([][]int, numCourses)
	flags := make([]int, numCourses)
	for _, pre := range prerequisites {
		cur, prev := pre[0], pre[1]
		adjacency[prev] = append(adjacency[prev], cur)
	}
	for i := 0; i < numCourses; i++ {
		if !dfs(i, adjacency, flags) {
			return false
		}
	}
	return true
}"""}},
}

CONV2["215"] = {
    "1.md": {0: {"go": """func findKthLargest(nums []int, k int) int {
	sort.Ints(nums)
	return nums[len(nums)-k]
}"""}},
}

CONV2["226"] = {
    "1.md": {
        0: {"go": """func invertTree(root *TreeNode) *TreeNode {
	// 递归函数的终止条件，节点为空时返回
	if root == nil {
		return nil
	}
	// 将当前节点的左右子树交换
	root.Left, root.Right = root.Right, root.Left
	// 递归交换当前节点的 左子树和右子树
	invertTree(root.Left)
	invertTree(root.Right)
	// 函数返回时就表示当前这个节点，以及它的左右子树都已经交换完了
	return root
}"""},
        1: {"go": """func invertTree(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}
	// 将二叉树中的节点逐层放入队列中，再迭代处理队列中的元素
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		// 每次都从队列中拿一个节点，并交换这个节点的左右子树
		tmp := queue[0]
		queue = queue[1:]
		tmp.Left, tmp.Right = tmp.Right, tmp.Left
		// 如果当前节点的左子树不为空，则放入队列等待后续处理
		if tmp.Left != nil {
			queue = append(queue, tmp.Left)
		}
		// 如果当前节点的右子树不为空，则放入队列等待后续处理
		if tmp.Right != nil {
			queue = append(queue, tmp.Right)
		}
	}
	// 返回处理完的根节点
	return root
}"""},
    },
}

CONV2["230"] = {
    "Official.md": {2: {"go": """// AVLNode 平衡二叉搜索树结点（允许重复值）
type AVLNode struct {
	val               int
	parent, left, right *AVLNode
	height, size      int // 结点高度（叶结点高度是 0）；结点元素数（子树节点总数）
}

type AVL struct {
	root *AVLNode
}

func getHeight(node *AVLNode) int {
	if node == nil {
		return 0
	}
	return node.height
}

func getSize(node *AVLNode) int {
	if node == nil {
		return 0
	}
	return node.size
}

// 重新计算 node 结点的高度和元素数
func recompute(node *AVLNode) {
	node.height = 1 + max(getHeight(node.left), getHeight(node.right))
	node.size = 1 + getSize(node.left) + getSize(node.right)
}

func subtreeFirst(node *AVLNode) *AVLNode {
	for node.left != nil {
		node = node.left
	}
	return node
}

func subtreeLast(node *AVLNode) *AVLNode {
	for node.right != nil {
		node = node.right
	}
	return node
}

// 在以 node 为根结点的子树中搜索值为 v 的结点，如果没有值为 v 的结点，
// 则返回值为 v 的结点应该在的位置的父结点
func subtreeSearch(node *AVLNode, v int) *AVLNode {
	if node.val < v && node.right != nil {
		return subtreeSearch(node.right, v)
	} else if node.val > v && node.left != nil {
		return subtreeSearch(node.left, v)
	}
	return node
}

// 重新连接父结点和子结点（子结点允许为空）
func relink(parent, child *AVLNode, isLeft bool) {
	if isLeft {
		parent.left = child
	} else {
		parent.right = child
	}
	if child != nil {
		child.parent = parent
	}
}

// 旋转操作
func (a *AVL) rotate(node *AVLNode) {
	parent := node.parent
	grandparent := parent.parent
	if grandparent == nil {
		a.root = node
		node.parent = nil
	} else {
		relink(grandparent, node, parent == grandparent.left)
	}
	if node == parent.left {
		relink(parent, node.right, true)
		relink(node, parent, false)
	} else {
		relink(parent, node.left, false)
		relink(node, parent, true)
	}
}

// trinode 操作
func (a *AVL) restructure(node *AVLNode) *AVLNode {
	parent := node.parent
	grandparent := parent.parent
	if (node == parent.right) == (parent == grandparent.right) { // 处理需要一次旋转的情况
		a.rotate(parent)
		return parent
	}
	// 处理需要两次旋转的情况：第 1 次旋转后即成为需要一次旋转的情况
	a.rotate(node)
	a.rotate(node)
	return node
}

func (a *AVL) isBalanced(node *AVLNode) bool {
	diff := getHeight(node.left) - getHeight(node.right)
	if diff < 0 {
		diff = -diff
	}
	return diff <= 1
}

func tallChild(node *AVLNode) *AVLNode {
	if getHeight(node.left) > getHeight(node.right) {
		return node.left
	}
	return node.right
}

// 获取 node 结点更高的子树中的更高的子树
func tallGrandchild(node *AVLNode) *AVLNode {
	return tallChild(tallChild(node))
}

// 从 node 结点开始（含 node 结点）逐个向上重新平衡二叉树，并更新结点高度和元素数
func (a *AVL) rebalance(node *AVLNode) {
	for node != nil {
		oldHeight, oldSize := node.height, node.size
		if !a.isBalanced(node) {
			node = a.restructure(tallGrandchild(node))
			recompute(node.left)
			recompute(node.right)
		}
		recompute(node)
		if node.height == oldHeight && node.size == oldSize {
			node = nil // 如果结点高度和元素数都没有变化则不需要再继续向上调整
		} else {
			node = node.parent
		}
	}
}

// 根据 vals[l:r] 构造平衡二叉搜索树 -> 返回根结点
func buildAVL(a *AVL, vals []int, l, r int, parent *AVLNode) *AVLNode {
	if l > r {
		return nil
	}
	m := (l + r) / 2
	node := &AVLNode{val: vals[m], parent: parent}
	node.left = buildAVL(a, vals, l, m-1, node)
	node.right = buildAVL(a, vals, m+1, r, node)
	recompute(node)
	return node
}

// 插入值为 v 的新结点
func (a *AVL) insert(v int) {
	if a.root == nil {
		a.root = &AVLNode{val: v}
		return
	}
	// 计算新结点的添加位置
	node := subtreeSearch(a.root, v)
	isAddLeft := v <= node.val // 是否将新结点添加到 node 的左子结点
	if node.val == v {         // 如果值为 v 的结点已存在
		if node.left != nil { // 值为 v 的结点存在左子结点，则添加到其左子树的最右侧
			node = subtreeLast(node.left)
			isAddLeft = false
		} else { // 值为 v 的结点不存在左子结点，则添加到其左子结点
			isAddLeft = true
		}
	}
	// 添加新结点
	leaf := &AVLNode{val: v, parent: node}
	if isAddLeft {
		node.left = leaf
	} else {
		node.right = leaf
	}
	a.rebalance(leaf)
}

// 删除值为 v 的结点 -> 返回是否成功删除结点
func (a *AVL) delete(v int) bool {
	if a.root == nil {
		return false
	}
	node := subtreeSearch(a.root, v)
	if node.val != v { // 没有找到需要删除的结点
		return false
	}
	// 处理当前结点既有左子树也有右子树的情况
	// 若左子树比右子树高度低，则将当前结点替换为右子树最左侧的结点，并移除右子树最左侧的结点
	// 若右子树比左子树高度低，则将当前结点替换为左子树最右侧的结点，并移除左子树最右侧的结点
	if node.left != nil && node.right != nil {
		var replacement *AVLNode
		if node.left.height <= node.right.height {
			replacement = subtreeFirst(node.right)
		} else {
			replacement = subtreeLast(node.left)
		}
		node.val = replacement.val
		node = replacement
	}
	parent := node.parent
	a.deleteNode(node)
	a.rebalance(parent)
	return true
}

// 删除结点 p 并用它的子结点代替它，结点 p 至多只能有 1 个子结点
func (a *AVL) deleteNode(node *AVLNode) {
	if node.left != nil && node.right != nil {
		panic("node has two children")
	}
	var child *AVLNode
	if node.left != nil {
		child = node.left
	} else {
		child = node.right
	}
	if child != nil {
		child.parent = node.parent
	}
	if node == a.root {
		a.root = child
	} else {
		parent := node.parent
		if node == parent.left {
			parent.left = child
		} else {
			parent.right = child
		}
	}
	node.parent = node
}

// 返回二叉搜索树中第 k 小的元素
func (a *AVL) kthSmallest(k int) int {
	node := a.root
	for node != nil {
		left := getSize(node.left)
		if left < k-1 {
			node = node.right
			k -= left + 1
		} else if left == k-1 {
			return node.val
		} else {
			node = node.left
		}
	}
	return 0
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// 模拟 1000 次插入和删除操作
func kthSmallest(root *TreeNode, k int) int {
	// 中序遍历生成数值列表
	inorderLst := []int{}
	var inorder func(node *TreeNode)
	inorder = func(node *TreeNode) {
		if node == nil {
			return
		}
		inorder(node.Left)
		inorderLst = append(inorderLst, node.Val)
		inorder(node.Right)
	}
	inorder(root)
	// 构造平衡二叉搜索树
	avl := &AVL{}
	avl.root = buildAVL(avl, inorderLst, 0, len(inorderLst)-1, nil)
	randomNums := make([]int, 1000)
	for i := range randomNums {
		randomNums[i] = rand.Intn(10001)
	}
	for _, num := range randomNums {
		avl.insert(num)
	}
	rand.Shuffle(len(randomNums), func(i, j int) { randomNums[i], randomNums[j] = randomNums[j], randomNums[i] })
	for _, num := range randomNums {
		avl.delete(num)
	}
	return avl.kthSmallest(k)
}"""}},
}

CONV2["236"] = {
    "1.md": {0: {"go": """func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
	if root == nil || root == p || root == q {
		return root
	}
	left := lowestCommonAncestor(root.Left, p, q)
	right := lowestCommonAncestor(root.Right, p, q)
	if left == nil && right == nil {
		return nil // 1.
	}
	if left == nil {
		return right // 3.
	}
	if right == nil {
		return left // 4.
	}
	return root // 2. if left and right
}"""}},
}

CONV2["238"] = {
    "2.md": {0: {"go": """func productExceptSelf(nums []int) []int {
	ans := make([]int, len(nums))
	for i := range ans {
		ans[i] = 1
	}
	tmp := 1
	for i := 1; i < len(nums); i++ {
		ans[i] = ans[i-1] * nums[i-1] // 下三角
	}
	for i := len(nums) - 2; i >= 0; i-- {
		tmp *= nums[i+1] // 上三角
		ans[i] *= tmp    // 下三角 * 上三角
	}
	return ans
}"""}},
}

CONV2["283"] = {
    "1.md": {
        0: {"go": """func moveZeroes(nums []int) {
	if len(nums) == 0 {
		return
	}
	// 第一次遍历的时候，j 指针记录非 0 的个数，只要是非 0 的统统都赋给 nums[j]
	j := 0
	for i := 0; i < len(nums); i++ {
		if nums[i] != 0 {
			nums[j] = nums[i]
			j++
		}
	}
	// 非 0 元素统计完了，剩下的都是 0 了
	// 所以第二次遍历把末尾的元素都赋为 0 即可
	for i := j; i < len(nums); i++ {
		nums[i] = 0
	}
}"""},
        1: {"go": """func moveZeroes(nums []int) {
	if len(nums) == 0 {
		return
	}
	// 两个指针 i 和 j
	j := 0
	for i := 0; i < len(nums); i++ {
		// 当前元素 != 0，就把其交换到左边，等于 0 的交换到右边
		if nums[i] != 0 {
			nums[j], nums[i] = nums[i], nums[j]
			j++
		}
	}
}"""},
    },
}

CONV2["300"] = {
    "1.md": {0: {"go": """func lengthOfLIS(nums []int) int {
	size := len(nums)
	// 特判
	if size < 2 {
		return size
	}
	// tail 数组的定义：长度为 i + 1 的上升子序列的末尾最小是几
	// 遍历第 1 个数，直接放在有序数组 tail 的开头
	tail := []int{nums[0]}
	for i := 1; i < size; i++ {
		// 找到大于等于 num 的第 1 个数，试图让它变小
		left, right := 0, len(tail)
		for left < right {
			// 选左中位数不是偶然，而是有原因的，原因请见 LeetCode 第 35 题题解
			mid := (left + right) >> 1
			if tail[mid] < nums[i] {
				// 中位数肯定不是要找的数，把它写在分支的前面
				left = mid + 1
			} else {
				right = mid
			}
		}
		if left == len(tail) {
			tail = append(tail, nums[i])
		} else {
			// 一定能找到第 1 个大于等于 nums[i] 的元素，因此无需再单独判断，直接更新即可
			tail[left] = nums[i]
		}
	}
	return len(tail)
}"""}},
    "2.md": {0: {"go": """// Dynamic programming + Dichotomy.
func lengthOfLIS(nums []int) int {
	tails := make([]int, len(nums))
	res := 0
	for _, num := range nums {
		i, j := 0, res
		for i < j {
			m := (i + j) / 2
			if tails[m] < num { // 如果要求非严格递增，将此行 '<' 改为 '<=' 即可
				i = m + 1
			} else {
				j = m
			}
		}
		tails[i] = num
		if j == res {
			res++
		}
	}
	return res
}"""}},
    "Official.md": {
        0: {"go": """func lengthOfLIS(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	dp := make([]int, len(nums))
	for i := range nums {
		dp[i] = 1
		for j := 0; j < i; j++ {
			if nums[i] > nums[j] && dp[j]+1 > dp[i] {
				dp[i] = dp[j] + 1
			}
		}
	}
	maxL := 0
	for _, v := range dp {
		if v > maxL {
			maxL = v
		}
	}
	return maxL
}"""},
        1: {"go": """func lengthOfLIS(nums []int) int {
	d := []int{}
	for _, n := range nums {
		if len(d) == 0 || n > d[len(d)-1] {
			d = append(d, n)
		} else {
			l, r := 0, len(d)-1
			loc := r
			for l <= r {
				mid := (l + r) / 2
				if d[mid] >= n {
					loc = mid
					r = mid - 1
				} else {
					l = mid + 1
				}
			}
			d[loc] = n
		}
	}
	return len(d)
}"""},
    },
}

CONV2["322"] = {
    "1.md": {
        0: {"go": """// 初始化 base case
// dp[状态1][状态2][...] = base

// 进行状态转移
// for 状态1 in 状态1的所有取值：
//     for 状态2 in 状态2的所有取值：
//         for ...
//             dp[状态1][状态2][...] = 求最值(选择1，选择2...)
// 例如本题的凑零钱：dp[n] = min(dp[n], 1 + dp[n-coin])"""},
        1: {"go": """func coinChange(coins []int, amount int) int {
	// 备忘录
	memo := map[int]int{}
	var dp func(n int) int
	dp = func(n int) int {
		// 查备忘录，避免重复计算
		if v, ok := memo[n]; ok {
			return v
		}
		// base case
		if n == 0 {
			return 0
		}
		if n < 0 {
			return -1
		}
		res := int(^uint(0) >> 1) // 相当于 float('INF')
		for _, coin := range coins {
			subproblem := dp(n - coin)
			if subproblem == -1 {
				continue
			}
			if 1+subproblem < res {
				res = 1 + subproblem
			}
		}
		// 记入备忘录
		if res == int(^uint(0)>>1) {
			memo[n] = -1
		} else {
			memo[n] = res
		}
		return memo[n]
	}
	return dp(amount)
}"""},
    },
    "Official.md": {
        0: {"go": """func coinChange(coins []int, amount int) int {
	memo := map[int]int{}
	var dp func(rem int) int
	dp = func(rem int) int {
		if rem < 0 {
			return -1
		}
		if rem == 0 {
			return 0
		}
		if v, ok := memo[rem]; ok {
			return v
		}
		mini := int(1e9)
		for _, coin := range coins {
			res := dp(rem - coin)
			if res >= 0 && res < mini {
				mini = res + 1
			}
		}
		if mini < int(1e9) {
			memo[rem] = mini
		} else {
			memo[rem] = -1
		}
		return memo[rem]
	}
	if amount < 1 {
		return 0
	}
	return dp(amount)
}"""},
        1: {"go": """func coinChange(coins []int, amount int) int {
	dp := make([]int, amount+1)
	for i := range dp {
		dp[i] = int(^uint(0) >> 1) // 相当于 float('inf')
	}
	dp[0] = 0
	for _, coin := range coins {
		for x := coin; x <= amount; x++ {
			if dp[x-coin]+1 < dp[x] {
				dp[x] = dp[x-coin] + 1
			}
		}
	}
	if dp[amount] == int(^uint(0)>>1) {
		return -1
	}
	return dp[amount]
}"""},
    },
}

CONV2["394"] = {
    "1.md": {
        0: {"go": """func decodeString(s string) string {
	type item struct {
		multi int
		res   string
	}
	stack := []item{}
	res, multi := "", 0
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c == '[' {
			stack = append(stack, item{multi, res})
			res, multi = "", 0
		} else if c == ']' {
			cur := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			res = cur.res + strings.Repeat(res, cur.multi)
		} else if c >= '0' && c <= '9' {
			multi = multi*10 + int(c-'0')
		} else {
			res += string(c)
		}
	}
	return res
}"""},
        1: {"go": """func decodeString(s string) string {
	var dfs func(s string, i int) (string, int)
	dfs = func(s string, i int) (string, int) {
		res, multi := "", 0
		for i < len(s) {
			if s[i] >= '0' && s[i] <= '9' {
				multi = multi*10 + int(s[i]-'0')
			} else if s[i] == '[' {
				var tmp string
				tmp, i = dfs(s, i+1)
				res += strings.Repeat(tmp, multi)
				multi = 0
			} else if s[i] == ']' {
				return res, i
			} else {
				res += string(s[i])
			}
			i++
		}
		return res, i
	}
	res, _ := dfs(s, 0)
	return res
}"""},
    },
}

CONV2["543"] = {
    "2.md": {0: {"go": """func diameterOfBinaryTree(root *TreeNode) int {
	ans := 1
	var depth func(root *TreeNode) int
	depth = func(root *TreeNode) int {
		if root == nil {
			return 0
		}
		L := depth(root.Left)
		R := depth(root.Right)
		if L+R+1 > ans {
			ans = L + R + 1
		}
		if L > R {
			return L + 1
		}
		return R + 1
	}
	depth(root)
	return ans - 1
}"""}},
    "Official.md": {0: {"go": """func diameterOfBinaryTree(root *TreeNode) int {
	ans := 1
	var depth func(node *TreeNode) int
	depth = func(node *TreeNode) int {
		// 访问到空节点了，返回 0
		if node == nil {
			return 0
		}
		// 左儿子为根的子树的深度
		L := depth(node.Left)
		// 右儿子为根的子树的深度
		R := depth(node.Right)
		// 计算 dNode 即 L+R+1 并更新 ans
		if L+R+1 > ans {
			ans = L + R + 1
		}
		// 返回该节点为根的子树的深度
		if L > R {
			return L + 1
		}
		return R + 1
	}
	depth(root)
	return ans - 1
}"""}},
}

CONV2["763"] = {
    "1.md": {
        0: {"go": """func partitionLabels(S string) []int {
	output := []int{}
	var findLast func(aw byte, S string) int
	findLast = func(aw byte, S string) int {
		for i := len(S) - 1; i >= 0; i-- {
			if S[i] == aw {
				return i
			}
		}
		return 0
	}
	var breakpoint func(startIndex int) int
	breakpoint = func(startIndex int) int {
		aw := S[startIndex]
		last := findLast(aw, S)
		j := startIndex + 1
		for j < last {
			temp := findLast(S[j], S)
			if temp > last {
				last = temp
			}
			j++
		}
		output = append(output, last-startIndex+1)
		return last
	}
	startIndex := 0
	for startIndex < len(S) {
		startIndex = breakpoint(startIndex) + 1
	}
	return output
}"""},
        1: {"go": """func partitionLabels(S string) []int {
	输出答案 := []int{}
	var 找最后 func(一个字母 byte, S string) int
	找最后 = func(一个字母 byte, S string) int {
		for 哎 := len(S) - 1; 哎 >= 0; 哎-- {
			if S[哎] == 一个字母 {
				return 哎
			}
		}
		return 0
	}
	var 查分隔位 func(一段的开始位置 int) int
	查分隔位 = func(一段的开始位置 int) int {
		一个字母 := S[一段的开始位置]
		一段的最后位置 := 找最后(一个字母, S)
		杰 := 一段的开始位置 + 1
		for 杰 < 一段的最后位置 {
			临时 := 找最后(S[杰], S)
			if 临时 > 一段的最后位置 {
				一段的最后位置 = 临时
			}
			杰++
		}
		输出答案 = append(输出答案, 一段的最后位置-一段的开始位置+1)
		return 一段的最后位置
	}
	一段的开始位置 := 0
	for 一段的开始位置 < len(S) {
		一段的开始位置 = 查分隔位(一段的开始位置) + 1
	}
	return 输出答案
}"""},
        2: {"go": """func partitionLabels(S string) []int {
	dic := map[byte]int{}
	for i := 0; i < len(S); i++ {
		dic[S[i]] = i // 存储某个字母对应地最后一个序号
	}
	num := 0 // 直接计数
	result := []int{}
	j := dic[S[0]] // 第一个字符的最后位置
	for i := 0; i < len(S); i++ { // 逐个遍历
		num++ // 找到一个就加 1 个长度
		if dic[S[i]] > j { // 思路一样，如果最后位置比刚才的大，就更新最后位置
			j = dic[S[i]]
		}
		if i == j { // 找到这一段的结束了
			result = append(result, num) // 加入 result
			num = 0                      // 归 0
		}
	}
	return result
}"""},
    },
}

CONV2["994"] = {
    "1.md": {
        0: {"go": """// depth := 0 // 记录遍历到第几层
// for queue 非空 {
//     depth++
//     n := len(queue)
//     循环 n 次:
//         node := queue.pop()
//         for node 的所有相邻结点 m {
//             if m 未访问过 {
//                 queue.push(m)
//             }
//         }
// }"""},
        1: {"go": """func orangesRotting(grid [][]int) int {
	M, N := len(grid), len(grid[0])
	queue := [][2]int{}
	count := 0 // count 表示新鲜橘子的数量
	for r := 0; r < M; r++ {
		for c := 0; c < N; c++ {
			if grid[r][c] == 1 {
				count++
			} else if grid[r][c] == 2 {
				queue = append(queue, [2]int{r, c})
			}
		}
	}
	round := 0 // round 表示腐烂的轮数，或者分钟数
	for count > 0 && len(queue) > 0 {
		round++
		n := len(queue)
		for i := 0; i < n; i++ {
			r, c := queue[0][0], queue[0][1]
			queue = queue[1:]
			if r-1 >= 0 && grid[r-1][c] == 1 {
				grid[r-1][c] = 2
				count--
				queue = append(queue, [2]int{r - 1, c})
			}
			if r+1 < M && grid[r+1][c] == 1 {
				grid[r+1][c] = 2
				count--
				queue = append(queue, [2]int{r + 1, c})
			}
			if c-1 >= 0 && grid[r][c-1] == 1 {
				grid[r][c-1] = 2
				count--
				queue = append(queue, [2]int{r, c - 1})
			}
			if c+1 < N && grid[r][c+1] == 1 {
				grid[r][c+1] = 2
				count--
				queue = append(queue, [2]int{r, c + 1})
			}
		}
	}
	if count > 0 {
		return -1
	}
	return round
}"""},
    },
    "2.md": {
        0: {"go": """// 设初始点为 (i, j)
// dirs := [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} // 上、下、左、右
// for _, d := range dirs {
//     ni, nj := i+d[0], j+d[1]
// }"""},
        1: {"go": """func orangesRotting(grid [][]int) int {
	row, col, time := len(grid), len(grid[0]), 0
	directions := [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	queue := [][3]int{}
	// add the rotten orange to the queue
	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if grid[i][j] == 2 {
				queue = append(queue, [3]int{i, j, time})
			}
		}
	}
	// bfs
	for len(queue) > 0 {
		i, j, time = queue[0][0], queue[0][1], queue[0][2]
		queue = queue[1:]
		for _, d := range directions {
			ni, nj := i+d[0], j+d[1]
			if ni >= 0 && ni < row && nj >= 0 && nj < col && grid[ni][nj] == 1 {
				grid[ni][nj] = 2
				queue = append(queue, [3]int{ni, nj, time + 1})
			}
		}
	}
	// if there are still fresh oranges, return -1
	for _, r := range grid {
		for _, v := range r {
			if v == 1 {
				return -1
			}
		}
	}
	return time
}"""},
    },
    "Official.md": {0: {"go": """func orangesRotting(grid [][]int) int {
	R, C := len(grid), len(grid[0])
	// queue - all starting cells with rotting oranges
	queue := [][3]int{}
	for r := 0; r < R; r++ {
		for c := 0; c < C; c++ {
			if grid[r][c] == 2 {
				queue = append(queue, [3]int{r, c, 0})
			}
		}
	}
	d := 0
	for len(queue) > 0 {
		item := queue[0]
		queue = queue[1:]
		r, c, d = item[0], item[1], item[2]
		nr := [4]int{r - 1, r, r + 1, r}
		nc := [4]int{c, c - 1, c, c + 1}
		for i := 0; i < 4; i++ {
			if nr[i] >= 0 && nr[i] < R && nc[i] >= 0 && nc[i] < C && grid[nr[i]][nc[i]] == 1 {
				grid[nr[i]][nc[i]] = 2
				queue = append(queue, [3]int{nr[i], nc[i], item[2] + 1})
			}
		}
	}
	// if there are still fresh oranges, return -1
	for _, row := range grid {
		for _, v := range row {
			if v == 1 {
				return -1
			}
		}
	}
	return d
}"""}},
}

CONV2["1143"] = {
    "1.md": {
        0: {"go": """func longestCommonSubsequence(text1 string, text2 string) int {
	M, N := len(text1), len(text2)
	dp := make([][]int, M+1)
	for i := range dp {
		dp[i] = make([]int, N+1)
	}
	for i := 1; i <= M; i++ {
		for j := 1; j <= N; j++ {
			if text1[i-1] == text2[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				if dp[i-1][j] > dp[i][j-1] {
					dp[i][j] = dp[i-1][j]
				} else {
					dp[i][j] = dp[i][j-1]
				}
			}
		}
	}
	return dp[M][N]
}"""},
        1: {"go": """// 躲坑：Go 中 make([][]int, M) 只是创建了 M 个 nil 行，
// 必须再对每一行 make([]int, N)，否则访问 dp[i][j] 会越界 panic
// dp := make([][]int, M)
// for i := range dp {
//     dp[i] = make([]int, N)
// }"""},
    },
    "2.md": {
        0: {"go": """func longestCommonSubsequence(str1 string, str2 string) int {
	m, n := len(str1), len(str2)
	// 构建 DP table 和 base case
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}
	// 进行状态转移
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if str1[i-1] == str2[j-1] {
				// 找到一个 lcs 中的字符
				dp[i][j] = 1 + dp[i-1][j-1]
			} else {
				// dp[i][j] = max(dp[i-1][j], dp[i][j-1])
				if dp[i-1][j] > dp[i][j-1] {
					dp[i][j] = dp[i-1][j]
				} else {
					dp[i][j] = dp[i][j-1]
				}
			}
		}
	}
	return dp[m][n]
}"""},
        1: {"go": """// 疑难解答：dp[i][j] = max(dp[i-1][j], dp[i][j-1]) 已经足够，
// 无需再与 dp[i-1][j-1] 比较 —— dp[i-1][j-1] + 1 的情况
// 一定包含在 max(dp[i-1][j], dp[i][j-1]) 的取值之中
// if str1[i-1] == str2[j-1] {
//     dp[i][j] = 1 + dp[i-1][j-1]
// } else {
//     dp[i][j] = max(dp[i-1][j], dp[i][j-1])
// }"""},
    },
}
