# -*- coding: utf-8 -*-
"""转换数据 Part1：need_go（Python 源码 → Go），题目 3–138。

结构: CONV1[pid][fname][idx] = {"go": "..."}，idx = 丢弃前代码组序号。
"""

CONV1 = {}

CONV1["3"] = {
    "1.md": {0: {"go": """func lengthOfLongestSubstringKDistinct(s string, k int) int {
	lookup := map[byte]int{}
	start, end, maxLen, counter := 0, 0, 0, 0
	for end < len(s) {
		if lookup[s[end]] == 0 {
			counter++
		}
		lookup[s[end]]++
		end++
		for counter > k {
			if lookup[s[start]] == 1 {
				counter--
			}
			lookup[s[start]]--
			start++
		}
		if end-start > maxLen {
			maxLen = end - start
		}
	}
	return maxLen
}"""}},
}

CONV1["5"] = {
    "Official.md": {0: {"go": """func longestPalindrome(s string) string {
	n := len(s)
	if n < 2 {
		return s
	}
	maxLen, begin := 1, 0
	// dp[i][j] 表示 s[i..j] 是否是回文串
	dp := make([][]bool, n)
	for i := range dp {
		dp[i] = make([]bool, n)
		dp[i][i] = true
	}
	// 递推开始，先枚举子串长度
	for L := 2; L <= n; L++ {
		// 枚举左边界，左边界的上限设置可以宽松一些
		for i := 0; i < n; i++ {
			// 由 L 和 i 可以确定右边界，即 j - i + 1 = L
			j := L + i - 1
			// 如果右边界越界，就可以退出当前循环
			if j >= n {
				break
			}
			if s[i] != s[j] {
				dp[i][j] = false
			} else {
				if j-i < 3 {
					dp[i][j] = true
				} else {
					dp[i][j] = dp[i+1][j-1]
				}
			}
			// 只要 dp[i][j] 为 true，就表示子串 s[i..j] 是回文，此时记录回文长度和起始位置
			if dp[i][j] && j-i+1 > maxLen {
				maxLen = j - i + 1
				begin = i
			}
		}
	}
	return s[begin : begin+maxLen]
}"""}},
}

CONV1["11"] = {
    "1.md": {0: {"go": """func maxArea(height []int) int {
	i, j, res := 0, len(height)-1, 0
	for i < j {
		if height[i] < height[j] {
			if height[i]*(j-i) > res {
				res = height[i] * (j - i)
			}
			i++
		} else {
			if height[j]*(j-i) > res {
				res = height[j] * (j - i)
			}
			j--
		}
	}
	return res
}"""}},
    "Official.md": {0: {"go": """func maxArea(height []int) int {
	l, r, ans := 0, len(height)-1, 0
	for l < r {
		area := min(height[l], height[r]) * (r - l)
		if area > ans {
			ans = area
		}
		if height[l] <= height[r] {
			l++
		} else {
			r--
		}
	}
	return ans
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}"""}},
}

CONV1["15"] = {
    "1.md": {0: {"go": """func threeSum(nums []int) [][]int {
	n := len(nums)
	res := [][]int{}
	if n < 3 {
		return res
	}
	sort.Ints(nums)
	for i := 0; i < n; i++ {
		if nums[i] > 0 {
			return res
		}
		if i > 0 && nums[i] == nums[i-1] {
			continue
		}
		L, R := i+1, n-1
		for L < R {
			if nums[i]+nums[L]+nums[R] == 0 {
				res = append(res, []int{nums[i], nums[L], nums[R]})
				for L < R && nums[L] == nums[L+1] {
					L++
				}
				for L < R && nums[R] == nums[R-1] {
					R--
				}
				L++
				R--
			} else if nums[i]+nums[L]+nums[R] > 0 {
				R--
			} else {
				L++
			}
		}
	}
	return res
}"""}},
}

CONV1["17"] = {
    "1.md": {
        0: {"go": """func letterCombinations(digits string) []string {
	if len(digits) == 0 {
		return []string{}
	}
	// 一个映射表，第二个位置是"abc"，第三个位置是"def"。。。
	// 这里也可以用 map，用数组可以更节省点内存
	d := []string{" ", "*", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}
	res := []string{}
	var dfs func(tmp string, index int)
	dfs = func(tmp string, index int) {
		// 递归的终止条件：index 记录每次遍历到字符串的位置
		if index == len(digits) {
			res = append(res, tmp)
			return
		}
		c := digits[index]
		// 下标从 0 开始一直到 9，c-'0' 获取数字对应的下标，如 '2' 对应下标 2 即 "abc"
		letters := d[c-'0']
		for _, ch := range letters {
			dfs(tmp+string(ch), index+1)
		}
	}
	dfs("", 0)
	return res
}"""},
        1: {"go": """func letterCombinations(digits string) []string {
	if len(digits) == 0 {
		return []string{}
	}
	// 一个映射表，第二个位置是"abc"，第三个位置是"def"。。。
	d := []string{" ", "*", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}
	// 先往队列中加入一个空字符
	res := []string{""}
	for i := 0; i < len(digits); i++ {
		// 由当前遍历到的字符，取字典表中查找对应的字符串
		letters := d[digits[i]-'0']
		size := len(res)
		// 计算出队列长度后，将队列中的每个元素挨个拿出来
		for k := 0; k < size; k++ {
			// 每次都从队列中拿出第一个元素
			tmp := res[0]
			res = res[1:]
			// 然后跟 "abc" 这样的字符串拼接，并再次放到队列中
			for _, j := range letters {
				res = append(res, tmp+string(j))
			}
		}
	}
	return res
}"""},
    },
    "2.md": {0: {"go": """func letterCombinations(digits string) []string {
	if len(digits) == 0 {
		return []string{}
	}
	phone := []string{"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}
	queue := []string{""} // 初始化队列
	for i := 0; i < len(digits); i++ {
		// 这里不使用 int() 转换字符串，使用 ASCII 码：'2' - '2' = 0 对应 "abc"
		letters := phone[digits[i]-'2']
		size := len(queue)
		for k := 0; k < size; k++ {
			tmp := queue[0]
			queue = queue[1:]
			for _, letter := range letters {
				queue = append(queue, tmp+string(letter))
			}
		}
	}
	return queue
}"""}},
}

