import numpy

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    print("starting mat fac")
    '''
    R: rating matrix
    P: |U| * K (User features matrix)
    Q: |D| * K (Item features matrix)
    K: latent features
    steps: iterations
    alpha: learning rate
    beta: regularization parameter'''
    Q = Q.T
    count = 0
    past = 0
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    # calculate error
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])

                    for k in range(K):
                        # calculate gradient with a and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        # if e doesn't change much for 250 steps
        if e-past < 0.005 and e-past >-0.005:
            count += 1
        else:
            count = 1
        past = e
        if count >= 250:
            break
        print("step %d, e = %f, count = %d" % (step,e,count))
    return P, Q.T

def getPred(R):
    # Rating matrix placeholder: get this from database
    # R = [
    #     [5,3,0,1],
    #     [4,0,0,1],
    #     [1,1,0,5],
    #     [1,0,0,4],
    #     [0,1,5,4],
    #     [2,1,3,0],
    #     ]
    R = []
    for user in range(100):
        s = []
        for song in range(5000):
            if numpy.random.randint(5000) < 6:
                s.append(1)
            else:
                s.append(0)
        print("user %d" % user)
        R.append(s)
    R = numpy.array(R)
    # N: num of User
    N = len(R)
    # M: num of Movie
    M = len(R[0])
    # Num of Features
    K = 8
    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = numpy.dot(nP, nQ.T)
    return nR

print(getPred(0))