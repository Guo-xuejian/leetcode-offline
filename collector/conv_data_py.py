# -*- coding: utf-8 -*-
"""转换数据 Part3：need_py（Go 源码 → Python），共 66 条。

结构: CONVPY[pid][fname][idx] = {"python": "..."}，idx = 丢弃前代码组序号。
"""

CONVPY = {}

CONVPY["2"] = {
    "Official.md": {0: {"python": """class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = tail = None
        carry = 0
        while l1 is not None or l2 is not None:
            n1, n2 = 0, 0
            if l1 is not None:
                n1 = l1.val
                l1 = l1.next
            if l2 is not None:
                n2 = l2.val
                l2 = l2.next
            s = n1 + n2 + carry
            s, carry = s % 10, s // 10
            if head is None:
                head = ListNode(s)
                tail = head
            else:
                tail.next = ListNode(s)
                tail = tail.next
        if carry > 0:
            tail.next = ListNode(carry)
        return head"""}},
}

CONVPY["31"] = {
    "1.md": {0: {"python": """class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        if len(nums) <= 1:
            return
        i, j, k = len(nums) - 2, len(nums) - 1, len(nums) - 1

        # find: A[i]<A[j]
        while i >= 0 and nums[i] >= nums[j]:
            i -= 1
            j -= 1

        if i >= 0:  # 不是最后一个排列
            # find: A[i]<A[k]
            while nums[i] >= nums[k]:
                k -= 1
            # swap A[i], A[k]
            nums[i], nums[k] = nums[k], nums[i]

        # reverse A[j:end]
        i, j = j, len(nums) - 1
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1"""}},
}

CONVPY["32"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        maxAns = 0
        dp = [0] * len(s)
        for i in range(1, len(s)):
            if s[i] == ')':
                if s[i - 1] == '(':
                    dp[i] = dp[i - 2] + 2 if i >= 2 else 2
                elif i - dp[i - 1] > 0 and s[i - dp[i - 1] - 1] == '(':
                    if i - dp[i - 1] >= 2:
                        dp[i] = dp[i - 1] + dp[i - dp[i - 1] - 2] + 2
                    else:
                        dp[i] = dp[i - 1] + 2
                maxAns = max(maxAns, dp[i])
        return maxAns"""},
        1: {"python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        maxAns = 0
        stack = [-1]
        for i in range(len(s)):
            if s[i] == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    maxAns = max(maxAns, i - stack[-1])
        return maxAns"""},
        2: {"python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        left, right, maxLength = 0, 0, 0
        for i in range(len(s)):
            if s[i] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                maxLength = max(maxLength, 2 * right)
            elif right > left:
                left, right = 0, 0
        left, right = 0, 0
        for i in range(len(s) - 1, -1, -1):
            if s[i] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                maxLength = max(maxLength, 2 * left)
            elif left > right:
                left, right = 0, 0
        return maxLength"""},
    },
}

CONVPY["34"] = {
    "Official.md": {0: {"python": """class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        leftmost = bisect_left(nums, target)
        if leftmost == len(nums) or nums[leftmost] != target:
            return [-1, -1]
        rightmost = bisect_left(nums, target + 1) - 1
        return [leftmost, rightmost]"""}},
}

CONVPY["35"] = {
    "Official.md": {0: {"python": """class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1
        ans = n
        while left <= right:
            mid = (right - left) >> 1 + left
            if target <= nums[mid]:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        return ans"""}},
}

CONVPY["39"] = {
    "Official.md": {0: {"python": """class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(target: int, idx: int) -> None:
            if idx == len(candidates):
                return
            if target == 0:
                ans.append(comb[:])
                return
            # 直接跳过
            dfs(target, idx + 1)
            # 选择当前数
            if target - candidates[idx] >= 0:
                comb.append(candidates[idx])
                dfs(target - candidates[idx], idx)
                comb.pop()

        ans, comb = [], []
        dfs(target, 0)
        return ans"""}},
}

CONVPY["45"] = {
    "Official.md": {0: {"python": """class Solution:
    def jump(self, nums: List[int]) -> int:
        position = len(nums) - 1
        steps = 0
        while position > 0:
            for i in range(position):
                if i + nums[i] >= position:
                    position = i
                    steps += 1
                    break
        return steps"""}},
}

CONVPY["53"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_ = nums[0]
        for i in range(1, len(nums)):
            if nums[i] + nums[i - 1] > nums[i]:
                nums[i] += nums[i - 1]
            if nums[i] > max_:
                max_ = nums[i]
        return max_"""},
        1: {"python": """class Status:
    def __init__(self, lSum: int, rSum: int, mSum: int, iSum: int):
        self.lSum = lSum
        self.rSum = rSum
        self.mSum = mSum
        self.iSum = iSum


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        return self.get(nums, 0, len(nums) - 1).mSum

    def pushUp(self, l: Status, r: Status) -> Status:
        iSum = l.iSum + r.iSum
        lSum = max(l.lSum, l.iSum + r.lSum)
        rSum = max(r.rSum, r.iSum + l.rSum)
        mSum = max(max(l.mSum, r.mSum), l.rSum + r.lSum)
        return Status(lSum, rSum, mSum, iSum)

    def get(self, nums: List[int], l: int, r: int) -> Status:
        if l == r:
            return Status(nums[l], nums[l], nums[l], nums[l])
        m = (l + r) >> 1
        lSub = self.get(nums, l, m)
        rSub = self.get(nums, m + 1, r)
        return self.pushUp(lSub, rSub)"""},
    },
}

