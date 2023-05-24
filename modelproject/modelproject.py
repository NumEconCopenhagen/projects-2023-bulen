"""
  A simple model of fertility transition based on income and education levels.
"""
from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize

class FertilityModel:

    def __init__(self):
        par = self.par = SimpleNamespace()

        # Utility function parameters
        par.beta = 0.95 # Altruistic motives
        par.eta = 0.5 # Decreasing returns to education
        par.alpha = 500 # The fixed cost of raising a child
        par.rho = 1.9 # Relative risk aversion
        par.tau = lambda y: 0.1*y  # tmp value
        par.theta = 0.1 # The time cost proportional to parental income
        par.a = 5 # A constant representing the maximum number of children over a lifetime
        par.gamma = 0 # Tax on having more than two children

    # Define e* after other par initialized
    def e_star(self, y):
        par = self.par
        return -(1/(1-par.eta))+(par.eta/(1-par.eta))*(self.phi(y)/par.tau(y)) # value for e based on parametrization.
    
    
    # Update functions for varying paramaters
    def phi(self, y):
        par = self.par
        return par.alpha + par.theta*y

    
    # Define the utility function with CRRA
    def u(self,c):
        par = self.par
        
        if par.rho == 1:
            return np.log(c)
        else:
            return (c**(1-par.rho))/(1-par.rho)
        
    # Define production function for human capital
    def h(self, e):
        par = self.par
        return (1+e)**par.eta
    
    
    # Define fertility function
    def n(self, s, y):
        par = self.par

        return ((1-par.eta)/((1+(1/par.beta))*par.theta))*(1/s)*(1+1/(self.phi(y)/par.tau(y)-1))

    # Define log-linearized fertility function
    def log_n(self, s, y):
        par = self.par

        return par.a - np.log(s) - np.log(self.phi(y)/par.tau(y))

    # Define objective function to maximize
    def V(self, args):
        par = self.par

        c, s, y = args
        snh = s*self.n(s, y)*self.h(self.e_star(y))
        return -1*(self.u(c) + par.beta*self.u(snh))

    # Define constraint
    def constraint(self, args):
        par = self.par

        c, s, y = args
        n = self.n(s, y)
        if par.gamma == 0:  # constraint without tax
            return y - c - (self.phi(y) * s * n) - (par.tau(y) * self.e_star(y) * s * n)
        elif par.gamma != 0 and n <= 2:  # Constraint with tax
            return y - c - (self.phi(y) * s * n) - (par.tau(y) * self.e_star(y) * s * n)
        else:
            return y - c - (self.phi(y) * s * n) - (par.tau(y) * self.e_star(y) * s * n) - (par.gamma * (n - 2) * y)

    def solution(self):
        # Define initial guess
        initial_guesses = (100, 0.8, 1000)

        # Call constraint method to calculate the constraint value
        const = {'type': 'ineq', 'fun': self.constraint}

        # Solve the optimization problem
        sol = minimize(self.V, initial_guesses, method='SLSQP', bounds=[(0, None), (0, None), (0, None)],  constraints=const)

        # Extract results
        c_star, s_star, y_star = sol.x

       # Return the results as a dictionary
        results = {
            "Optimal consumption": c_star,
            "Optimal survival probability": s_star,
            "Optimal income": y_star,
            "Optimal number of children": self.n(s_star, y_star),
            "Log-linearized optimal number of children": self.log_n(s_star, y_star)
         }

        return results
