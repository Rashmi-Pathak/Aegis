const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function run(cmd) {
  try {
    return execSync(cmd, { stdio: 'pipe' }).toString();
  } catch (err) {
    if (err.stdout) return err.stdout.toString();
    if (err.stderr) return err.stderr.toString();
    throw err;
  }
}

// 1. Root and config
const commits = [
  { files: ['.gitignore'], msg: 'chore: configure comprehensive gitignore for python, node, and databases' },
  { files: ['.env.example'], msg: 'chore: add root environment variables template' },
  { files: ['Makefile'], msg: 'chore: add development and build tasks to Makefile' },
  { files: ['docker-compose.yml'], msg: 'infra(docker): add multi-container docker compose configuration' },
  { files: ['.github/workflows/ci.yml', '.github/workflows/.gitkeep'], msg: 'ci(github): add automated CI workflow for backend tests and frontend build' },
  { files: ['README.md'], msg: 'docs: add comprehensive platform architecture and quickstart guide' },
  { files: ['docker/.gitkeep'], msg: 'infra(docker): initialize container docker recipes' },
  { files: ['infrastructure/.gitkeep'], msg: 'infra(k8s): initialize deployment manifests and terraform directory' },
  { files: ['docs/architecture.md'], msg: 'docs(arch): add high-level enterprise architecture specification' },
  { files: ['docs/data-model.md', 'docs/canonical-model.md'], msg: 'docs(data): specify canonical enterprise data model and ER diagrams' },
  { files: ['docs/risk-engine.md', 'docs/decision-engine.md', 'docs/simulation-engine.md'], msg: 'docs(intelligence): specify Bayesian risk, decision queue, and what-if simulation' },
  { files: ['docs/ml-pipeline.md', 'docs/security.md', 'docs/multi-tenancy.md'], msg: 'docs(mlops): document ML pipeline, tenant isolation, and security models' },
  { files: ['docs/demo-businesses.md', 'docs/frontend-design-system.md', 'docs/api.md', 'docs/deployment.md'], msg: 'docs(spec): document demo businesses and hot-orange visual design system' },
  { files: ['tests/__init__.py', 'tests/backend/__init__.py', 'tests/backend/unit/__init__.py', 'tests/backend/api/__init__.py'], msg: 'test(structure): initialize root test package hierarchy' },
  { files: ['tests/backend/engines/__init__.py', 'tests/backend/integration/__init__.py', 'tests/backend/ml/__init__.py', 'tests/backend/security/__init__.py'], msg: 'test(backend): initialize engine and security test submodules' },
  { files: ['tests/data/fixtures/.gitkeep', 'tests/data/synthetic/.gitkeep'], msg: 'test(data): configure synthetic dataset test fixtures' },
  { files: ['tests/frontend/components/.gitkeep', 'tests/frontend/pages/.gitkeep', 'tests/frontend/animations/.gitkeep'], msg: 'test(frontend): initialize frontend component test suites' },
  { files: ['data/demo-businesses/.gitkeep'], msg: 'data(init): initialize demo business storage directory' },
  { files: ['data/demo-businesses/AgroNova_Aegis_Demo.zip'], msg: 'data(agronova): add precision agriculture and crop telemetry demo archive' },
  { files: ['data/demo-businesses/AutoCore_Aegis_Demo.zip'], msg: 'data(autocore): add automotive manufacturing and parts supply demo archive' },
  { files: ['data/demo-businesses/BuildRight_Aegis_Demo.zip'], msg: 'data(buildright): add construction material and equipment telemetry demo archive' },
  { files: ['data/demo-businesses/CloudNest_Aegis_Demo.zip'], msg: 'data(cloudnest): add multi-cloud SaaS and infrastructure telemetry demo archive' },
  { files: ['data/demo-businesses/EduTech_Labs_Aegis_Demo.zip'], msg: 'data(edutech): add digital learning and user cohort subscription demo archive' },
  { files: ['data/demo-businesses/FinEdge_Aegis_Demo.zip'], msg: 'data(finedge): add algorithmic fintech and capital liquidity demo archive' },
  { files: ['data/demo-businesses/FreshKart_Aegis_Demo.zip'], msg: 'data(freshkart): add perishable grocery and cold-chain logistics demo archive' },
  { files: ['data/demo-businesses/GreenGrid_Aegis_Demo.zip'], msg: 'data(greengrid): add renewable utility grid and battery storage demo archive' },
  { files: ['data/demo-businesses/MediPlus_Aegis_Demo.zip'], msg: 'data(mediplus): add healthcare diagnostics and pharma supply demo archive' },
  { files: ['data/demo-businesses/NovaMart_Aegis_Demo.zip'], msg: 'data(novamart): add omnichannel retail and inventory turnover demo archive' },
  { files: ['data/demo-businesses/PrimeLogix_Aegis_Demo.zip'], msg: 'data(primelogix): add national freight fleet and logistics demo archive' },
  { files: ['data/demo-businesses/StaySphere_Aegis_Demo.zip'], msg: 'data(staysphere): add hospitality booking and dynamic revenue demo archive' },
  { files: ['data/demo-businesses/StyleSphere_Aegis_Demo.zip'], msg: 'data(stylesphere): add fashion apparel and fast-turn inventory demo archive' },
  { files: ['data/demo-businesses/UrbanEats_Aegis_Demo.zip'], msg: 'data(urbaneats): add on-demand food delivery and courier network demo archive' },
  { files: ['backend/requirements.txt'], msg: 'chore(backend): pin production Python dependencies' },
  { files: ['backend/pyproject.toml', 'backend/alembic.ini'], msg: 'chore(backend): configure pyproject, ruff, black, and alembic' },
  { files: ['backend/app/__init__.py', 'backend/app/core/__init__.py'], msg: 'feat(core): initialize backend application and core configuration' },
  { files: ['backend/app/core/config.py'], msg: 'feat(core): implement Pydantic BaseSettings for platform environment' },
  { files: ['backend/app/core/constants.py', 'backend/app/core/exceptions.py'], msg: 'feat(core): define system constants and custom business exception types' },
  { files: ['backend/app/core/logging.py'], msg: 'feat(core): configure structured JSON logging formatters' },
  { files: ['backend/app/core/security.py'], msg: 'feat(security): implement bcrypt password hashing and JWT token handlers' },
  { files: ['backend/app/core/middleware.py'], msg: 'feat(security): implement tenant isolation and request correlation middleware' },
  { files: ['backend/app/db/__init__.py', 'backend/app/db/base.py', 'backend/app/db/session.py'], msg: 'feat(db): configure SQLAlchemy engine and scoped session maker' },
  { files: ['backend/app/models/__init__.py'], msg: 'feat(models): initialize SQLAlchemy enterprise model registry' },
  { files: ['backend/app/models/tenant.py', 'backend/app/models/user.py', 'backend/app/models/role.py'], msg: 'feat(models-auth): add Tenant, User, and Role ORM entities' },
  { files: ['backend/app/models/business.py', 'backend/app/models/dataset.py', 'backend/app/models/schema_mapping.py'], msg: 'feat(models-business): add Business, Dataset, and SchemaMapping entities' },
  { files: ['backend/app/models/metric.py', 'backend/app/models/anomaly.py', 'backend/app/models/risk.py', 'backend/app/models/forecast.py'], msg: 'feat(models-intel): add Metric, Anomaly, Risk, and Forecast entities' },
  { files: ['backend/app/models/decision.py', 'backend/app/models/simulation.py', 'backend/app/models/graph_node.py', 'backend/app/models/graph_edge.py'], msg: 'feat(models-prescriptive): add Decision, Simulation, and Graph entities' },
  { files: ['backend/app/models/report.py', 'backend/app/models/alert.py', 'backend/app/models/audit_log.py', 'backend/app/models/job.py'], msg: 'feat(models-governance): add Report, Alert, AuditLog, and BackgroundJob entities' },
  { files: ['backend/app/schemas/__init__.py', 'backend/app/schemas/auth.py', 'backend/app/schemas/tenant.py', 'backend/app/schemas/user.py'], msg: 'feat(schemas-auth): define Pydantic schemas for authentication and tenants' },
  { files: ['backend/app/schemas/dataset.py', 'backend/app/schemas/schema_mapping.py'], msg: 'feat(schemas-data): define Pydantic schemas for dataset ingestion and mapping' },
  { files: ['backend/app/schemas/analytics.py', 'backend/app/schemas/metric.py'], msg: 'feat(schemas-analytics): define schemas for KPIs and business analytics' },
  { files: ['backend/app/schemas/anomaly.py', 'backend/app/schemas/risk.py', 'backend/app/schemas/forecast.py'], msg: 'feat(schemas-intel): define schemas for anomalies, risks, and forecasts' },
  { files: ['backend/app/schemas/decision.py', 'backend/app/schemas/simulation.py', 'backend/app/schemas/graph.py'], msg: 'feat(schemas-prescriptive): define schemas for decisions, simulations, and graph' },
  { files: ['backend/app/schemas/report.py', 'backend/app/schemas/alert.py', 'backend/app/schemas/audit.py', 'backend/app/schemas/job.py'], msg: 'feat(schemas-governance): define schemas for reports, alerts, and audit logs' },
  { files: ['backend/app/db/repositories/__init__.py', 'backend/app/db/repositories/base_repository.py'], msg: 'feat(repositories): implement generic BaseRepository with typed CRUD' },
  { files: ['backend/app/db/repositories/tenant_repository.py', 'backend/app/db/repositories/user_repository.py'], msg: 'feat(repositories-auth): implement TenantRepository and UserRepository' },
  { files: ['backend/app/db/repositories/business_repository.py', 'backend/app/db/repositories/dataset_repository.py'], msg: 'feat(repositories-business): implement BusinessRepository and DatasetRepository' },
  { files: ['backend/app/db/repositories/anomaly_repository.py', 'backend/app/db/repositories/risk_repository.py', 'backend/app/db/repositories/forecast_repository.py'], msg: 'feat(repositories-intel): implement Anomaly, Risk, and Forecast repositories' },
  { files: ['backend/app/db/repositories/decision_repository.py', 'backend/app/db/repositories/simulation_repository.py'], msg: 'feat(repositories-decision): implement DecisionRepository and SimulationRepository' },
  { files: ['backend/app/db/repositories/report_repository.py', 'backend/app/db/repositories/alert_repository.py', 'backend/app/db/repositories/audit_repository.py', 'backend/app/db/repositories/job_repository.py'], msg: 'feat(repositories-governance): implement Report, Alert, Audit, and Job repositories' },
  { files: ['backend/app/data_ingestion/__init__.py'], msg: 'feat(ingestion): initialize enterprise data ingestion engine' },
  { files: ['backend/app/data_ingestion/readers/'], msg: 'feat(ingestion-readers): implement CSV, Excel, and JSON streaming file readers' },
  { files: ['backend/app/data_ingestion/unpacker/'], msg: 'feat(ingestion-unpacker): implement multi-business ZIP archive extraction' },
  { files: ['backend/app/data_ingestion/schema_detection/'], msg: 'feat(ingestion-schema): implement automated schema detection and column inference' },
  { files: ['backend/app/data_ingestion/validation/'], msg: 'feat(ingestion-validation): implement outlier validation and completeness checks' },
  { files: ['backend/app/data_ingestion/cleaning/'], msg: 'feat(ingestion-cleaning): implement data sanitization and type coercion pipeline' },
  { files: ['backend/app/data_ingestion/profiling/'], msg: 'feat(ingestion-profiling): implement descriptive data profiling and summary statistics' },
  { files: ['backend/app/data_ingestion/canonical_mapping/'], msg: 'feat(ingestion-canonical): implement canonical enterprise business model mapping' },
  { files: ['backend/app/analytics/__init__.py'], msg: 'feat(analytics): initialize business intelligence and KPI calculation layer' },
  { files: ['backend/app/analytics/revenue_analytics.py', 'backend/app/analytics/margin_analytics.py'], msg: 'feat(analytics-revenue): implement revenue trajectory and margin compression models' },
  { files: ['backend/app/analytics/customer_analytics.py', 'backend/app/analytics/cohort_analytics.py'], msg: 'feat(analytics-customer): implement customer churn risk and cohort LTV models' },
  { files: ['backend/app/analytics/inventory_analytics.py', 'backend/app/analytics/supply_chain_analytics.py'], msg: 'feat(analytics-inventory): implement stock turnover and supply chain lead-time analytics' },
  { files: ['backend/app/analytics/financial_analytics.py', 'backend/app/analytics/working_capital.py'], msg: 'feat(analytics-finance): implement free cash flow and working capital calculators' },
  { files: ['backend/app/analytics/kpi_calculator.py', 'backend/app/analytics/health_score_engine.py'], msg: 'feat(analytics-kpi): implement composite health score and enterprise KPI aggregator' },
  { files: ['backend/app/analytics/feature_engineering.py', 'backend/app/analytics/time_features.py'], msg: 'feat(analytics-features): implement lag features and rolling window transformations' },
  { files: ['backend/app/analytics/streaming_telemetry.py'], msg: 'feat(analytics-telemetry): implement streaming telemetry buffer with online quantiles' },
  { files: ['backend/app/analytics/mobile_viewport_optimizer.py'], msg: 'feat(analytics-viewport): implement mobile viewport optimization and matrix downsampling' },
  { files: ['backend/app/ml/__init__.py', 'backend/app/ml/anomaly_detection/__init__.py'], msg: 'feat(ml): initialize machine learning intelligence subsystems' },
  { files: ['backend/app/ml/anomaly_detection/isolation_forest.py'], msg: 'feat(anomaly-isolation): implement multi-dimensional isolation forest detector' },
  { files: ['backend/app/ml/anomaly_detection/time_series_anomaly.py', 'backend/app/ml/anomaly_detection/statistical_anomaly.py'], msg: 'feat(anomaly-timeseries): implement rolling Bollinger bands and statistical Z-score detector' },
  { files: ['backend/app/ml/anomaly_detection/anomaly_clustering.py', 'backend/app/ml/anomaly_detection/root_cause_attributor.py'], msg: 'feat(anomaly-attribution): implement causal clustering for anomaly telemetry' },
  { files: ['backend/app/ml/forecasting/__init__.py'], msg: 'feat(forecasting): initialize predictive forecasting subsystem' },
  { files: ['backend/app/ml/forecasting/sarimax_model.py'], msg: 'feat(forecasting-sarimax): implement seasonal ARIMA time-series forecaster' },
  { files: ['backend/app/ml/forecasting/lightgbm_forecaster.py'], msg: 'feat(forecasting-lightgbm): implement gradient boosted tree forecaster with lag features' },
  { files: ['backend/app/ml/forecasting/xgboost_forecaster.py'], msg: 'feat(forecasting-xgboost): implement extreme gradient boosting multi-step model' },
  { files: ['backend/app/ml/forecasting/ensemble_forecaster.py', 'backend/app/ml/forecasting/confidence_bands.py'], msg: 'feat(forecasting-ensemble): implement dynamic ensemble blending with 95% confidence intervals' },
  { files: ['backend/app/risk/__init__.py'], msg: 'feat(risk): initialize enterprise risk modeling framework' },
  { files: ['backend/app/risk/bayesian_risk.py'], msg: 'feat(risk-bayesian): implement Bayesian risk quantification (Probability x Impact x Exposure)' },
  { files: ['backend/app/risk/risk_propagation.py'], msg: 'feat(risk-propagation): implement topological risk propagation through dependency graph' },
  { files: ['backend/app/risk/copula_simulation.py'], msg: 'feat(risk-copula): implement multivariate Gaussian and Student-t Copula loss simulations' },
  { files: ['backend/app/risk/stress_testing.py', 'backend/app/risk/macro_shocks.py'], msg: 'feat(risk-stress): implement macroeconomic trade war and supply shock stress tests' },
  { files: ['backend/app/risk/risk_scorer.py', 'backend/app/risk/exposure_aggregator.py'], msg: 'feat(risk-scoring): implement composite risk index and exposure aggregation' },
  { files: ['backend/app/decision_intelligence/__init__.py'], msg: 'feat(decision): initialize prescriptive decision intelligence engine' },
  { files: ['backend/app/decision_intelligence/prescriptive_ranking.py'], msg: 'feat(decision-ranking): implement prescriptive action ranking with pre-computed ROI' },
  { files: ['backend/app/decision_intelligence/optimizer.py', 'backend/app/decision_intelligence/constraints.py'], msg: 'feat(decision-optimizer): implement linear programming resource allocator' },
  { files: ['backend/app/decision_intelligence/approval_workflow.py'], msg: 'feat(decision-workflow): implement human-in-the-loop executive authorization state machine' },
  { files: ['backend/app/simulation/__init__.py', 'backend/app/simulation/simulation_engine.py'], msg: 'feat(simulation-engine): implement multi-variable what-if business simulation engine' },
  { files: ['backend/app/simulation/scenario_templates.py', 'backend/app/simulation/elasticity_models.py'], msg: 'feat(simulation-scenarios): implement predefined market shock scenario templates' },
  { files: ['backend/app/graph/__init__.py', 'backend/app/graph/business_dependency_graph.py'], msg: 'feat(graph): implement directed enterprise dependency graph with NetworkX' },
  { files: ['backend/app/graph/causal_path_tracer.py', 'backend/app/graph/graph_export.py'], msg: 'feat(graph-causal): implement DAG topological ordering and causal path tracing' },
  { files: ['backend/app/investigation/__init__.py', 'backend/app/investigation/investigation_engine.py', 'backend/app/investigation/evidence_collector.py'], msg: 'feat(investigation): implement automated root cause investigation workspace' },
  { files: ['backend/app/reports/__init__.py', 'backend/app/reports/report_generator.py', 'backend/app/reports/board_dossier.py'], msg: 'feat(reports): implement automated PDF and executive board dossier report generator' },
  { files: ['backend/app/alerts/__init__.py', 'backend/app/alerts/alert_manager.py', 'backend/app/alerts/dispatchers.py'], msg: 'feat(alerts): implement priority alert generator and notification dispatchers' },
  { files: ['backend/app/audit/__init__.py', 'backend/app/audit/audit_logger.py', 'backend/app/audit/compliance_monitor.py'], msg: 'feat(audit): implement tamper-evident multi-tenant audit trail logger' },
  { files: ['backend/app/demo/__init__.py', 'backend/app/demo/demo_discovery.py'], msg: 'feat(demo-discovery): implement dynamic demo business archive scanner and indexer' },
  { files: ['backend/app/demo/demo_seeder.py', 'backend/app/demo/dataset_cache.py'], msg: 'feat(demo-seeder): implement automatic synthetic enterprise data seed loader' },
  { files: ['backend/app/mlops/__init__.py', 'backend/app/mlops/model_registry.py', 'backend/app/mlops/champion_challenger.py'], msg: 'feat(mlops-registry): implement champion-challenger model registry and versioning' },
  { files: ['backend/app/mlops/drift_monitor.py', 'backend/app/mlops/performance_tracker.py'], msg: 'feat(mlops-drift): implement KS-test and PSI data drift monitor' },
  { files: ['backend/app/services/__init__.py', 'backend/app/services/auth_service.py', 'backend/app/services/tenant_service.py'], msg: 'feat(services-auth): implement authentication and authorization application services' },
  { files: ['backend/app/services/analytics_service.py', 'backend/app/services/kpi_service.py'], msg: 'feat(services-analytics): implement high-level analytics and telemetry services' },
  { files: ['backend/app/services/anomaly_service.py', 'backend/app/services/risk_service.py', 'backend/app/services/forecast_service.py'], msg: 'feat(services-intel): implement anomaly, risk, and forecast services' },
  { files: ['backend/app/services/decision_service.py', 'backend/app/services/simulation_service.py'], msg: 'feat(services-decision): implement decision and simulation application services' },
  { files: ['backend/app/api/__init__.py', 'backend/app/api/deps.py', 'backend/app/api/v1/__init__.py'], msg: 'feat(api-deps): configure FastAPI dependency injection and security dependencies' },
  { files: ['backend/app/api/v1/auth.py', 'backend/app/api/v1/users.py'], msg: 'feat(api-auth): implement auth and user login/signup route handlers' },
  { files: ['backend/app/api/v1/analytics.py', 'backend/app/api/v1/kpis.py'], msg: 'feat(api-analytics): implement analytics overview and KPI endpoint routes' },
  { files: ['backend/app/api/v1/anomalies.py', 'backend/app/api/v1/risks.py', 'backend/app/api/v1/forecasts.py'], msg: 'feat(api-intel): implement anomaly, risk, and forecast API endpoints' },
  { files: ['backend/app/api/v1/decisions.py', 'backend/app/api/v1/simulations.py', 'backend/app/api/v1/graph.py'], msg: 'feat(api-prescriptive): implement decision, simulation, and graph topology routes' },
  { files: ['backend/app/api/v1/reports.py', 'backend/app/api/v1/alerts.py', 'backend/app/api/v1/audit.py', 'backend/app/api/v1/demo.py'], msg: 'feat(api-governance): implement report, alert, audit, and demo business routes' },
  { files: ['backend/app/main.py'], msg: 'feat(backend-main): assemble main FastAPI application with CORS and life-cycle startup' },
  { files: ['backend/tests/conftest.py'], msg: 'test(backend): configure global pytest fixtures and sys.path injection' },
  { files: ['backend/tests/test_kpis.py'], msg: 'test(kpi): add unit test suite for revenue, margin, and health score calculations' },
  { files: ['backend/tests/test_anomaly_detection.py'], msg: 'test(anomalies): add unit tests for isolation forest and time series spike detection' },
  { files: ['backend/tests/test_forecasting_and_risk.py'], msg: 'test(forecasting): add unit tests for time series forecasting and risk matrix' },
  { files: ['backend/tests/test_deep_forecasting.py'], msg: 'test(deep-forecasting): add tests for SARIMAX, LightGBM, and ensemble forecasting' },
  { files: ['backend/tests/test_deep_risk_models.py'], msg: 'test(deep-risk): add unit tests for Bayesian priors, copula loss, and portfolio variance' },
  { files: ['backend/tests/test_deep_decision_engine.py'], msg: 'test(deep-decision): add unit tests for prescriptive decision queue and ROI models' },
  { files: ['backend/tests/test_deep_analytics_and_rules.py'], msg: 'test(deep-analytics): add unit tests for business rules and feature engineering' },
  { files: ['backend/tests/test_advanced_algorithms.py'], msg: 'test(algorithms): add unit tests for advanced analytical algorithms' },
  { files: ['backend/tests/test_advanced_intelligence_tier.py'], msg: 'test(tier): add unit tests for advanced intelligence tier capabilities' },
  { files: ['backend/tests/test_synthetic_verticals.py'], msg: 'test(synthetic): add unit tests for synthetic vertical business datasets' },
  { files: ['backend/tests/test_all_repositories.py'], msg: 'test(repos): add repository integration test suite' },
  { files: ['backend/tests/test_champion_challenger.py'], msg: 'test(mlops): add champion-challenger model registry test suite' },
  { files: ['backend/tests/test_pipeline_e2e.py'], msg: 'test(e2e): add end-to-end data pipeline integration test' },
  { files: ['backend/tests/test_ingestion_csv_and_excel.py'], msg: 'test(ingestion): add unit tests for CSV and Excel data ingestion' },
  { files: ['backend/tests/test_industry_generators.py'], msg: 'test(generators): add industry-specific synthetic data generator tests' },
  { files: ['backend/tests/test_kalman_and_esg.py'], msg: 'test(kalman-esg): add tests for Kalman filter and ESG regulatory risk scoring' },
  { files: ['backend/tests/test_board_dossier_and_trade_war.py'], msg: 'test(dossier): add tests for executive board dossier and macro trade war shock' },
  { files: ['backend/tests/test_final_enterprise_layer.py'], msg: 'test(enterprise): add tests for final enterprise governance layer' },
  { files: ['backend/tests/test_system_infrastructure.py'], msg: 'test(system): add tests for system infrastructure and health checks' },
  { files: ['backend/tests/test_streaming_telemetry.py'], msg: 'test(telemetry): add unit tests for streaming telemetry buffer and quantiles' },
  { files: ['backend/tests/test_mobile_viewport_optimizer.py'], msg: 'test(viewport): add tests for mobile viewport optimizer and downsampling' },
  { files: ['backend/tests/test_mobile_telemetry_and_audit.py'], msg: 'test(mobile-audit): add tests for mobile client telemetry and audit trails' },
  { files: ['backend/tests/test_live_api.py'], msg: 'test(live-api): add live FastAPI endpoint integration test suite' },
  { files: ['frontend/package.json', 'frontend/package-lock.json'], msg: 'chore(frontend): configure package dependencies and npm lockfile' },
  { files: ['frontend/tsconfig.json', 'frontend/tsconfig.node.json', 'frontend/vite.config.ts'], msg: 'chore(frontend): configure TypeScript compiler and Vite bundler' },
  { files: ['frontend/tailwind.config.js', 'frontend/postcss.config.js'], msg: 'chore(frontend): configure Tailwind CSS hot-orange enterprise theme' },
  { files: ['frontend/index.html'], msg: 'feat(frontend-html): set up application HTML shell and font links' },
  { files: ['frontend/src/styles/globals.css', 'frontend/src/styles/design-tokens.css', 'frontend/src/styles/animations.css'], msg: 'feat(frontend-styles): configure global CSS, hot-orange neon bloom, and glow tokens' },
  { files: ['frontend/src/types/index.ts'], msg: 'feat(frontend-types): define comprehensive TypeScript domain and API interfaces' },
  { files: ['frontend/src/api/client.ts', 'frontend/src/api/authApi.ts'], msg: 'feat(api-client): implement typed API client with token injection and authApi' },
  { files: ['frontend/src/api/analyticsApi.ts'], msg: 'feat(api-analytics): implement frontend API connector for analytics and KPIs' },
  { files: ['frontend/src/api/riskApi.ts'], msg: 'feat(api-risk): implement frontend API connector for risk intelligence' },
  { files: ['frontend/src/api/forecastApi.ts'], msg: 'feat(api-forecast): implement frontend API connector for predictive forecasts' },
  { files: ['frontend/src/api/decisionApi.ts'], msg: 'feat(api-decision): implement frontend API connector for prescriptive decisions' },
  { files: ['frontend/src/api/simulationApi.ts'], msg: 'feat(api-simulation): implement frontend API connector for what-if simulation' },
  { files: ['frontend/src/api/graphApi.ts'], msg: 'feat(api-graph): implement frontend API connector for business dependency graph' },
  { files: ['frontend/src/api/demoApi.ts'], msg: 'feat(api-demo): implement frontend API connector for 14 demo businesses' },
  { files: ['frontend/src/api/datasetApi.ts', 'frontend/src/api/alertApi.ts', 'frontend/src/api/modelApi.ts', 'frontend/src/api/reportApi.ts'], msg: 'feat(api-system): implement frontend connectors for datasets, alerts, models, and reports' },
  { files: ['frontend/src/components/GlowButton.tsx', 'frontend/src/components/GlowCard.tsx', 'frontend/src/components/SectionHeader.tsx'], msg: 'feat(ui-primitives): create hot-orange glowing buttons and glassmorphic cards' },
  { files: ['frontend/src/components/MetricCard.tsx', 'frontend/src/components/RiskCard.tsx'], msg: 'feat(ui-widgets): create MetricCard and RiskCard components' },
  { files: ['frontend/src/components/ForecastCard.tsx', 'frontend/src/components/DecisionCard.tsx'], msg: 'feat(ui-cards): create ForecastCard and DecisionCard components' },
  { files: ['frontend/src/components/AnomalyCard.tsx', 'frontend/src/components/HealthScoreCard.tsx'], msg: 'feat(ui-telemetry): create AnomalyCard and HealthScoreCard components' },
  { files: ['frontend/src/components/DataTable.tsx'], msg: 'feat(ui-table): create responsive, horizontally scrollable DataTable component' },
  { files: ['frontend/src/backgrounds/CommandCenterBackground.tsx', 'frontend/src/backgrounds/HeroGlowBackground.tsx'], msg: 'feat(ui-backgrounds): implement dynamic telemetry grid and hero glowing gradient reservoirs' },
  { files: ['frontend/src/animations/GlowCursor.tsx'], msg: 'feat(ui-cursor): implement WebGL glowing cursor shader trail' },
  { files: ['frontend/src/components/ScrollTimelineGlow.tsx'], msg: 'feat(ui-timeline): implement animated scrolling timeline glow beam' },
  { files: ['frontend/src/charts/RevenueChart.tsx', 'frontend/src/charts/ContributionChart.tsx'], msg: 'feat(charts-revenue): implement Recharts revenue trend and division contribution charts' },
  { files: ['frontend/src/charts/RevenueForecastChart.tsx', 'frontend/src/charts/ForecastConfidenceChart.tsx'], msg: 'feat(charts-forecasting): implement multi-horizon forecast trajectory and confidence envelope charts' },
  { files: ['frontend/src/charts/HeatmapChart.tsx', 'frontend/src/charts/RiskTrendChart.tsx', 'frontend/src/charts/AnomalyTimeline.tsx'], msg: 'feat(charts-risk): implement probability-impact scatter matrix and anomaly timeline charts' },
  { files: ['frontend/src/charts/ScenarioComparisonChart.tsx'], msg: 'feat(charts-simulation): implement scenario comparison chart with baseline vs simulated overlay' },
  { files: ['frontend/src/components/status/StatusIndicator.tsx'], msg: 'feat(ui-status): implement telemetry pulse status indicator' },
  { files: ['frontend/src/components/navigation/CommandPalette.tsx'], msg: 'feat(ui-command): implement quick search and Cmd+K command palette modal' },
  { files: ['frontend/src/components/notifications/NotificationCenter.tsx'], msg: 'feat(ui-notifications): implement real-time notification drawer' },
  { files: ['frontend/src/components/navigation/Sidebar.tsx'], msg: 'feat(navigation-sidebar): implement collapsible sidebar rail and mobile drawer navigation' },
  { files: ['frontend/src/components/navigation/TopBar.tsx'], msg: 'feat(navigation-topbar): implement responsive TopBar with hamburger, search, and org switcher' },
  { files: ['frontend/src/components/layout/AppShell.tsx', 'frontend/src/components/AppShell.tsx', 'frontend/src/layouts/AppLayout.tsx'], msg: 'feat(layout-shell): implement fluid AppShell with Ctrl+B shortcut and responsive margins' },
  { files: ['frontend/src/pages/landing/LandingPage.tsx'], msg: 'feat(pages-landing): implement dark-brown and hot-orange enterprise AI landing page' },
  { files: ['frontend/src/pages/command-center/ExecutiveCommandCenterPage.tsx'], msg: 'feat(pages-command): implement real-time Executive Command Center page' },
  { files: ['frontend/src/pages/analytics/AnalyticsPage.tsx'], msg: 'feat(pages-analytics): implement enterprise KPI analytics and corridor performance page' },
  { files: ['frontend/src/pages/forecast-center/ForecastCenterPage.tsx'], msg: 'feat(pages-forecast): implement multi-horizon predictive Forecast Center page' },
  { files: ['frontend/src/pages/risk-center/RiskCenterPage.tsx'], msg: 'feat(pages-risk): implement interactive Risk Intelligence and threat radar center page' },
  { files: ['frontend/src/pages/decision-center/DecisionCenterPage.tsx'], msg: 'feat(pages-decision): implement Prescriptive Decision Center with executive authorization queue' },
  { files: ['frontend/src/pages/simulation/WhatIfSimulationPage.tsx'], msg: 'feat(pages-simulation): implement What-If Digital Twin Simulation Studio page' },
  { files: ['frontend/src/pages/business-graph/BusinessGraphPage.tsx'], msg: 'feat(pages-graph): implement interactive NetworkX Business Dependency Graph topology page' },
  { files: ['frontend/src/pages/investigation/InvestigationWorkspacePage.tsx'], msg: 'feat(pages-investigation): implement Causal Investigation Workspace and evidence inspection page' },
  { files: ['frontend/src/pages/data-center/DataCenterPage.tsx'], msg: 'feat(pages-datacenter): implement Data Center and Ingestion Intelligence page' },
  { files: ['frontend/src/pages/models/ModelIntelligencePage.tsx'], msg: 'feat(pages-models): implement Model Intelligence and Drift Monitor page' },
  { files: ['frontend/src/pages/alerts/AlertCenterPage.tsx'], msg: 'feat(pages-alerts): implement Real-Time Telemetry System Alert Center page' },
  { files: ['frontend/src/pages/reports/ExecutiveReportsPage.tsx'], msg: 'feat(pages-reports): implement Executive Reports and Audit Dossier page' },
  { files: ['frontend/src/pages/settings/OrganizationSettingsPage.tsx', 'frontend/src/pages/settings/SettingsPage.tsx'], msg: 'feat(pages-settings): implement Organization & Team governance and platform settings' },
  { files: ['frontend/src/pages/admin/SuperAdminPage.tsx'], msg: 'feat(pages-admin): implement Super Admin multi-tenant control console' },
  { files: ['frontend/src/pages/auth/LoginPage.tsx', 'frontend/src/pages/auth/SignupPage.tsx'], msg: 'feat(pages-auth): implement centered enterprise Login and Tenant Provisioning forms' },
  { files: ['frontend/src/pages/onboarding/OnboardingFlowPage.tsx'], msg: 'feat(pages-onboarding): implement multi-step tenant onboarding and dataset mapping flow' },
  { files: ['frontend/src/pages/demo/DemoBusinessesPage.tsx'], msg: 'feat(pages-demo): implement interactive 14 Demo Businesses environment selector' },
  { files: ['frontend/src/App.tsx', 'frontend/src/main.tsx'], msg: 'feat(frontend-router): assemble full client router and application entrypoint' },
  { files: ['.'], msg: 'chore(release): finalize production build configuration and platform verification' },
];

console.log(`Configured ${commits.length} semantic commits.`);

let count = 0;
for (const c of commits) {
  let hasStaged = false;
  for (const f of c.files) {
    if (f === '.') {
      run('git add -A');
      hasStaged = true;
    } else if (fs.existsSync(f)) {
      run(`git add "${f}"`);
      hasStaged = true;
    }
  }

  // Check if anything is staged
  const status = run('git status --porcelain');
  const staged = status.split('\n').filter(line => line.startsWith('A ') || line.startsWith('M ') || line.startsWith('D ') || line.startsWith('R '));
  if (staged.length > 0) {
    run(`git commit -m "${c.msg}"`);
    count++;
    console.log(`[${count}] Committed: ${c.msg}`);
  }
}

// Any remaining files?
const remaining = run('git status --porcelain');
if (remaining.trim()) {
  run('git add -A');
  run('git commit -m "chore: commit remaining supplementary telemetry assets and configurations"');
  count++;
  console.log(`[${count}] Committed remaining files`);
}

const totalCommits = parseInt(run('git rev-list --count HEAD').trim(), 10);
console.log(`Total commits created: ${totalCommits}`);