CONVPY["70"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def climbStairs(self, n: int) -> int:
        p, q, r = 0, 0, 1
        for i in range(1, n + 1):
            p = q
            q = r
            r = p + q
        return r"""},
        1: {"python": """class Solution:
    def climbStairs(self, n: int) -> int:
        def mul(a, b):
            c = [[0] * 2 for _ in range(2)]
            for i in range(2):
                for j in range(2):
                    c[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j]
            return c

        def pow_(a, n):
            res = [[1, 0], [0, 1]]
            while n > 0:
                if n & 1 == 1:
                    res = mul(res, a)
                a = mul(a, a)
                n >>= 1
            return res

        return pow_([[1, 1], [1, 0]], n)[0][0]"""},
        2: {"python": """class Solution:
    def climbStairs(self, n: int) -> int:
        sqrt5 = math.sqrt(5)
        pow1 = ((1 + sqrt5) / 2) ** (n + 1)
        pow2 = ((1 - sqrt5) / 2) ** (n + 1)
        return int(round((pow1 - pow2) / sqrt5))"""},
    },
}

CONVPY["74"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row = bisect_right([r[0] for r in matrix], target) - 1
        if row < 0:
            return False
        col = bisect_left(matrix[row], target)
        return col < len(matrix[row]) and matrix[row][col] == target"""},
        1: {"python": """class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        i = bisect_left([matrix[x // n][x % n] for x in range(m * n)], target)
        return i < m * n and matrix[i // n][i % n] == target"""},
    },
}

CONVPY["76"] = {
    "Official.md": {0: {"python": """class Solution:
    def minWindow(self, s: str, t: str) -> str:
        ori, cnt = {}, {}
        for c in t:
            ori[c] = ori.get(c, 0) + 1
        sLen = len(s)
        ansL, ansR = -1, -1
        length = float('inf')

        def check() -> bool:
            for k, v in ori.items():
                if cnt.get(k, 0) < v:
                    return False
            return True

        l = 0
        for r in range(sLen):
            if ori.get(s[r], 0) > 0:
                cnt[s[r]] = cnt.get(s[r], 0) + 1
            while check() and l <= r:
                if r - l + 1 < length:
                    length = r - l + 1
                    ansL, ansR = l, l + length
                if s[l] in ori:
                    cnt[s[l]] -= 1
                l += 1
        if ansL == -1:
            return ""
        return s[ansL:ansR]"""}},
}

