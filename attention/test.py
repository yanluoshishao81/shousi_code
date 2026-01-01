class ListNode:
    def __init__(self,val=0,next=None):
        self.val=val
        self.next=next
def twosum(l1,l2):
    carry=0
    cur=dum=ListNode(0)
    while l1 or l2 or carry:
        if l1:
            carry+=l1.val
            l1=l1.next
        if l2:
            carry+=l2.val
            l2=l2.next
        cur.next=ListNode(carry%10)
        cur=cur.next
        carry//=10
    return  dum.next

# l1=ListNode(0)
# l1.next=ListNode(2)
# l2=ListNode(5)
# l2.next=ListNode(5)
#
# result=twosum(l1,l2)
# while result:
#     print(result.val,end="")
#     result=result.next
def create_list(nums):
    dum=ListNode(0)
    cur=dum
    for num in nums:
        cur.next=ListNode(num)
        cur=cur.next
    return dum.next

def print_list(node):
    result=[]
    while node:
        result.append(str(node.val))
        node=node.next
    return " -> ".join(result) if result else "空链表"

def main():
    input1 = input().