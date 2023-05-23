"""
  A simple model of fertility transition based on income and education levels.
"""
from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize_scalar

class FertilityModel():

    def __init__(self):
        par = self.par = SimpleNamespace()

        # Utility function parameters
        par.beta = 0.95 # Altruistic motives
        par.eta = 0.5 # Decreasing returns to education
        par.alpha = 0.1 # The fixed cost of raising a child
        par.rho = 1.5 # Relative risk aversion
        par.tau = 1 # tmp value
        par.phi = 1 # tmp value
        #lambda y: 0.1*y # The marginal cost of each year of schooling
        
        par.theta = 0.1 # The time cost proportional to parental income
        par.a = 10 # A constant representing the maximum number of children over a lifetime
        par.gamma = 0.5 # Tax on having more than two children

        # Define e* after other par initialized
        par.e = -(1/(1-par.eta))+(par.eta/(1-par.eta))*(par.phi/par.tau) # value for e based on parametrization.
    
    # Update functions for varying paramaters
    def u_phi(self, y):
        par = self.par
        par.phi = par.alpha + par.theta*y
        return # return just tells the function to terminate, but the update is made in the par property.

    
    # Define the utility function with CRRA
    def u(self,c):
        
        par = self.par
        
        if par.rho == 1:
            return np.log(c)
        else:
            return (c**(1-par.rho))/(1-par.rho)
        
    # # Define production function for human capital
    # def h(self):
    #     par = self.par
    #     return (1+par.e)**par.eta
    
    # # Define fertility function
    # def n(self, s, y):
        
    #     par = self.par

    #     #par.phi = par.alpha + par.theta*y
    #     #par.e = (-1/(1-par.eta)) + ((par.eta/(1-par.eta))*(par.phi/par.tau(y)))
    #     return ((1-par.eta)/((1+(1/par.beta))*par.theta))*(1/s)*(1+1/(par.phi/par.tau-1))

    # # Define log-linearized fertility function
    # def log_n(self, s, y):
        
    #     par = self.par

    #     #par.e = (-1/(1-par.eta)) + ((par.eta/(1-par.eta))*(par.phi/par.tau))
    #     return par.a - np.log(s) - np.log(par.phi/par.tau)


    # # Define objective function to maximize
    # def V(self, args):
        
    #     par = self.par

    #     c, s, y = args
    #     return -1*(self.u(c) + par.beta*self.u(s*self.n(s, y)*self.h()))

    # # Define constraint
    # def constraint(self, args):
        
    #     par = self.par

    #     c, s, y = args
    #     n = self.n(s, y)
    #     par.phi = par.alpha + par.theta*y
    #     par.e = (-1/(1-par.eta)) + ((par.eta/(1-par.eta))*(par.phi/par.tau(y)))
    #     if par.gamma == 0: #constraint without tax
    #     return y - c - (par.phi*s*n) - (par.tau(y)*par.e*s*n) 
    #     elif par.gamma != 0 and n <= 2: #Constraint with tax
    #     return y - c - (par.phi*s*n) - (par.tau(y)*par.e*s*n)
    #     else:
    #     return y - c - (par.phi*s*n) - (par.tau(y)*par.e*s*n) - (par.gamma*(n-2)*y)
    

    def solution(self):
        # Define initial guess
        c_guess = 1
        s_guess = 0.9
        y_guess = 100


        # Call constraint method to calculate the constraint value
        const = {'type': 'eq', 'fun': self.constraint}

        # Solve the optimization problem
        sol = minimize_scalar(self.V, (c_guess, s_guess, y_guess), method='bounded', bounds=((0, y_guess), (0, 1), (0, None)), constraints=const)

        # Extract results
        c_star, s_star, y_star = sol.x

        # Print results
        print(f"Optimal consumption: {c_star:.2f}")
        print(f"Optimal survival probability: {s_star:.2f}")
        print(f"Optimal income: {y_star:.2f}")
        print(f"Optimal number of children: {self.n(s_star, y_star):.2f}")
        print(f"Log-linearized optimal number of children: {self.log_n(s_star, y_star):.2f}")