CONVPY["78"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        for mask in range(1 << n):
            t = []
            for i in range(n):
                if mask >> i & 1:
                    t.append(nums[i])
            ans.append(t)
        return ans"""},
        1: {"python": """class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans, t = [], []

        def dfs(cur: int) -> None:
            if cur == len(nums):
                ans.append(t[:])
                return
            t.append(nums[cur])
            dfs(cur + 1)
            t.pop()
            dfs(cur + 1)

        dfs(0)
        return ans"""},
    },
}

CONVPY["94"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        res = []

        def inorder(node: TreeNode) -> None:
            if node is None:
                return
            inorder(node.left)
            res.append(node.val)
            inorder(node.right)

        inorder(root)
        return res"""},
        1: {"python": """class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        res = []
        stack = []
        while root is not None or stack:
            while root is not None:
                stack.append(root)
                root = root.left
            root = stack.pop()
            res.append(root.val)
            root = root.right
        return res"""},
        2: {"python": """class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        res = []
        while root is not None:
            if root.left is not None:
                # predecessor 节点就是当前 root 节点向左走一步，然后一直向右走至无法走为止
                predecessor = root.left
                while predecessor.right is not None and predecessor.right != root:
                    predecessor = predecessor.right
                # 让 predecessor 的右指针指向 root，继续遍历左子树
                if predecessor.right is None:
                    predecessor.right = root
                    root = root.left
                else:  # 说明左子树已经访问完了，我们需要断开链接
                    res.append(root.val)
                    predecessor.right = None
                    root = root.right
            else:  # 如果没有左孩子，则直接访问右孩子
                res.append(root.val)
                root = root.right
        return res"""},
    },
}

CONVPY["101"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def check(p: TreeNode, q: TreeNode) -> bool:
            if p is None and q is None:
                return True
            if p is None or q is None:
                return False
            return p.val == q.val and check(p.left, q.right) and check(p.right, q.left)

        return check(root, root)"""},
        1: {"python": """class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        u, v = root, root
        queue = [u, v]
        while queue:
            u, v = queue.pop(0), queue.pop(0)
            if u is None and v is None:
                continue
            if u is None or v is None:
                return False
            if u.val != v.val:
                return False
            queue.append(u.left)
            queue.append(v.right)
            queue.append(u.right)
            queue.append(v.left)
        return True"""},
    },
}

CONVPY["102"] = {
    "Official.md": {0: {"python": """class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        ret = []
        if root is None:
            return ret
        q = [root]
        i = 0
        while q:
            ret.append([])
            p = []
            for node in q:
                ret[i].append(node.val)
                if node.left is not None:
                    p.append(node.left)
                if node.right is not None:
                    p.append(node.right)
            q = p
            i += 1
        return ret"""}},
}

CONVPY["104"] = {
    "Official.md": {1: {"python": """class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if root is None:
            return 0
        queue = [root]
        ans = 0
        while queue:
            sz = len(queue)
            while sz > 0:
                node = queue.pop(0)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
                sz -= 1
            ans += 1
        return ans"""}},
}

CONVPY["124"] = {
    "1.md": {0: {"python": """class Solution:
    def __init__(self):
        self.max = float('-inf')

    def maxPathSum(self, root: TreeNode) -> int:
        self.find(root)
        return self.max

    def find(self, root: TreeNode) -> int:
        if root is None:
            return 0
        l = self.find(root.left)
        r = self.find(root.right)
        s = l + r + root.val
        if s > self.max:
            self.max = s
        temp = l if l > r else r
        return temp + root.val if temp + root.val > 0 else 0"""}},
}

CONVPY["138"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        self.cacheNode = {}
        return self.deepCopy(head)

    def deepCopy(self, node: 'Node') -> 'Node':
        if node is None:
            return None
        if node in self.cacheNode:
            return self.cacheNode[node]
        newNode = Node(node.val)
        self.cacheNode[node] = newNode
        newNode.next = self.deepCopy(node.next)
        newNode.random = self.deepCopy(node.random)
        return newNode"""},
        1: {"python": """class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if head is None:
            return None
        # 第一步：在原链表的每个节点后面拷贝出一个新的节点
        node = head
        while node is not None:
            node.next = Node(node.val, node.next)
            node = node.next.next
        # 第二步：给拷贝节点的 random 赋值
        node = head
        while node is not None:
            if node.random is not None:
                node.next.random = node.random.next
            node = node.next.next
        # 第三步：拆分链表
        headNew = head.next
        node = head
        while node is not None:
            nodeNew = node.next
            node.next = node.next.next
            if nodeNew.next is not None:
                nodeNew.next = nodeNew.next.next
            node = node.next
        return headNew"""},
    },
}

