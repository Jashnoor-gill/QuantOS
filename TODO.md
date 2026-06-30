# TODO - Portfolio Engine Implementation

- [ ] Inspect existing backend portfolio_optimizer routes/services/schemas and frontend PortfolioPage.
- [ ] Create backend/app/modules/portfolio_optimizer/optimizer.py implementing:
  - Mean-Variance (Markowitz) with long-only + weights sum to 1 + target return + risk aversion.
  - Minimum Variance.
  - Risk Parity.
  - Efficient Frontier generation.
- [ ] Extend backend/app/modules/portfolio_optimizer/schemas.py with optimization request/response models.
- [ ] Extend backend/app/modules/portfolio_optimizer/routes.py with the 3 POST optimize endpoints and 1 GET efficient-frontier endpoint.
- [ ] Wire route handlers to optimizer.py functions.
- [ ] Update frontend/src/pages/PortfolioPage.tsx to call these endpoints, render:
  - weights table
  - expected return, volatility, Sharpe ratio
  - efficient frontier chart
- [ ] Ensure backend compiles: python -m py_compile app/main.py
- [ ] Ensure frontend builds: cd frontend && npm run build
- [ ] Verification: report created/modified files, route registrations, endpoint paths, optimizer function names, and first 30 lines of optimizer.py.

