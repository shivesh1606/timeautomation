def max_subarray_sum(a, b):
    n = len(a)
    m = len(b)
    dp_curr = [0] * 2
    dp_prev = [0] * 2
    
    for i in range(m):
        for j in range(2):
            if j == 0:
                dp_curr[j] = max(dp_prev[j] + a[0], dp_prev[1] + a[n-1])
            else:
                dp_curr[j] = max(dp_prev[j] + a[n-1], dp_prev[0] + a[0])
            a_sum = sum(a)
            dp_curr[j] = max(dp_curr[j], a_sum)
            a.append(b[i])
            a_sum += b[i]
            if j == 0:
                a_sum -= a[0]
                del a[0]
            else:
                a_sum -= a[n]
                del a[n]
            dp_curr[j] = max(dp_curr[j], a_sum)
        
        dp_prev, dp_curr = dp_curr, dp_prev
    
    return max(dp_prev[0], dp_prev[1])