CONVPY["139"] = {
    "1.md": {
        0: {"python": """def canBreak(start: int, s: str, wordMap: dict) -> bool:
    if start == len(s):
        return True

    for i in range(start + 1, len(s) + 1):
        prefix = s[start:i]
        if prefix in wordMap and canBreak(i, s, wordMap):
            return True

    return False


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        wordMap = {w: True for w in wordDict}
        return canBreak(0, s, wordMap)"""},
        1: {"python": """def canBreak(start: int, s: str, wordMap: dict, memo: dict) -> bool:
    if start == len(s):
        return True

    if start in memo:
        return memo[start]

    for i in range(start + 1, len(s) + 1):
        prefix = s[start:i]
        if prefix in wordMap and canBreak(i, s, wordMap, memo):
            memo[start] = True
            return True

    memo[start] = False
    return False


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        wordMap = {w: True for w in wordDict}
        memo = {}
        return canBreak(0, s, wordMap, memo)"""},
        2: {"python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        l = len(s)
        wordMap = {v: True for v in wordDict}
        queue = [0]
        while queue:
            index = queue.pop(0)
            if index == l:
                return True
            for i in range(index + 1, l + 1):
                if s[index:i] in wordMap:
                    queue.append(i)
        return False"""},
        3: {"python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        l = len(s)
        wordMap = {v: True for v in wordDict}
        visited = [False] * (l + 1)  # 记录已经访问过的位置，避免重复
        queue = [0]
        while queue:
            index = queue.pop(0)
            if index == l:
                return True
            if visited[index]:
                continue
            visited[index] = True
            for i in range(index + 1, l + 1):
                if s[index:i] in wordMap:
                    queue.append(i)
        return False"""},
        4: {"python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        l = len(s)
        wordMap = {v: True for v in wordDict}
        dp = [False] * (l + 1)
        dp[0] = True
        for i in range(l):
            for j in range(i + 1, l + 1):
                if dp[i] and s[i:j] in wordMap:
                    dp[j] = True
        return dp[l]"""},
        5: {"python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        wordMap = {v: True for v in wordDict}
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in wordMap:
                    dp[i] = True
                    break
        return dp[len(s)]"""},
    },
    "Official.md": {0: {"python": """class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        wordDictSet = {w: True for w in wordDict}
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in wordDictSet:
                    dp[i] = True
                    break
        return dp[len(s)]"""}},
}

CONVPY["142"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        seen = set()
        while head is not None:
            if head in seen:
                return head
            seen.add(head)
            head = head.next
        return None"""},
        1: {"python": """class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        slow, fast = head, head
        while fast is not None:
            slow = slow.next
            if fast.next is None:
                return None
            fast = fast.next.next
            if fast == slow:
                p = head
                while p != slow:
                    p = p.next
                    slow = slow.next
                return p
        return None"""},
    },
}

CONVPY["152"] = {
    "Official.md": {0: {"python": """class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        maxF, minF, ans = nums[0], nums[0], nums[0]
        for i in range(1, len(nums)):
            mx, mn = maxF, minF
            maxF = max(mx * nums[i], nums[i], mn * nums[i])
            minF = min(mn * nums[i], nums[i], mx * nums[i])
            ans = max(maxF, ans)
        return ans"""}},
}

CONVPY["160"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        seen = set()
        while headA is not None:
            seen.add(headA)
            headA = headA.next
        while headB is not None:
            if headB in seen:
                return headB
            headB = headB.next
        return None"""},
        1: {"python": """class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        if headA is None or headB is None:
            return None
        pA, pB = headA, headB
        while pA != pB:
            pA = pA.next if pA is not None else headB
            pB = pB.next if pB is not None else headA
        return pA"""},
    },
}

