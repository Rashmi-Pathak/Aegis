import apiClient from './client';
import { DatasetItem, ModelIntelligenceItem } from '@/types';

export const datasetApi = {
  async getDatasets(): Promise<DatasetItem[]> {
    try {
      return await apiClient<DatasetItem[]>('/datasets');
    } catch {
      return [
        {
          id: 'ds_freight_telemetry',
          name: 'Fleet IoT & GPS Telemetry Feed',
          sourceType: 'api',
          recordCount: 284000,
          columnCount: 18,
          qualityScore: 98,
          lastUpdated: '12m ago',
          status: 'ready',
          schema: [
            { name: 'vehicle_vin', type: 'VARCHAR(17)', nullPercentage: 0, hasOutliers: false },
            { name: 'timestamp', type: 'TIMESTAMP', nullPercentage: 0, hasOutliers: false },
            { name: 'speed_mph', type: 'FLOAT', nullPercentage: 0.1, hasOutliers: true },
            { name: 'fuel_rate_gph', type: 'FLOAT', nullPercentage: 0.4, hasOutliers: true },
            { name: 'engine_load_pct', type: 'FLOAT', nullPercentage: 0.2, hasOutliers: false },
          ],
        },
        {
          id: 'ds_tms_billing',
          name: 'TMS Shipping Orders & Invoicing',
          sourceType: 'postgres',
          recordCount: 89400,
          columnCount: 24,
          qualityScore: 96,
          lastUpdated: '1h ago',
          status: 'ready',
          schema: [
            { name: 'order_id', type: 'UUID', nullPercentage: 0, hasOutliers: false },
            { name: 'client_id', type: 'VARCHAR(32)', nullPercentage: 0, hasOutliers: false },
            { name: 'origin_hub', type: 'VARCHAR(8)', nullPercentage: 0, hasOutliers: false },
            { name: 'dest_hub', type: 'VARCHAR(8)', nullPercentage: 0, hasOutliers: false },
            { name: 'contract_rate_usd', type: 'DECIMAL(12,2)', nullPercentage: 0, hasOutliers: false },
            { name: 'fuel_surcharge_usd', type: 'DECIMAL(10,2)', nullPercentage: 1.2, hasOutliers: true },
          ],
        },
        {
          id: 'ds_customs_edi',
          name: 'EDI-214 Carrier Shipment Status Messages',
          sourceType: 'zip',
          recordCount: 54600,
          columnCount: 14,
          qualityScore: 94,
          lastUpdated: '3h ago',
          status: 'ready',
          schema: [
            { name: 'shipment_id', type: 'VARCHAR(32)', nullPercentage: 0, hasOutliers: false },
            { name: 'status_code', type: 'VARCHAR(4)', nullPercentage: 0, hasOutliers: false },
            { name: 'terminal_code', type: 'VARCHAR(8)', nullPercentage: 0.8, hasOutliers: false },
            { name: 'dwell_hours', type: 'INTEGER', nullPercentage: 0, hasOutliers: true },
          ],
        },
      ];
    }
  },

  async uploadDataset(file: File): Promise<{ jobId: string; status: string }> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      return await apiClient('/ingestion/upload', {
        method: 'POST',
        body: formData,
      });
    } catch {
      return {
        jobId: 'job_upload_' + Math.random().toString(36).substring(7),
        status: 'PROCESSING_INGESTION_PIPELINE',
      };
    }
  },
};

export const modelApi = {
  async getModels(): Promise<ModelIntelligenceItem[]> {
    try {
      return await apiClient<ModelIntelligenceItem[]>('/models');
    } catch {
      return [
        {
          id: 'mdl_revenue_ensemble',
          name: 'Multi-Horizon Topline Forecast (LightGBM + ARIMA)',
          type: 'forecasting',
          version: 'v2.4.1',
          accuracy: '97.2%',
          mae: '$0.28M',
          rmse: '$0.41M',
          driftStatus: 'stable',
          lastTrained: 'Yesterday, 02:00 UTC',
        },
        {
          id: 'mdl_iforest_anom',
          name: 'High-Dimensional Isolation Forest & LOF',
          type: 'anomaly_detection',
          version: 'v1.8.0',
          accuracy: '98.5%',
          f1Score: '0.94',
          driftStatus: 'stable',
          lastTrained: '3 days ago',
        },
        {
          id: 'mdl_risk_scoring',
          name: 'Multi-Factor Enterprise Risk & Exposure Engine',
          type: 'risk_scoring',
          version: 'v3.1.0',
          accuracy: '95.8%',
          driftStatus: 'stable',
          lastTrained: 'Weekly Sunday Cycle',
        },
        {
          id: 'mdl_causal_graph',
          name: 'NetworkX Causal Propagation & Root Cause Graph',
          type: 'causal_inference',
          version: 'v2.0.2',
          accuracy: '94.1%',
          driftStatus: 'stable',
          lastTrained: 'Continuous Graph Updates',
        },
      ];
    }
  },
};

export default datasetApi;
