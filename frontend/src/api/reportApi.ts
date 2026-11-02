import apiClient from './client';
import { ReportItem, AlertItem } from '@/types';

export const reportApi = {
  async getReports(): Promise<ReportItem[]> {
    try {
      return await apiClient<ReportItem[]>('/reports');
    } catch {
      return [
        {
          id: 'rep_exec_q1',
          title: 'Executive Risk & Capital Intelligence Briefing',
          category: 'executive',
          generatedAt: 'Today, 06:00 UTC',
          frequency: 'weekly',
          status: 'ready',
          summary: 'Synthesis of cross-business margins, exposure vectors, diesel hedging recommendation, and 90-day cash flow scenario.',
        },
        {
          id: 'rep_fuel_surge',
          title: 'Commodity & Energy Price Exposure Audit',
          category: 'risk',
          generatedAt: 'Yesterday, 18:30 UTC',
          frequency: 'on_demand',
          status: 'ready',
          summary: 'Causal propagation analysis from crude futures into carrier spot surcharges and SLA penalties.',
        },
        {
          id: 'rep_forecast_q2',
          title: '90-Day Multi-Horizon Demand & Fleet Capacity Forecast',
          category: 'forecast',
          generatedAt: '2 days ago',
          frequency: 'monthly',
          status: 'ready',
          summary: 'Trained ensemble models predicting lane-level freight demand, seasonal variance, and terminal storage capacity.',
        },
        {
          id: 'rep_quality_mar',
          title: 'Canonical Data Quality & Ingestion Integrity Report',
          category: 'data_quality',
          generatedAt: '3 days ago',
          frequency: 'weekly',
          status: 'ready',
          summary: 'Validation analysis across 8 enterprise datasets: 96.8% health score, 0 duplicate keys, 4 outlier records isolated.',
        },
      ];
    }
  },
};

export const alertApi = {
  async getAlerts(): Promise<AlertItem[]> {
    try {
      return await apiClient<AlertItem[]>('/alerts');
    } catch {
      return [
        {
          id: 'alt_01',
          timestamp: '12m ago',
          severity: 'critical',
          source: 'Risk Engine - Energy Module',
          message: 'Fuel expense benchmark exceeded +15% alert threshold on Southwest corridor.',
          affectedMetric: 'Operating Margin ($2.85M Exposure)',
          actionRequired: 'Review Decision #DEC-01 (Rail Reroute)',
          isRead: false,
        },
        {
          id: 'alt_02',
          timestamp: '1h ago',
          severity: 'high',
          source: 'Anomaly Detector - Logistics EDI',
          message: 'Demurrage charges accelerated to $18.6K/day at Long Beach Terminal 4.',
          affectedMetric: 'Intermodal Dwell Fees',
          actionRequired: 'Trigger pre-clearance EDI customs expedite',
          isRead: false,
        },
        {
          id: 'alt_03',
          timestamp: '4h ago',
          severity: 'medium',
          source: 'Forecasting Engine',
          message: 'Q2 revenue confidence interval expanded to ±4.2% due to supplier pricing volatility.',
          affectedMetric: 'Revenue Predictability',
          actionRequired: 'Run What-If Scenario with +10% cost variance',
          isRead: true,
        },
      ];
    }
  },
};

export default reportApi;