CONVPY["189"] = {
    "1.md": {0: {"python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        k %= len(nums)
        self.reverse(nums, 0, len(nums) - 1)
        self.reverse(nums, 0, k - 1)
        self.reverse(nums, k, len(nums) - 1)

    def reverse(self, nums: List[int], l: int, r: int) -> None:
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1"""}},
    "Official.md": {
        0: {"python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        newNums = [0] * n
        for i, v in enumerate(nums):
            newNums[(i + k) % n] = v
        nums[:] = newNums"""},
        1: {"python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        count = 0
        start = 0
        while count < n:
            pre = nums[start]
            cur = start
            while True:
                nxt = (cur + k) % n
                nums[nxt], pre = pre, nums[nxt]
                cur = nxt
                count += 1
                if cur == start:
                    break
            start += 1"""},
        2: {"python": """class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        def reverse(i: int, j: int) -> None:
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        n = len(nums)
        k %= n
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)"""},
    },
}

CONVPY["206"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev"""},
        1: {"python": """class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if head is None or head.next is None:
            return head
        newHead = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return newHead"""},
    },
}

CONVPY["215"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return self.quickSelect(nums, 0, len(nums) - 1, len(nums) - k)

    def quickSelect(self, a: List[int], l: int, r: int, index: int) -> int:
        q = self.partition(a, l, r)
        if q == index:
            return a[q]
        elif q < index:
            return self.quickSelect(a, q + 1, r, index)
        return self.quickSelect(a, l, q - 1, index)

    def partition(self, a: List[int], l: int, r: int) -> int:
        x = a[r]
        i = l - 1
        for j in range(l, r):
            if a[j] <= x:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[r] = a[r], a[i + 1]
        return i + 1"""},
        1: {"python": """class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heapSize = len(nums)
        self.buildMaxHeap(nums, heapSize)
        for i in range(len(nums) - 1, len(nums) - k, -1):
            nums[0], nums[i] = nums[i], nums[0]
            heapSize -= 1
            self.maxHeapify(nums, 0, heapSize)
        return nums[0]

    def buildMaxHeap(self, a: List[int], heapSize: int) -> None:
        for i in range(heapSize // 2, -1, -1):
            self.maxHeapify(a, i, heapSize)

    def maxHeapify(self, a: List[int], i: int, heapSize: int) -> None:
        l, r, largest = i * 2 + 1, i * 2 + 2, i
        if l < heapSize and a[l] > a[largest]:
            largest = l
        if r < heapSize and a[r] > a[largest]:
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            self.maxHeapify(a, largest, heapSize)"""},
    },
}

CONVPY["236"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None:
            return None
        if root.val == p.val or root.val == q.val:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left is not None and right is not None:
            return root
        if left is None:
            return right
        return left"""},
        1: {"python": """class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        parent, visited = {}, set()

        def dfs(r: 'TreeNode') -> None:
            if r is None:
                return
            if r.left is not None:
                parent[r.left.val] = r
                dfs(r.left)
            if r.right is not None:
                parent[r.right.val] = r
                dfs(r.right)

        dfs(root)
        while p is not None:
            visited.add(p.val)
            p = parent.get(p.val)
        while q is not None:
            if q.val in visited:
                return q
            q = parent.get(q.val)
        return None"""},
    },
}

CONVPY["279"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def numSquares(self, n: int) -> int:
        f = [0] * (n + 1)
        for i in range(1, n + 1):
            minn = float('inf')
            j = 1
            while j * j <= i:
                minn = min(minn, f[i - j * j])
                j += 1
            f[i] = minn + 1
        return f[n]"""},
        1: {"python": """class Solution:
    def numSquares(self, n: int) -> int:
        if n <= 0:
            return 0
        marked = [False] * (n + 1)
        marked[n] = True
        queue = [n]
        level = 0
        while queue:
            level += 1
            size = len(queue)
            for _ in range(size):
                num = queue.pop(0)
                j = 1
                while j * j <= num:
                    nxt = num - j * j
                    if nxt == 0:
                        return level
                    if not marked[nxt]:
                        queue.append(nxt)
                        marked[nxt] = True
                    j += 1
        return -1"""},
    },
}

CONVPY["287"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        n = len(nums)
        l, r = 1, n - 1
        ans = -1
        while l <= r:
            mid = (l + r) >> 1
            cnt = 0
            for i in range(n):
                if nums[i] <= mid:
                    cnt += 1
            if cnt <= mid:
                l = mid + 1
            else:
                r = mid - 1
                ans = mid
        return ans"""},
        1: {"python": """class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        bitMax = 31
        while (n - 1) >> bitMax == 0:
            bitMax -= 1
        for bit in range(bitMax + 1):
            x = y = 0
            for i in range(n):
                if nums[i] & (1 << bit) > 0:
                    x += 1
                if i >= 1 and i & (1 << bit) > 0:
                    y += 1
            if x > y:
                ans |= 1 << bit
        return ans"""},
        2: {"python": """class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        slow = nums[slow]
        fast = nums[nums[fast]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow"""},
    },
}