CONV1["20"] = {
    "1.md": {0: {"go": """func isValid(s string) bool {
	dic := map[byte]byte{'{': '}', '[': ']', '(': ')', '?': '?'}
	stack := []byte{'?'}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if _, ok := dic[c]; ok {
			stack = append(stack, c)
		} else if dic[stack[len(stack)-1]] != c {
			return false
		}
	}
	return len(stack) == 1
}"""}},
    "2.md": {0: {"go": """func isValid(s string) bool {
	dic := map[byte]byte{')': '(', ']': '[', '}': '{'}
	stack := []byte{}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if len(stack) > 0 {
			if _, ok := dic[c]; ok {
				if stack[len(stack)-1] == dic[c] {
					stack = stack[:len(stack)-1]
				} else {
					return false
				}
			} else {
				stack = append(stack, c)
			}
		} else {
			stack = append(stack, c)
		}
	}
	return len(stack) == 0
}"""}},
}

CONV1["21"] = {
    "1.md": {
        0: {"go": """func f(x int) int {
	if x > 0 {
		return x + f(x-1)
	}
	return 0 // f(0) = 0
}"""},
        1: {"go": """func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2 // 终止条件，直到两个链表都空
	}
	if l2 == nil {
		return l1
	}
	if l1.Val <= l2.Val { // 递归调用
		l1.Next = mergeTwoLists(l1.Next, l2)
		return l1
	}
	l2.Next = mergeTwoLists(l1, l2.Next)
	return l2
}"""},
    },
    "Official.md": {
        0: {"go": """func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2
	} else if l2 == nil {
		return l1
	} else if l1.Val < l2.Val {
		l1.Next = mergeTwoLists(l1.Next, l2)
		return l1
	} else {
		l2.Next = mergeTwoLists(l1, l2.Next)
		return l2
	}
}"""},
        1: {"go": """func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
	prehead := &ListNode{Val: -1}
	prev := prehead
	for l1 != nil && l2 != nil {
		if l1.Val <= l2.Val {
			prev.Next = l1
			l1 = l1.Next
		} else {
			prev.Next = l2
			l2 = l2.Next
		}
		prev = prev.Next
	}
	// 合并后 l1 和 l2 最多只有一个还未被合并完，我们直接将链表末尾指向未合并完的链表即可
	if l1 != nil {
		prev.Next = l1
	} else {
		prev.Next = l2
	}
	return prehead.Next
}"""},
    },
}

CONV1["22"] = {
    "1.md": {0: {"go": """func generateParenthesis(n int) []string {
	res := []string{}
	var dfs func(curStr string, left, right, n int)
	dfs = func(curStr string, left, right, n int) {
		if left == n && right == n {
			res = append(res, curStr)
			return
		}
		if left < right {
			return
		}
		if left < n {
			dfs(curStr+"(", left+1, right, n)
		}
		if right < n {
			dfs(curStr+")", left, right+1, n)
		}
	}
	dfs("", 0, 0, n)
	return res
}"""}},
    "2.md": {0: {"go": """func generateParenthesis(n int) []string {
	if n == 0 {
		return []string{}
	}
	totalL := [][]string{}
	totalL = append(totalL, []string{""}) // 0 组括号时记为 ""（相当于 None）
	totalL = append(totalL, []string{"()"}) // 1 组括号只有一种情况
	for i := 2; i <= n; i++ { // 开始计算 i 组括号时的括号组合
		l := []string{}
		for j := 0; j < i; j++ { // 开始遍历 p q ，其中 p+q=i-1 ，j 作为索引
			nowList1 := totalL[j]    // p = j 时的括号组合情况
			nowList2 := totalL[i-1-j] // q = (i-1)-j 时的括号组合情况
			for _, k1 := range nowList1 {
				for _, k2 := range nowList2 {
					el := "(" + k1 + ")" + k2
					l = append(l, el) // 把所有可能的情况添加到 l 中
				}
			}
		}
		totalL = append(totalL, l) // l 这个 list 就是 i 组括号的所有情况
	}
	return totalL[n]
}"""}},
    "Official.md": {
        0: {"go": """func generateParenthesis(n int) []string {
	ans := []string{}
	var generate func(A []byte)
	generate = func(A []byte) {
		if len(A) == 2*n {
			if valid(A) {
				ans = append(ans, string(A))
			}
			return
		}
		A = append(A, '(')
		generate(A)
		A = A[:len(A)-1]
		A = append(A, ')')
		generate(A)
		A = A[:len(A)-1]
	}
	var valid func(A []byte) bool
	valid = func(A []byte) bool {
		bal := 0
		for _, c := range A {
			if c == '(' {
				bal++
			} else {
				bal--
			}
			if bal < 0 {
				return false
			}
		}
		return bal == 0
	}
	generate([]byte{})
	return ans
}"""},
        1: {"go": """func generateParenthesis(n int) []string {
	ans := []string{}
	var backtrack func(S []byte, left, right int)
	backtrack = func(S []byte, left, right int) {
		if len(S) == 2*n {
			ans = append(ans, string(S))
			return
		}
		if left < n {
			S = append(S, '(')
			backtrack(S, left+1, right)
			S = S[:len(S)-1]
		}
		if right < left {
			S = append(S, ')')
			backtrack(S, left, right+1)
			S = S[:len(S)-1]
		}
	}
	backtrack([]byte{}, 0, 0)
	return ans
}"""},
        2: {"go": """func generateParenthesis(n int) []string {
	memo := map[int][]string{}
	var gen func(n int) []string
	gen = func(n int) []string {
		if v, ok := memo[n]; ok {
			return v
		}
		if n == 0 {
			return []string{""}
		}
		ans := []string{}
		for c := 0; c < n; c++ {
			for _, left := range gen(c) {
				for _, right := range gen(n - 1 - c) {
					ans = append(ans, "("+left+")"+right)
				}
			}
		}
		memo[n] = ans
		return ans
	}
	return gen(n)
}"""},
    },
}

