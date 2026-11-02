export interface User {
  id: string;
  email: string;
  name: string;
  role: 'super_admin' | 'admin' | 'analyst' | 'executive' | 'viewer';
  organizationId: string;
  avatarUrl?: string;
  createdAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  industry: string;
  tier: 'starter' | 'growth' | 'enterprise';
  healthScore: number;
  dataQualityScore: number;
  activeRisksCount: number;
  createdAt: string;
}

export interface DemoBusiness {
  id: string;
  name: string;
  industry: string;
  tagline: string;
  description: string;
  zipFileName: string;
  datasetCount: number;
  recordCount: number;
  healthScore: number;
  riskCount: number;
  primaryRiskStory: {
    trigger: string;
    causalChain: string[];
    affectedMetrics: string[];
    potentialImpact: string;
  };
  metrics: {
    revenue: string;
    growth: string;
    margin: string;
    runway: string;
  };
}

export interface MetricSummary {
  title: string;
  value: string | number;
  changePercent: number;
  trend: 'up' | 'down' | 'neutral';
  timeframe: string;
  forecast?: string | number;
  isAnomaly?: boolean;
}

export interface AnomalyItem {
  id: string;
  metric: string;
  detectedAt: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  deviationScore: number;
  expectedValue: number | string;
  actualValue: number | string;
  explanation: string;
  rootCauseCandidate: string;
}

export interface RiskItem {
  id: string;
  title: string;
  category: 'financial' | 'operational' | 'supply_chain' | 'market' | 'customer';
  severity: 'critical' | 'high' | 'medium' | 'low';
  score: number; // 0-100
  probability: number; // 0-1
  impact: number; // 0-100
  exposureAmount: string;
  detectedAt: string;
  status: 'active' | 'investigating' | 'mitigated' | 'accepted';
  primaryDrivers: string[];
  secondaryDrivers: string[];
  affectedAreas: string[];
  recommendedActions: string[];
}

export interface ForecastItem {
  id: string;
  metric: string;
  horizonDays: number;
  modelUsed: string;
  confidenceScore: number; // 0-1
  historical: { date: string; value: number }[];
  forecast: { date: string; value: number; lowerBound: number; upperBound: number }[];
  accuracyMetrics: {
    mae: number;
    rmse: number;
    mape: string;
  };
}

export interface DecisionItem {
  id: string;
  title: string;
  type: 'procurement' | 'pricing' | 'marketing' | 'operations' | 'budget';
  recommendation: string;
  reasoning: string;
  expectedImpact: string;
  riskReduction: string;
  confidence: number;
  status: 'pending' | 'approved' | 'rejected' | 'simulated';
  requiresHumanApproval: boolean;
  estimatedRoi: string;
  simulatedScenarioId?: string;
}

export interface SimulationParams {
  marketingSpendDelta: number; // %
  priceDelta: number; // %
  discountDelta: number; // %
  hiringDelta: number; // head count
  procurementDelta: number; // %
  inventoryBufferDelta: number; // %
}

export interface SimulationResult {
  baselineRevenue: number;
  simulatedRevenue: number;
  baselineProfit: number;
  simulatedProfit: number;
  baselineCashFlow: number;
  simulatedCashFlow: number;
  baselineRiskScore: number;
  simulatedRiskScore: number;
  tradeoffs: string[];
  confidence: number;
}

export interface BusinessGraphNode {
  id: string;
  label: string;
  category: 'revenue' | 'customers' | 'operations' | 'marketing' | 'finance' | 'supply_chain';
  status: 'normal' | 'warning' | 'critical';
  value: string;
  riskScore: number;
  dependencies: string[];
}

export interface BusinessGraphEdge {
  source: string;
  target: string;
  weight: number;
  relationship: string;
  isStressed?: boolean;
}

export interface DatasetItem {
  id: string;
  name: string;
  sourceType: 'zip' | 'csv' | 'excel' | 'postgres' | 'api';
  recordCount: number;
  columnCount: number;
  qualityScore: number;
  lastUpdated: string;
  status: 'ready' | 'processing' | 'error';
  schema: {
    name: string;
    type: string;
    nullPercentage: number;
    hasOutliers: boolean;
  }[];
}

export interface ModelIntelligenceItem {
  id: string;
  name: string;
  type: 'forecasting' | 'anomaly_detection' | 'risk_scoring' | 'causal_inference';
  version: string;
  accuracy: string;
  f1Score?: string;
  mae?: string;
  rmse?: string;
  driftStatus: 'stable' | 'slight_drift' | 'retrain_recommended';
  lastTrained: string;
}

export interface ReportItem {
  id: string;
  title: string;
  category: 'executive' | 'risk' | 'forecast' | 'data_quality' | 'decision';
  generatedAt: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'on_demand';
  status: 'ready' | 'generating';
  summary: string;
}

export interface AlertItem {
  id: string;
  timestamp: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  source: string;
  message: string;
  affectedMetric: string;
  actionRequired: string;
  isRead: boolean;
}