CONVPY["347"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        res = []
        # 建立哈希表统计频率
        mapNum = {}
        for item in nums:
            mapNum[item] = mapNum.get(item, 0) + 1
        # 建立桶：下标为频率，值为对应数字列表
        buckets = [[] for _ in range(len(nums) + 1)]
        for key, value in mapNum.items():
            buckets[value].append(key)
        # 倒序遍历桶
        for i in range(len(buckets) - 1, -1, -1):
            res.extend(buckets[i])
            if len(res) >= k:
                break
        return res[:k]"""},
        1: {"python": """class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        mapNum = {}
        for item in nums:
            mapNum[item] = mapNum.get(item, 0) + 1
        h = []  # 小顶堆，元素为 (频率, 数字)
        for key, value in mapNum.items():
            heapq.heappush(h, (value, key))
            if len(h) > k:
                heapq.heappop(h)
        res = [0] * k
        for i in range(k - 1, -1, -1):
            res[i] = heapq.heappop(h)[1]
        return res"""},
    },
}

CONVPY["394"] = {
    "Official.md": {
        0: {"python": """class Solution:
    def decodeString(self, s: str) -> str:
        # 初始化栈，存字符串和重复次数
        stack = []
        res = ""
        multi = 0
        for c in s:
            if c == '[':
                stack.append((multi, res))
                res, multi = "", 0
            elif c == ']':
                cur_multi, last_res = stack.pop()
                res = last_res + cur_multi * res
            elif '0' <= c <= '9':
                multi = multi * 10 + int(c)
            else:
                res += c
        return res"""},
        1: {"python": """class Solution:
    def decodeString(self, s: str) -> str:
        def dfs(s: str, i: int):
            res = ""
            multi = 0
            while i < len(s):
                if '0' <= s[i] <= '9':
                    multi = multi * 10 + int(s[i])
                elif s[i] == '[':
                    tmp, i = dfs(s, i + 1)
                    res += multi * tmp
                    multi = 0
                elif s[i] == ']':
                    return res, i
                else:
                    res += s[i]
                i += 1
            return res, i

        res, _ = dfs(s, 0)
        return res"""},
    },
}

CONVPY["560"] = {
    "1.md": {
        0: {"python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                sum_ = 0
                for q in range(i, j + 1):
                    sum_ += nums[q]
                if sum_ == k:
                    count += 1
        return count"""},
        1: {"python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            sum_ = 0
            for j in range(i, len(nums)):
                sum_ += nums[j]
                if sum_ == k:
                    count += 1
        return count"""},
        2: {"python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        hash_ = {0: 1}
        preSum = 0
        for i in range(len(nums)):
            preSum += nums[i]
            if hash_.get(preSum - k, 0) > 0:
                count += hash_[preSum - k]
            hash_[preSum] = hash_.get(preSum, 0) + 1
        return count"""},
    },
    "Official.md": {
        0: {"python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        for start in range(len(nums)):
            sum_ = 0
            for end in range(start, -1, -1):
                sum_ += nums[end]
                if sum_ == k:
                    count += 1
        return count"""},
        1: {"python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count, pre = 0, 0
        m = {0: 1}
        for i in range(len(nums)):
            pre += nums[i]
            if pre - k in m:
                count += m[pre - k]
            m[pre] = m.get(pre, 0) + 1
        return count"""},
    },
}

CONVPY["763"] = {
    "2.md": {0: {"python": """class Solution:
    def partitionLabels(self, S: str) -> List[int]:
        maxPos = {}
        for i in range(len(S)):
            maxPos[S[i]] = i

        res = []
        start = 0
        scannedCharMaxPos = 0
        for i in range(len(S)):
            curCharMaxPos = maxPos[S[i]]
            if curCharMaxPos > scannedCharMaxPos:
                scannedCharMaxPos = curCharMaxPos
            if i == scannedCharMaxPos:
                res.append(i - start + 1)
                start = i + 1
        return res"""}},
}
