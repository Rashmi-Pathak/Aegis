import apiClient from './client';
import { BusinessGraphNode, BusinessGraphEdge } from '@/types';

export interface BusinessGraphData {
  nodes: BusinessGraphNode[];
  edges: BusinessGraphEdge[];
}

export const graphApi = {
  async getBusinessGraph(): Promise<BusinessGraphData> {
    try {
      return await apiClient<BusinessGraphData>('/graph/business-digital-twin');
    } catch {
      return {
        nodes: [
          { id: 'fuel_energy', label: 'Fuel & Energy Index', category: 'supply_chain', status: 'critical', value: '+28% Cost', riskScore: 88, dependencies: ['fleet_ops', 'operating_costs'] },
          { id: 'fleet_ops', label: 'Fleet Operations', category: 'operations', status: 'warning', value: '84% Util', riskScore: 72, dependencies: ['deliveries', 'driver_capacity'] },
          { id: 'driver_capacity', label: 'Driver Capacity', category: 'operations', status: 'warning', value: '92% Active', riskScore: 64, dependencies: ['fleet_ops'] },
          { id: 'deliveries', label: 'On-Time Deliveries (OTIF)', category: 'operations', status: 'normal', value: '96.2%', riskScore: 32, dependencies: ['client_retention', 'revenue'] },
          { id: 'client_retention', label: 'Client Retention', category: 'customers', status: 'normal', value: '94.8%', riskScore: 28, dependencies: ['revenue'] },
          { id: 'operating_costs', label: 'Operating Cost Base', category: 'finance', status: 'critical', value: '$127M', riskScore: 82, dependencies: ['gross_margin', 'cash_flow'] },
          { id: 'revenue', label: 'Gross Revenue', category: 'revenue', status: 'normal', value: '$148.2M', riskScore: 34, dependencies: ['gross_margin', 'cash_flow'] },
          { id: 'gross_margin', label: 'Gross Profit Margin', category: 'finance', status: 'critical', value: '14.2%', riskScore: 86, dependencies: ['cash_flow'] },
          { id: 'cash_flow', label: 'Free Cash Flow', category: 'finance', status: 'warning', value: '$18.6M', riskScore: 68, dependencies: [] },
          { id: 'warehousing', label: 'Terminal Warehousing', category: 'supply_chain', status: 'normal', value: '78% Cap', riskScore: 30, dependencies: ['operating_costs'] },
          { id: 'marketing_sales', label: 'Enterprise Contract Sales', category: 'marketing', status: 'normal', value: '+$12M Pipe', riskScore: 25, dependencies: ['revenue'] },
        ],
        edges: [
          { source: 'fuel_energy', target: 'operating_costs', weight: 0.85, relationship: 'Direct Cost Inflator', isStressed: true },
          { source: 'fuel_energy', target: 'fleet_ops', weight: 0.65, relationship: 'Speed/Idling Route Policy', isStressed: true },
          { source: 'driver_capacity', target: 'fleet_ops', weight: 0.78, relationship: 'Dispatch Feasibility' },
          { source: 'fleet_ops', target: 'deliveries', weight: 0.9, relationship: 'SLA Performance' },
          { source: 'deliveries', target: 'client_retention', weight: 0.82, relationship: 'Service Quality Trust' },
          { source: 'client_retention', target: 'revenue', weight: 0.94, relationship: 'Recurring Billable Volume' },
          { source: 'marketing_sales', target: 'revenue', weight: 0.6, relationship: 'New Contract Growth' },
          { source: 'revenue', target: 'gross_margin', weight: 0.95, relationship: 'Topline Inflow' },
          { source: 'operating_costs', target: 'gross_margin', weight: 0.92, relationship: 'Margin Compression', isStressed: true },
          { source: 'gross_margin', target: 'cash_flow', weight: 0.88, relationship: 'Operating Surplus Flow', isStressed: true },
          { source: 'warehousing', target: 'operating_costs', weight: 0.45, relationship: 'Facility Overhead' },
        ],
      };
    }
  },
};

export default graphApi;
