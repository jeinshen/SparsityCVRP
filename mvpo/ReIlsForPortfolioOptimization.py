import random

import pandas as pd
import numpy as np

def INITIALISE():
    df = pd.read_csv('./data/prices.csv')
    df = df[["symbol", "date", "close"]]

    df_matrix = df.pivot(index="date", columns="symbol", values="close")
    df_matrix = df_matrix.loc["2019-01-02":"2021-12-31"]
    df_matrix = df_matrix.dropna(axis=1, how="any")
    df_matrix.to_csv('raw_data.csv')

    def log_return(present, past):
        return np.log(present / past)

    df_return_matrix = df_matrix.apply(lambda col: log_return(col, col.shift(1)))
    df_return_matrix = df_return_matrix.iloc[1:]
    df_return_matrix.to_csv('matrix_of_returns.csv')

    cov_matrix = df_return_matrix.cov()
    cov_matrix.to_csv('matrix_of_covariances.csv')
    global ORIGINAL_SIGMA
    ORIGINAL_SIGMA = cov_matrix.to_numpy()

    return_means = df_return_matrix.mean()
    return_means.to_csv('matrix_of_means.csv')
    global ORIGINAL_MU
    ORIGINAL_MU = return_means.to_numpy()

def f(x):
    if (SIGMA.shape[0] != SIGMA.shape[1]) or (SIGMA.shape[0] != MU.size) or (x.shape != MU.shape):
        print("ERROR: SIGMA and/or MU and/or x have wrong shape")
        return 0
    Variance = (x @ SIGMA) @ x
    Mean = MU @ x
    return Variance - rho * Mean

def gradient(X, epsilon=0.05):
    n = MU.size
    NABLA = np.zeros(n)
    for i in range(n):
        X_1 = np.zeros(n)
        X_1[i] = epsilon
        NABLA[i] = (f(X + X_1) - f(X - X_1)) / (2 * epsilon)
    return NABLA

def next_step(X, new_indices=1, extra_gradient_steps=5, alpha=0.5):
    for _ in range(new_indices):
        NABLA = gradient(X)
        if np.all(NABLA <= 0):
            print("ALL NEGATIVE GRADIENT")
            return X

        NABLA_zero = np.where(X == 0, NABLA, 0)
        NABLA_non_zero = np.where(X != 0, NABLA, 0)

        new_index = np.argmin(NABLA_zero)
        X = X - alpha * NABLA_non_zero
        X[new_index] = - alpha * NABLA_zero[new_index]
        X = np.where(X >= 0, X, 0)
        X = X / sum(X)

    for _ in range(extra_gradient_steps):
        NABLA = gradient(X)
        NABLA_non_zero = np.where(X != 0, NABLA, 0)
        X = X - alpha * NABLA_non_zero
        X = np.where(X >= 0, X, 0)
        X = X / sum(X)

    return X

def greedy(MAX_NONZERO=50, extra_gradient_steps=5, alpha=0.5):
    X = np.zeros(MU.shape)
    for i in range(MAX_NONZERO):
        X = next_step(X, 1, extra_gradient_steps, alpha)
    return X

def revert_random(X):
    A = np.copy(X)
    non_zero_indices = np.nonzero(X)[0]
    values_of_indices = np.zeros(non_zero_indices.size)
    for i in range(len(non_zero_indices)):
        Y = np.copy(X)
        Y[non_zero_indices[i]] = 0
        values_of_indices[i] = f(Y)
    w = values_of_indices - values_of_indices.min() + 1
    p = w / sum(w)

    selected = np.random.choice(non_zero_indices, REVERTED, p=p, replace=False)
    for i in selected:
        A[i] = 0
    return A

def revert_deterministic(X):
    A = np.copy(X)
    non_zero_indices = np.nonzero(X)[0]
    values_of_indices = np.zeros(non_zero_indices.size)
    for i in range(len(non_zero_indices)):
        Y = np.copy(X)
        Y[non_zero_indices[i]] = 0
        values_of_indices[i] = f(Y)
    largest_indices = np.argsort(values_of_indices)[-2:]
    A[largest_indices] = 0
    return A

def ILS(iterations, max_nonzero):
    Current_solution = np.copy(GREEDY)
    Current_value = f(Current_solution)
    step_number = 0
    for i in range(iterations):
        step_number += 1
        X = revert_random(Current_solution)
        X = next_step(X, new_indices=max_nonzero-np.count_nonzero(X))
        if (f(X) < Current_value) or (np.exp(-(step_number)) > np.random.uniform()):
            Current_solution = X
            Current_value = f(Current_solution)
    return Current_solution

INITIALISE()

def get_random_matrices(SIZE):
    random_indices = np.random.choice(ORIGINAL_SIGMA.shape[0], SIZE, replace=False)
    new_SIGMA = ORIGINAL_SIGMA[np.ix_(random_indices, random_indices)]
    new_MU = ORIGINAL_MU[random_indices]
    return new_SIGMA, new_MU


n=5
np.random.seed(0)
rho = 0.5
SIZE_OF_THE_PROBLEM_vector = [100, 200, 400]
MAX_NONZERO_vector = [[10, 20, 30],[20, 40, 60],[40, 80, 120]]
ILS_ITERATIONS_vector = [300,600,1200]

EXTRA_GRADIENT_STEPS = 2
alpha = 1
REVERTED_vector = [[5, 10, 15, 20, 25],[10,20,30,40,50],[20,40,60]]


for i in range(len(SIZE_OF_THE_PROBLEM_vector)):
    SIZE_OF_THE_PROBLEM = SIZE_OF_THE_PROBLEM_vector[i]
    for s in range(5,7):
        random.seed(s)
        SIGMA, MU = get_random_matrices(SIZE_OF_THE_PROBLEM)
        for j in range(len(MAX_NONZERO_vector)):

            MAX_NONZERO = MAX_NONZERO_vector[i][j]
            ILS_ITERATIONS = ILS_ITERATIONS_vector[i]
            REVERTED = REVERTED_vector[i][j]
            GREEDY = greedy(MAX_NONZERO, EXTRA_GRADIENT_STEPS, alpha)
            X = ILS(ILS_ITERATIONS, MAX_NONZERO)
            print(SIZE_OF_THE_PROBLEM, MAX_NONZERO, ILS_ITERATIONS, REVERTED,  (X @ SIGMA) @ X, MU @ X, f(X),  (GREEDY @ SIGMA) @ GREEDY, MU @ GREEDY, f(GREEDY) )