CONV1["23"] = {
    "1.md": {
        0: {"go": """type heapNode struct {
	val int
	idx int
}

type minHeap []heapNode

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i].val < h[j].val }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(heapNode)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func mergeKLists(lists []*ListNode) *ListNode {
	dummy := &ListNode{}
	p := dummy
	h := &minHeap{}
	heap.Init(h)
	for i := range lists {
		if lists[i] != nil {
			heap.Push(h, heapNode{lists[i].Val, i})
			lists[i] = lists[i].Next
		}
	}
	for h.Len() > 0 {
		t := heap.Pop(h).(heapNode)
		p.Next = &ListNode{Val: t.val}
		p = p.Next
		if lists[t.idx] != nil {
			heap.Push(h, heapNode{lists[t.idx].Val, t.idx})
			lists[t.idx] = lists[t.idx].Next
		}
	}
	return dummy.Next
}"""},
        1: {"go": """func mergeKLists(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}
	return merge(lists, 0, len(lists)-1)
}

func merge(lists []*ListNode, left, right int) *ListNode {
	if left == right {
		return lists[left]
	}
	mid := left + (right-left)/2
	l1 := merge(lists, left, mid)
	l2 := merge(lists, mid+1, right)
	return mergeTwoLists(l1, l2)
}

func mergeTwoLists(l1, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}
	if l1.Val < l2.Val {
		l1.Next = mergeTwoLists(l1.Next, l2)
		return l1
	}
	l2.Next = mergeTwoLists(l1, l2.Next)
	return l2
}"""},
    },
}

CONV1["33"] = {
    "Official.md": {0: {"go": """func search(nums []int, target int) int {
	if len(nums) == 0 {
		return -1
	}
	l, r := 0, len(nums)-1
	for l <= r {
		mid := (l + r) / 2
		if nums[mid] == target {
			return mid
		}
		if nums[0] <= nums[mid] {
			if nums[0] <= target && target < nums[mid] {
				r = mid - 1
			} else {
				l = mid + 1
			}
		} else {
			if nums[mid] < target && target <= nums[len(nums)-1] {
				l = mid + 1
			} else {
				r = mid - 1
			}
		}
	}
	return -1
}"""}},
}

CONV1["39"] = {
    "1.md": {
        0: {"go": """func combinationSum(candidates []int, target int) [][]int {
	var dfs func(candidates []int, begin, size int, path []int, res *[][]int, target int)
	dfs = func(candidates []int, begin, size int, path []int, res *[][]int, target int) {
		if target < 0 {
			return
		}
		if target == 0 {
			*res = append(*res, append([]int(nil), path...))
			return
		}
		for index := begin; index < size; index++ {
			dfs(candidates, index, size, append(path, candidates[index]), res, target-candidates[index])
		}
	}
	size := len(candidates)
	if size == 0 {
		return [][]int{}
	}
	res := [][]int{}
	dfs(candidates, 0, size, []int{}, &res, target)
	return res
}"""},
        1: {"go": """func combinationSum(candidates []int, target int) [][]int {
	var dfs func(candidates []int, begin, size int, path []int, res *[][]int, target int)
	dfs = func(candidates []int, begin, size int, path []int, res *[][]int, target int) {
		if target == 0 {
			*res = append(*res, append([]int(nil), path...))
			return
		}
		for index := begin; index < size; index++ {
			residue := target - candidates[index]
			if residue < 0 {
				break
			}
			dfs(candidates, index, size, append(path, candidates[index]), res, residue)
		}
	}
	size := len(candidates)
	if size == 0 {
		return [][]int{}
	}
	sort.Ints(candidates)
	res := [][]int{}
	dfs(candidates, 0, size, []int{}, &res, target)
	return res
}"""},
    },
}

