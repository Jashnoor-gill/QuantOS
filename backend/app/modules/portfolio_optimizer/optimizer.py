import numpy as np
import pandas as pd
from scipy.optimize import minimize, Bounds

def mean_variance_optimization(returns, target_return=0.10, risk_aversion=0.5):
    """
    Performs Mean-Variance Optimization (Markowitz).
    """
    cov_matrix = returns.cov()
    expected_returns = returns.mean()
    num_assets = len(expected_returns)

    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights

    def portfolio_return(weights):
        return weights.T @ expected_returns

    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: portfolio_return(x) - target_return}
    ]
    bounds = Bounds(0, 1)
    initial_weights = np.array([1/num_assets] * num_assets)

    result = minimize(portfolio_variance, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    weights = result.x
    expected_portfolio_return = portfolio_return(weights)
    expected_portfolio_volatility = np.sqrt(portfolio_variance(weights))
    sharpe_ratio = expected_portfolio_return / expected_portfolio_volatility

    return {
        "weights": dict(zip(returns.columns, weights)),
        "expected_return": expected_portfolio_return,
        "volatility": expected_portfolio_volatility,
        "sharpe_ratio": sharpe_ratio
    }

def minimum_variance_portfolio(returns):
    """
    Calculates the Minimum Variance Portfolio.
    """
    cov_matrix = returns.cov()
    num_assets = len(cov_matrix)

    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights

    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    bounds = Bounds(0, 1)
    initial_weights = np.array([1/num_assets] * num_assets)

    result = minimize(portfolio_variance, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    weights = result.x
    expected_portfolio_return = returns.mean().T @ weights
    expected_portfolio_volatility = np.sqrt(portfolio_variance(weights))
    sharpe_ratio = expected_portfolio_return / expected_portfolio_volatility

    return {
        "weights": dict(zip(returns.columns, weights)),
        "expected_return": expected_portfolio_return,
        "volatility": expected_portfolio_volatility,
        "sharpe_ratio": sharpe_ratio
    }

def risk_parity_portfolio(returns):
    """
    Calculates the Risk Parity Portfolio.
    """
    cov_matrix = returns.cov()
    num_assets = len(cov_matrix)

    def risk_contribution_objective(weights):
        portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
        marginal_risk_contributions = (weights * (cov_matrix @ weights)) / portfolio_volatility
        total_risk_contributions = marginal_risk_contributions
        risk_parity = total_risk_contributions - total_risk_contributions.mean()
        return np.sum(risk_parity**2)

    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    bounds = Bounds(0, 1)
    initial_weights = np.array([1/num_assets] * num_assets)

    result = minimize(risk_contribution_objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    weights = result.x
    expected_portfolio_return = returns.mean().T @ weights
    expected_portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
    sharpe_ratio = expected_portfolio_return / expected_portfolio_volatility

    return {
        "weights": dict(zip(returns.columns, weights)),
        "expected_return": expected_portfolio_return,
        "volatility": expected_portfolio_volatility,
        "sharpe_ratio": sharpe_ratio
    }


def efficient_frontier(returns, num_portfolios=100):
    """
    Generates the Efficient Frontier.
    """
    cov_matrix = returns.cov()
    expected_returns = returns.mean()
    num_assets = len(expected_returns)
    
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(expected_returns * weights)
        portfolio_std_dev = np.sqrt(weights.T @ cov_matrix @ weights)
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = results[0,i] / results[1,i]
        
    return pd.DataFrame(results.T, columns=['return', 'volatility', 'sharpe_ratio'])
