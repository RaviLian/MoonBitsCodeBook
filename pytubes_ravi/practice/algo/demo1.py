from typing import List


def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    m1 = {}
    m2 = {}
    for num in nums1:
        m1[num] = 1

    for elem in nums2:
        m2[elem] = 1

    res = []
    for key in m1:
        if key in m2.keys():
            res.append(key)
    return res


if __name__ == '__main__':
    n1 = [1, 2, 2, 1]
    n2 = [2, 2]
    print(intersection(n1, n2))