CONV1["41"] = {
    "1.md": {0: {"go": """func firstMissingPositive(nums []int) int {
	size := len(nums)
	for i := 0; i < size; i++ {
		// 先判断这个数字是不是索引，然后判断这个数字是不是放在了正确的地方
		for nums[i] >= 1 && nums[i] <= size && nums[i] != nums[nums[i]-1] {
			nums[i], nums[nums[i]-1] = nums[nums[i]-1], nums[i]
		}
	}
	for i := 0; i < size; i++ {
		if i+1 != nums[i] {
			return i + 1
		}
	}
	return size + 1
}"""}},
}

CONV1["46"] = {
    "1.md": {
        0: {"go": """func permute(nums []int) [][]int {
	size := len(nums)
	res := [][]int{}
	if size == 0 {
		return res
	}
	used := make([]bool, size)
	var dfs func(path []int, depth int)
	dfs = func(path []int, depth int) {
		if depth == size {
			res = append(res, append([]int(nil), path...))
			return
		}
		for i := 0; i < size; i++ {
			if !used[i] {
				used[i] = true
				dfs(append(path, nums[i]), depth+1)
				used[i] = false
			}
		}
	}
	dfs([]int{}, 0)
	return res
}"""},
        1: {"go": """func permute(nums []int) [][]int {
	size := len(nums)
	res := [][]int{}
	if size == 0 {
		return res
	}
	var dfs func(path []int, depth, state int)
	dfs = func(path []int, depth, state int) {
		if depth == size {
			res = append(res, append([]int(nil), path...))
			return
		}
		for i := 0; i < size; i++ {
			if (state>>i)&1 == 0 {
				dfs(append(path, nums[i]), depth+1, state^(1<<i))
			}
		}
	}
	dfs([]int{}, 0, 0)
	return res
}"""},
    },
    "Official.md": {0: {"go": """func permute(nums []int) [][]int {
	n := len(nums)
	res := [][]int{}
	var backtrack func(first int)
	backtrack = func(first int) {
		// 所有数都填完了
		if first == n {
			tmp := make([]int, n)
			copy(tmp, nums)
			res = append(res, tmp)
			return
		}
		for i := first; i < n; i++ {
			// 动态维护数组
			nums[first], nums[i] = nums[i], nums[first]
			// 继续递归填下一个数
			backtrack(first + 1)
			// 撤销操作
			nums[first], nums[i] = nums[i], nums[first]
		}
	}
	backtrack(0)
	return res
}"""}},
}

CONV1["48"] = {
    "2.md": {
        0: {"go": """func rotate(matrix [][]int) {
	n := len(matrix)
	// 深拷贝 matrix -> tmp
	tmp := make([][]int, n)
	for i := range tmp {
		tmp[i] = make([]int, n)
		copy(tmp[i], matrix[i])
	}
	// 根据元素旋转公式，遍历修改原矩阵 matrix 的各元素
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			matrix[j][n-1-i] = tmp[i][j]
		}
	}
}"""},
        1: {"go": """func rotate(matrix [][]int) {
	// 设矩阵行列数为 n
	n := len(matrix)
	// 起始点范围为 0 <= i < n / 2 , 0 <= j < (n + 1) / 2
	for i := 0; i < n/2; i++ {
		for j := 0; j < (n+1)/2; j++ {
			// 暂存 A 至 tmp
			tmp := matrix[i][j]
			// 元素旋转操作 A <- D <- C <- B <- tmp
			matrix[i][j] = matrix[n-1-j][i]
			matrix[n-1-j][i] = matrix[n-1-i][n-1-j]
			matrix[n-1-i][n-1-j] = matrix[j][n-1-i]
			matrix[j][n-1-i] = tmp
		}
	}
}"""},
    },
}

CONV1["53"] = {
    "1.md": {
        0: {"go": """func maxSubArray(nums []int) int {
	size := len(nums)
	pre, res := 0, nums[0]
	for i := 0; i < size; i++ {
		if pre+nums[i] > nums[i] {
			pre = pre + nums[i]
		} else {
			pre = nums[i]
		}
		if pre > res {
			res = pre
		}
	}
	return res
}"""},
        1: {"go": """func maxSubArray(nums []int) int {
	size := len(nums)
	if size == 0 {
		return 0
	}
	return maxSubArrayDC(nums, 0, size-1)
}

func maxSubArrayDC(nums []int, left, right int) int {
	if left == right {
		return nums[left]
	}
	mid := (left + right) >> 1
	m1 := maxSubArrayDC(nums, left, mid)
	m2 := maxSubArrayDC(nums, mid+1, right)
	m3 := maxCrossArray(nums, left, mid, right)
	if m1 >= m2 && m1 >= m3 {
		return m1
	}
	if m2 >= m3 {
		return m2
	}
	return m3
}

// 一定包含 nums[mid] 元素的最大连续子数组的和，
// 思路是看看左边"扩散到底"，得到一个最大数，右边"扩散到底"得到一个最大数，然后再加上中间数
func maxCrossArray(nums []int, left, mid, right int) int {
	leftSumMax, s1 := 0, 0
	for i := mid - 1; i >= left; i-- {
		s1 += nums[i]
		if s1 > leftSumMax {
			leftSumMax = s1
		}
	}
	rightSumMax, s2 := 0, 0
	for i := mid + 1; i <= right; i++ {
		s2 += nums[i]
		if s2 > rightSumMax {
			rightSumMax = s2
		}
	}
	return leftSumMax + nums[mid] + rightSumMax
}"""},
    },
}

