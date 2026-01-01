from collections import defaultdict
def numpair(nums):
    cnt=defaultdict(int)
    ans=0
    for i,x in enumerate(nums):
        ans+=cnt[x]
        cnt[x]+=1
    return ans 

nums=list(map(int,input().split()))
print(numpair(nums))