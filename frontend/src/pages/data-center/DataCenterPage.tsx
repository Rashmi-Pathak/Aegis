import React, { useState, useEffect } from 'react';
import { Database, Upload, CheckCircle2, AlertCircle, FileSpreadsheet, RefreshCw, Layers } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import DataTable from '@/components/DataTable';
import { datasetApi } from '@/api/datasetApi';
import { DatasetItem } from '@/types';

export const DataCenterPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [datasets, setDatasets] = useState<DatasetItem[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<DatasetItem | null>(null);

  useEffect(() => {
    datasetApi.getDatasets().then((ds) => {
      setDatasets(ds);
      setSelectedDataset(ds[0]);
    });
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            DATA INGESTION & QUALITY PIPELINE
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Data Center & Ingestion Intelligence
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Automated schema mapping, type inference, outlier validation, and canonical transformation.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/onboarding/upload')}
          >
            <Upload className="w-4 h-4 mr-1.5" />
            Upload New ZIP / CSV
          </GlowButton>
        </div>
      </div>

      {/* Dataset Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {datasets.map((d) => {
          const isSelected = selectedDataset?.id === d.id;
          return (
            <div
              key={d.id}
              onClick={() => setSelectedDataset(d)}
              className={`p-6 rounded-2xl bg-[#120C08] border transition-all duration-200 cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'border-[#FF6A00] shadow-[0_0_20px_rgba(255,106,0,0.25)] bg-[#17100B]'
                  : 'border-[#FF6A00]/16 hover:border-[#FF6A00]/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between font-mono text-xs mb-3">
                  <span className="px-2 py-0.5 rounded-full uppercase bg-[#FF6A00]/15 text-[#FF8A24] text-[10px] font-bold">
                    {d.sourceType} SOURCE
                  </span>
                  <span className="text-[#6F665F]">{d.lastUpdated}</span>
                </div>
                <h4 className="text-base font-bold text-[#F5F0EA]">{d.name}</h4>
                <p className="text-xs text-[#A89D92] font-mono mt-1">
                  {d.recordCount.toLocaleString()} Records • {d.columnCount} Columns
                </p>
              </div>

              <div className="mt-5 pt-3 border-t border-[#FF6A00]/12 flex items-center justify-between text-xs font-mono">
                <div>
                  <span className="text-[10px] text-[#6F665F] uppercase block">Data Health</span>
                  <span className="font-bold text-[#FFB15A]">{d.qualityScore}% Quality</span>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Canonical Ready</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Dataset Detail & Schema Table */}
      {selectedDataset && (
        <GlowCard className="space-y-5">
          <div className="flex items-center justify-between border-b border-[#FF6A00]/14 pb-4">
            <div>
              <h3 className="text-lg font-bold text-[#F5F0EA]">
                Schema Specification: {selectedDataset.name}
              </h3>
              <p className="text-xs font-mono text-[#A89D92]">
                Canonical Column Mapping, Null Tolerances & Outlier Detection
              </p>
            </div>
            <span className="text-xs font-mono text-[#FF8A24] bg-[#FF6A00]/15 px-3 py-1 rounded-full">
              {selectedDataset.schema.length} Canonical Fields
            </span>
          </div>

          <DataTable
            columns={[
              { key: 'name', header: 'Column Name' },
              {
                key: 'type',
                header: 'Inferred Data Type',
                render: (row) => <span className="font-mono text-[#FFB15A]">{row.type}</span>,
              },
              {
                key: 'nullPercentage',
                header: 'Null %',
                render: (row) => (
                  <span className="font-mono text-[#A89D92]">{row.nullPercentage}%</span>
                ),
              },
              {
                key: 'hasOutliers',
                header: 'Outlier Anomaly Status',
                render: (row) => (
                  <span
                    className={`font-mono text-xs font-bold ${
                      row.hasOutliers ? 'text-[#FF4500]' : 'text-emerald-400'
                    }`}
                  >
                    {row.hasOutliers ? 'Isolated' : 'Clean'}
                  </span>
                ),
              },
            ]}
            data={selectedDataset.schema}
            keyExtractor={(row) => row.name}
          />
        </GlowCard>
      )}
    </div>
  );
};

export default DataCenterPage;