CONV1["55"] = {
    "Official.md": {0: {"go": """func canJump(nums []int) bool {
	n, rightmost := len(nums), 0
	for i := 0; i < n; i++ {
		if i <= rightmost {
			if i+nums[i] > rightmost {
				rightmost = i + nums[i]
			}
			if rightmost >= n-1 {
				return true
			}
		}
	}
	return false
}"""}},
}

CONV1["56"] = {
    "Official.md": {0: {"go": """func merge(intervals [][]int) [][]int {
	sort.Slice(intervals, func(i, j int) bool { return intervals[i][0] < intervals[j][0] })
	merged := [][]int{}
	for _, interval := range intervals {
		// 如果列表为空，或者当前区间与上一区间不重合，直接添加
		if len(merged) == 0 || merged[len(merged)-1][1] < interval[0] {
			merged = append(merged, interval)
		} else {
			// 否则的话，我们就可以与上一区间进行合并
			if interval[1] > merged[len(merged)-1][1] {
				merged[len(merged)-1][1] = interval[1]
			}
		}
	}
	return merged
}"""}},
}

CONV1["62"] = {
    "1.md": {
        0: {"go": """func uniquePaths(m int, n int) int {
	// 组合数 C(m+n-2, m-1)，用 Gamma 函数实现阶乘：n! = Γ(n+1)
	res := math.Gamma(float64(m+n-1)) / math.Gamma(float64(m)) / math.Gamma(float64(n))
	return int(math.Round(res))
}"""},
        1: {"go": """func uniquePaths(m int, n int) int {
	cur := make([]int, n)
	for i := range cur {
		cur[i] = 1
	}
	for i := 1; i < m; i++ {
		for j := 1; j < n; j++ {
			cur[j] += cur[j-1]
		}
	}
	return cur[n-1]
}"""},
    },
}

CONV1["64"] = {
    "1.md": {0: {"go": """func minPathSum(grid [][]int) int {
	m, n := len(grid), len(grid[0])
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if i == 0 && j == 0 {
				continue
			} else if i == 0 {
				grid[i][j] = grid[i][j-1] + grid[i][j]
			} else if j == 0 {
				grid[i][j] = grid[i-1][j] + grid[i][j]
			} else {
				if grid[i-1][j] < grid[i][j-1] {
					grid[i][j] = grid[i-1][j] + grid[i][j]
				} else {
					grid[i][j] = grid[i][j-1] + grid[i][j]
				}
			}
		}
	}
	return grid[m-1][n-1]
}"""}},
}

CONV1["70"] = {
    "2.md": {0: {"go": """// f(n) 只依赖于 f(n-1) 和 f(n-2)，只需要两项就足够了
func climbStairs(n int) int {
	a, b := 1, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}"""}},
}

CONV1["72"] = {
    "1.md": {0: {"go": """func minDistance(word1 string, word2 string) int {
	memo := map[[2]int]int{}
	var helper func(i, j int) int
	helper = func(i, j int) int {
		if i == len(word1) || j == len(word2) {
			return len(word1) - i + len(word2) - j
		}
		if v, ok := memo[[2]int{i, j}]; ok {
			return v
		}
		var ans int
		if word1[i] == word2[j] {
			ans = helper(i+1, j+1)
		} else {
			inserted := helper(i, j+1)
			deleted := helper(i+1, j)
			replaced := helper(i+1, j+1)
			ans = min(min(inserted, deleted), replaced) + 1
		}
		memo[[2]int{i, j}] = ans
		return ans
	}
	return helper(0, 0)
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}"""}},
    "Official.md": {0: {"go": """func minDistance(word1 string, word2 string) int {
	n, m := len(word1), len(word2)
	// 有一个字符串为空串
	if n*m == 0 {
		return n + m
	}
	// DP 数组
	D := make([][]int, n+1)
	for i := range D {
		D[i] = make([]int, m+1)
		D[i][0] = i
	}
	for j := 0; j <= m; j++ {
		D[0][j] = j
	}
	// 计算所有 DP 值
	for i := 1; i <= n; i++ {
		for j := 1; j <= m; j++ {
			left := D[i-1][j] + 1
			down := D[i][j-1] + 1
			leftDown := D[i-1][j-1]
			if word1[i-1] != word2[j-1] {
				leftDown++
			}
			D[i][j] = min(min(left, down), leftDown)
		}
	}
	return D[n][m]
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}"""}},
}

CONV1["73"] = {
    "1.md": {0: {"go": """func setZeroes(matrix [][]int) {
	flagCol := false
	row, col := len(matrix), len(matrix[0])
	for i := 0; i < row; i++ {
		if matrix[i][0] == 0 {
			flagCol = true
		}
		for j := 1; j < col; j++ {
			if matrix[i][j] == 0 {
				matrix[i][0] = 0
				matrix[0][j] = 0
			}
		}
	}
	for i := row - 1; i >= 0; i-- {
		for j := col - 1; j > 0; j-- {
			if matrix[i][0] == 0 || matrix[0][j] == 0 {
				matrix[i][j] = 0
			}
		}
		if flagCol {
			matrix[i][0] = 0
		}
	}
}"""}},
}

