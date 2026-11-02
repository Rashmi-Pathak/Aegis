import apiClient from './client';
import { MetricSummary } from '@/types';

export interface AnalyticsOverview {
  healthScore: number;
  kpis: {
    revenue: MetricSummary;
    operatingMargin: MetricSummary;
    cashFlow: MetricSummary;
    customerHealth: MetricSummary;
    inventoryTurnover: MetricSummary;
    fuelCostRatio: MetricSummary;
  };
  revenueTrend: { date: string; actual: number; target: number }[];
  marginBreakdown: { category: string; value: number }[];
  categoryPerformance: { name: string; revenue: number; margin: number; riskScore: number }[];
}

export const analyticsApi = {
  async getOverview(): Promise<AnalyticsOverview> {
    try {
      return await apiClient<AnalyticsOverview>('/analytics/overview');
    } catch {
      return {
        healthScore: 78,
        kpis: {
          revenue: {
            title: 'Gross Operating Revenue',
            value: '$148.24M',
            changePercent: 8.4,
            trend: 'up',
            timeframe: 'vs prior quarter',
          },
          operatingMargin: {
            title: 'Operating Profit Margin',
            value: '14.2%',
            changePercent: -2.8,
            trend: 'down',
            timeframe: 'compression detected',
            isAnomaly: true,
          },
          cashFlow: {
            title: 'Free Cash Flow',
            value: '$18.65M',
            changePercent: -4.1,
            trend: 'down',
            timeframe: '30-day run rate',
          },
          customerHealth: {
            title: 'Key Client Retention',
            value: '94.8%',
            changePercent: 1.2,
            trend: 'up',
            timeframe: 'top 50 corporate accounts',
          },
          inventoryTurnover: {
            title: 'Fleet Asset Utilization',
            value: '84.6%',
            changePercent: -3.4,
            trend: 'down',
            timeframe: 'trailing 90 days',
          },
          fuelCostRatio: {
            title: 'Energy / Fuel Expense',
            value: '28.4%',
            changePercent: 14.8,
            trend: 'up',
            timeframe: 'benchmark deviation',
            isAnomaly: true,
          },
        },
        revenueTrend: [
          { date: 'Oct', actual: 38.2, target: 36.5 },
          { date: 'Nov', actual: 41.5, target: 40.0 },
          { date: 'Dec', actual: 47.8, target: 45.2 },
          { date: 'Jan', actual: 39.4, target: 42.0 },
          { date: 'Feb', actual: 42.6, target: 43.5 },
          { date: 'Mar', actual: 48.2, target: 46.0 },
        ],
        marginBreakdown: [
          { category: 'Freight Haulage', value: 48 },
          { category: 'Dedicated Warehousing', value: 24 },
          { category: 'Cold-Chain Pharma', value: 18 },
          { category: 'Customs Brokerage', value: 10 },
        ],
        categoryPerformance: [
          { name: 'Transcontinental Heavy Rail', revenue: 42.5, margin: 18.2, riskScore: 28 },
          { name: 'Cross-Border Truckload (TL)', revenue: 58.4, margin: 11.4, riskScore: 68 },
          { name: 'Temperature Controlled Bio', revenue: 27.6, margin: 26.8, riskScore: 22 },
          { name: 'Last-Mile Micro Distribution', revenue: 19.7, margin: 8.5, riskScore: 74 },
        ],
      };
    }
  },

  async getRevenueData() {
    try {
      return await apiClient('/analytics/revenue');
    } catch {
      return (await this.getOverview()).revenueTrend;
    }
  },
};

export default analyticsApi;
