from fastapi import APIRouter

from app.modules.users.routes import router as users_router
from app.modules.factor_engine.routes import router as factor_engine_router
from app.modules.alpha_engine.routes import router as alpha_engine_router
from app.modules.strategy_engine.routes import router as strategy_engine_router
from app.modules.backtesting_engine.routes import router as backtesting_engine_router
from app.modules.portfolio_optimizer.routes import router as portfolio_optimizer_router
from app.modules.risk_engine.routes import router as risk_engine_router
from app.modules.volatility_lab.routes import router as volatility_lab_router
from app.modules.stat_arb_engine.routes import router as stat_arb_engine_router
from app.modules.reporting.routes import router as reporting_router
from app.modules.ai_assistant.routes import router as ai_assistant_router
from app.modules.market_data.routes import router as market_data_router
from app.modules.analytics.routes import router as analytics_router































router = APIRouter()

# User Management Routes
router.include_router(
    users_router,
    prefix="/auth",
    tags=["Authentication"],
)

# Factor Engine Routes
router.include_router(
    factor_engine_router,
    prefix="/factor-engine",
    tags=["Factor Engine"],
)

# Alpha Engine Routes
router.include_router(
    alpha_engine_router,
    prefix="/alpha-engine",
    tags=["Alpha Engine"],
)

# Strategy Engine Routes
router.include_router(
    strategy_engine_router,
    prefix="/strategy-engine",
    tags=["Strategy Engine"],
)

# Backtesting Engine Routes
router.include_router(
    backtesting_engine_router,
    prefix="/backtesting-engine",
    tags=["Backtesting Engine"],
)

# Portfolio Optimizer Routes
router.include_router(
    portfolio_optimizer_router,
    prefix="/portfolio-optimizer",
    tags=["Portfolio Optimizer"],
)

# Risk Engine Routes
router.include_router(
    risk_engine_router,
    prefix="/risk-engine",
    tags=["Risk Engine"],
)

# Volatility Lab Routes
router.include_router(
    volatility_lab_router,
    prefix="/volatility-lab",
    tags=["Volatility Lab"],
)

# Stat Arb Engine Routes
router.include_router(
    stat_arb_engine_router,
    prefix="/stat-arb-engine",
    tags=["Stat Arb Engine"],
)

# Reporting Routes
router.include_router(
    reporting_router,
    prefix="/reporting",
    tags=["Reporting"],
)

# AI Assistant Routes
router.include_router(
    ai_assistant_router,
    prefix="/ai-assistant",
    tags=["AI Assistant"],
)

# Market Data Routes
router.include_router(
    market_data_router,
    prefix="/market-data",
    tags=["Market Data"],
)

# Analytics Routes
router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)






