CONV1["74"] = {
    "2.md": {
        0: {"go": """func searchMatrix(matrix [][]int, target int) bool {
	m, n := len(matrix), len(matrix[0])
	l, r := 0, m*n-1
	for l <= r {
		mid := (l + r) >> 1
		x, y := mid/n, mid%n
		if matrix[x][y] > target {
			r = mid - 1
		} else if matrix[x][y] < target {
			l = mid + 1
		} else {
			return true
		}
	}
	return false
}"""},
        1: {"go": """func searchMatrix(matrix [][]int, target int) bool {
	m, n := len(matrix), len(matrix[0])
	x, y := 0, n-1
	for x < m && y >= 0 {
		if matrix[x][y] > target {
			y--
		} else if matrix[x][y] < target {
			x++
		} else {
			return true
		}
	}
	return false
}"""},
    },
}

CONV1["75"] = {
    "1.md": {0: {"go": """// all in [0, zero] = 0
// all in (zero, i) = 1
// all in (two, len - 1] = 2
func sortColors(nums []int) {
	size := len(nums)
	if size < 2 {
		return
	}
	zero, two, i := -1, size-1, 0
	for i <= two {
		if nums[i] == 0 {
			zero++
			nums[i], nums[zero] = nums[zero], nums[i]
			i++
		} else if nums[i] == 1 {
			i++
		} else {
			nums[i], nums[two] = nums[two], nums[i]
			two--
		}
	}
}"""}},
}

CONV1["76"] = {
    "1.md": {0: {"go": """func minWindow(s string, t string) string {
	need := map[byte]int{}
	for i := 0; i < len(t); i++ {
		need[t[i]]++
	}
	needCnt := len(t)
	i, resL, resLen := 0, 0, int(^uint(0)>>1)
	for j := 0; j < len(s); j++ {
		c := s[j]
		if need[c] > 0 {
			needCnt--
		}
		need[c]--
		if needCnt == 0 { // 步骤一：滑动窗口包含了所有 T 元素
			for { // 步骤二：增加 i，排除多余元素
				c2 := s[i]
				if need[c2] == 0 {
					break
				}
				need[c2]++
				i++
			}
			if j-i < resLen { // 记录结果
				resLen = j - i
				resL = i
			}
			need[s[i]]++ // 步骤三：i 增加一个位置，寻找新的满足条件滑动窗口
			needCnt++
			i++
		}
	}
	if resLen == int(^uint(0)>>1) { // 如果 res 始终没被更新过，代表无满足条件的结果
		return ""
	}
	return s[resL : resL+resLen+1]
}"""}},
}

CONV1["78"] = {
    "2.md": {0: {"go": """func combinationSum2(candidates []int, target int) [][]int {
	if len(candidates) == 0 {
		return [][]int{}
	}
	sort.Ints(candidates)
	n := len(candidates)
	res := [][]int{}
	var backtrack func(i, tmpSum int, tmpList []int)
	backtrack = func(i, tmpSum int, tmpList []int) {
		if tmpSum == target {
			res = append(res, append([]int(nil), tmpList...))
			return
		}
		for j := i; j < n; j++ {
			if tmpSum+candidates[j] > target {
				break
			}
			if j > i && candidates[j] == candidates[j-1] {
				continue
			}
			backtrack(j+1, tmpSum+candidates[j], append(tmpList, candidates[j]))
		}
	}
	backtrack(0, 0, []int{})
	return res
}"""}},
}

CONV1["79"] = {
    "1.md": {0: {"go": """var dirs = [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}

func exist(board [][]byte, word string) bool {
	m, n := len(board), len(board[0])
	marked := make([][]bool, m)
	for i := range marked {
		marked[i] = make([]bool, n)
	}
	var search func(i, j int, k int) bool
	search = func(i, j int, k int) bool {
		if board[i][j] != word[k] {
			return false
		}
		if k == len(word)-1 {
			return true
		}
		marked[i][j] = true
		for _, d := range dirs {
			ni, nj := i+d[0], j+d[1]
			if ni >= 0 && ni < m && nj >= 0 && nj < n && !marked[ni][nj] && search(ni, nj, k+1) {
				return true
			}
		}
		marked[i][j] = false
		return false
	}
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if search(i, j, 0) {
				return true
			}
		}
	}
	return false
}"""}},
}

CONV1["84"] = {
    "1.md": {
        0: {"go": """func largestRectangleArea(heights []int) int {
	size := len(heights)
	res := 0
	for i := 0; i < size; i++ {
		left := i
		curHeight := heights[i]
		for left > 0 && heights[left-1] >= curHeight {
			left--
		}
		right := i
		for right < size-1 && heights[right+1] >= curHeight {
			right++
		}
		maxWidth := right - left + 1
		if maxWidth*curHeight > res {
			res = maxWidth * curHeight
		}
	}
	return res
}"""},
        1: {"go": """func largestRectangleArea(heights []int) int {
	size := len(heights)
	res := 0
	heights = append([]int{0}, append(heights, 0)...)
	// 先放入哨兵结点，在循环中就不用做非空判断
	stack := []int{0}
	size += 2
	for i := 1; i < size; i++ {
		for heights[i] < heights[stack[len(stack)-1]] {
			curHeight := heights[stack[len(stack)-1]]
			stack = stack[:len(stack)-1]
			curWidth := i - stack[len(stack)-1] - 1
			if curHeight*curWidth > res {
				res = curHeight * curWidth
			}
		}
		stack = append(stack, i)
	}
	return res
}"""},
    },
}

