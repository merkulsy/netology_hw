# 2 task
# Нужно реализовать функцию, принимающую список чисел. Вывести число, которое встречается чаще всего.
# Максимальное число голосов всегда уникально.

# def vote(votes):
#     d = {}
#     for v in votes:
#         d.setdefault(v, 0)
#         d[v] += 1
#     sorted_by_count = sorted(d.items(), key=lambda a: a[1], reverse=True)
#     return sorted_by_count[0][0]

def vote(votes):
    set_votes = set(votes)
    max_vote = max(set_votes, key=lambda v: votes.count(v))
    return max_vote

# print(vote([1,1,1,2,3,4,4,4,4]))
if __name__ == '__main__':
    print(vote([1,1,1,2,3]))
    print(vote([1,2,3,2,2]))