CONV1["94"] = {
    "1.md": {0: {"go": """const (
	WHITE = 0
	GRAY  = 1
)

type stackItem struct {
	color int
	node  *TreeNode
}

func inorderTraversal(root *TreeNode) []int {
	res := []int{}
	stack := []stackItem{{WHITE, root}}
	for len(stack) > 0 {
		it := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if it.node == nil {
			continue
		}
		if it.color == WHITE {
			stack = append(stack, stackItem{WHITE, it.node.Right})
			stack = append(stack, stackItem{GRAY, it.node})
			stack = append(stack, stackItem{WHITE, it.node.Left})
		} else {
			res = append(res, it.node.Val)
		}
	}
	return res
}"""}},
    "2.md": {
        0: {"go": """func inorderTraversal(root *TreeNode) []int {
	res := []int{}
	var dfs func(root *TreeNode)
	dfs = func(root *TreeNode) {
		if root == nil {
			return
		}
		// 按照 左-打印-右 的方式遍历
		dfs(root.Left)
		res = append(res, root.Val)
		dfs(root.Right)
	}
	dfs(root)
	return res
}"""},
        1: {"go": """func inorderTraversal(root *TreeNode) []int {
	res := []int{}
	stack := []*TreeNode{}
	for len(stack) > 0 || root != nil {
		// 不断往左子树方向走，每走一次就将当前节点保存到栈中
		// 这是模拟递归的调用
		if root != nil {
			stack = append(stack, root)
			root = root.Left
		} else {
			// 当前节点为空，说明左边走到头了，从栈中弹出节点并保存
			// 然后转向右边节点，继续上面整个过程
			tmp := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			res = append(res, tmp.Val)
			root = tmp.Right
		}
	}
	return res
}"""},
        2: {"go": """func inorderTraversal(root *TreeNode) []int {
	res := []int{}
	pre := (*TreeNode)(nil)
	for root != nil {
		// 如果左节点不为空，就将当前节点连带右子树全部挂到
		// 左节点的最右子树下面
		if root.Left != nil {
			pre = root.Left
			for pre.Right != nil {
				pre = pre.Right
			}
			pre.Right = root
			// 将 root 指向 root 的 left
			tmp := root
			root = root.Left
			tmp.Left = nil
		} else {
			// 左子树为空，则打印这个节点，并向右边遍历
			res = append(res, root.Val)
			root = root.Right
		}
	}
	return res
}"""},
    },
}

CONV1["101"] = {
    "1.md": {
        0: {"go": """func isSymmetric(root *TreeNode) bool {
	if root == nil {
		return true
	}
	var dfs func(left, right *TreeNode) bool
	dfs = func(left, right *TreeNode) bool {
		// 递归的终止条件是两个节点都为空
		// 或者两个节点中有一个为空
		// 或者两个节点的值不相等
		if left == nil && right == nil {
			return true
		}
		if left == nil || right == nil {
			return false
		}
		if left.Val != right.Val {
			return false
		}
		return dfs(left.Left, right.Right) && dfs(left.Right, right.Left)
	}
	// 用递归函数，比较左节点，右节点
	return dfs(root.Left, root.Right)
}"""},
        1: {"go": """func isSymmetric(root *TreeNode) bool {
	if root == nil || (root.Left == nil && root.Right == nil) {
		return true
	}
	// 用队列保存节点
	queue := []*TreeNode{root.Left, root.Right}
	for len(queue) > 0 {
		// 从队列中取出两个节点，再比较这两个节点
		left := queue[0]
		right := queue[1]
		queue = queue[2:]
		// 如果两个节点都为空就继续循环，两者有一个为空就返回 false
		if left == nil && right == nil {
			continue
		}
		if left == nil || right == nil {
			return false
		}
		if left.Val != right.Val {
			return false
		}
		// 将左节点的左孩子，右节点的右孩子放入队列
		queue = append(queue, left.Left, right.Right)
		// 将左节点的右孩子，右节点的左孩子放入队列
		queue = append(queue, left.Right, right.Left)
	}
	return true
}"""},
    },
}

CONV1["104"] = {
    "2.md": {
        0: {"go": """func maxDepth(root *TreeNode) int {
	// 节点为空，高度为 0
	if root == nil {
		return 0
	}
	// 递归计算左子树的最大深度
	leftHeight := maxDepth(root.Left)
	// 递归计算右子树的最大深度
	rightHeight := maxDepth(root.Right)
	// 二叉树的最大深度 = 子树的最大深度 + 1（1 是根节点）
	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}"""},
        1: {"go": """func maxDepth(root *TreeNode) int {
	// 节点为空，高度为 0
	if root == nil {
		return 0
	}
	// 递归计算左子树的最大深度
	leftHeight := maxDepth(root.Left)
	// 递归计算右子树的最大深度
	rightHeight := maxDepth(root.Right)
	// 二叉树的最大深度 = 子树的最大深度 + 1（1 是根节点）
	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}"""},
        2: {"go": """func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}
	// 初始化队列
	queue := []*TreeNode{root}
	depth := 0
	// 当队列不为空
	for len(queue) > 0 {
		// 当前层的节点数
		n := len(queue)
		// 弹出当前层的所有节点，并将所有子节点入队列
		for i := 0; i < n; i++ {
			node := queue[0]
			queue = queue[1:]
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		depth++
	}
	// 二叉树最大层次即为二叉树最深深度
	return depth
}"""},
        3: {"go": """func maxDepth(root *TreeNode) int {
	// 空树，高度为 0
	if root == nil {
		return 0
	}
	// 初始化队列和层次
	queue := []*TreeNode{root}
	depth := 0
	// 当队列不为空
	for len(queue) > 0 {
		// 当前层的节点数
		n := len(queue)
		// 弹出当前层的所有节点，并将所有子节点入队列
		for i := 0; i < n; i++ {
			node := queue[0]
			queue = queue[1:]
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		depth++
	}
	// 二叉树最大层次即为二叉树最深深度
	return depth
}"""},
    },
}

CONV1["105"] = {
    "2.md": {0: {"go": """func buildTree(preorder []int, inorder []int) *TreeNode {
	preLen, inLen := len(preorder), len(inorder)
	if preLen != inLen {
		return nil
	}
	var build func(preorder []int, preLeft, preRight int, inorder []int, inLeft, inRight int) *TreeNode
	build = func(preorder []int, preLeft, preRight int, inorder []int, inLeft, inRight int) *TreeNode {
		if preLeft > preRight || inLeft > inRight {
			return nil
		}
		pivot := preorder[preLeft]
		pivotIndex := inLeft
		for inorder[pivotIndex] != pivot {
			pivotIndex++
		}
		root := &TreeNode{Val: pivot}
		root.Left = build(preorder, preLeft+1, preLeft+pivotIndex-inLeft, inorder, inLeft, pivotIndex-1)
		root.Right = build(preorder, preLeft+pivotIndex-inLeft+1, preRight, inorder, pivotIndex+1, inRight)
		return root
	}
	return build(preorder, 0, preLen-1, inorder, 0, inLen-1)
}"""}},
}

CONV1["118"] = {
    "1.md": {0: {"go": """func generate(numRows int) [][]int {
	if numRows == 0 {
		return [][]int{}
	}
	res := [][]int{{1}}
	for len(res) < numRows {
		prev := res[len(res)-1]
		newRow := make([]int, len(prev)+1)
		newRow[0] = 1
		for i := 1; i < len(prev); i++ {
			newRow[i] = prev[i-1] + prev[i]
		}
		newRow[len(prev)] = 1
		res = append(res, newRow)
	}
	return res
}"""}},
}

CONV1["121"] = {
    "Official.md": {
        0: {"go": """// 此方法会超时
func maxProfit(prices []int) int {
	ans := 0
	for i := 0; i < len(prices); i++ {
		for j := i + 1; j < len(prices); j++ {
			if prices[j]-prices[i] > ans {
				ans = prices[j] - prices[i]
			}
		}
	}
	return ans
}"""},
        1: {"go": """func maxProfit(prices []int) int {
	inf := int(1e9)
	minprice := inf
	maxprofit := 0
	for _, price := range prices {
		if price-minprice > maxprofit {
			maxprofit = price - minprice
		}
		if price < minprice {
			minprice = price
		}
	}
	return maxprofit
}"""},
    },
}

CONV1["138"] = {
    "1.md": {
        0: {"go": """func copyRandomList(head *Node) *Node {
	if head == nil {
		return nil
	}
	p := head
	// 第一步，在每个原节点后面创建一个新节点
	// 1->1'->2->2'->3->3'
	for p != nil {
		newNode := &Node{Val: p.Val}
		newNode.Next = p.Next
		p.Next = newNode
		p = newNode.Next
	}
	p = head
	// 第二步，设置新节点的随机节点
	for p != nil {
		if p.Random != nil {
			p.Next.Random = p.Random.Next
		}
		p = p.Next.Next
	}
	// 第三步，将两个链表分离
	p = head
	dummy := &Node{Val: -1}
	cur := dummy
	for p != nil {
		cur.Next = p.Next
		cur = cur.Next
		p.Next = cur.Next
		p = p.Next
	}
	return dummy.Next
}"""},
        1: {"go": """func copyRandomList(head *Node) *Node {
	if head == nil {
		return nil
	}
	// 创建一个哈希表，key 是原节点，value 是新节点
	d := map[*Node]*Node{}
	p := head
	// 将原节点和新节点放入哈希表中
	for p != nil {
		newNode := &Node{Val: p.Val}
		d[p] = newNode
		p = p.Next
	}
	p = head
	// 遍历原链表，设置新节点的 next 和 random
	for p != nil {
		// p 是原节点，d[p] 是对应的新节点，p.Next 是原节点的下一个
		// d[p.Next] 是原节点下一个对应的新节点
		if p.Next != nil {
			d[p].Next = d[p.Next]
		}
		// p.Random 是原节点随机指向，d[p.Random] 是原节点随机指向对应的新节点
		if p.Random != nil {
			d[p].Random = d[p.Random]
		}
		p = p.Next
	}
	// 返回头结点，即原节点对应的 value（新节点）
	return d[head]
}"""},
    },
}
