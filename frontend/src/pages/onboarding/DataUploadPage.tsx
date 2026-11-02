import React, { useState } from 'react';
import { UploadCloud, FileArchive, Database, Server, ArrowRight, ShieldCheck } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const DataUploadPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFileName(e.dataTransfer.files[0].name);
    }
  };

  const handleStartProcessing = () => {
    onNavigate('/onboarding/processing');
  };

  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <div className="w-full max-w-3xl space-y-6">
        <div className="text-center space-y-2">
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-bold tracking-widest">
            STEP 2 OF 4 • INGESTION INTAKE
          </span>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-[#F5F0EA]">Connect Your Business Data</h1>
          <p className="text-xs sm:text-sm text-[#A89D92] max-w-xl mx-auto">
            Upload raw multi-dataset ZIP files, spreadsheets, or establish read-only database connections.
          </p>
        </div>

        {/* Drag and Drop Box */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={`p-10 rounded-3xl border-2 border-dashed transition-all duration-300 text-center flex flex-col items-center justify-center cursor-pointer ${
            dragActive
              ? 'border-[#FF6A00] bg-[#FF6A00]/10 shadow-[0_0_35px_rgba(255,106,0,0.3)]'
              : 'border-[#FF6A00]/25 bg-[#120C08]/80 hover:border-[#FF6A00]/60'
          }`}
          onClick={() => {
            setSelectedFileName('PrimeLogix_Aegis_Demo.zip');
          }}
        >
          <div className="w-16 h-16 rounded-2xl bg-[#FF6A00]/15 border border-[#FF6A00]/30 flex items-center justify-center text-[#FF6A00] mb-4">
            <UploadCloud className="w-8 h-8" />
          </div>

          <h3 className="text-lg font-bold text-[#F5F0EA]">
            {selectedFileName ? selectedFileName : 'DROP YOUR BUSINESS DATA'}
          </h3>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Supported archives: <strong className="text-[#FFB15A]">ZIP, CSV, XLSX, Parquet</strong> (up to 2GB)
          </p>

          <div className="mt-6 flex items-center gap-3">
            <span className="px-3 py-1 rounded-full bg-[#17100B] border border-[#FF6A00]/15 text-[11px] font-mono text-[#FF8A24]">
              {selectedFileName ? 'File Ready for Pipeline' : 'Click to Select or Drop File'}
            </span>
          </div>
        </div>

        {/* Alternative: Database Integrations */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { name: 'PostgreSQL Direct', desc: 'Read-only replica connection with RLS', icon: Database },
            { name: 'Snowflake / BigQuery', desc: 'Warehouse federated connector', icon: Server },
            { name: 'REST Telemetry API', desc: 'Continuous webhook streaming intake', icon: Server },
          ].map((conn) => {
            const Icon = conn.icon;
            return (
              <div
                key={conn.name}
                onClick={() => setSelectedFileName('cloud_warehouse_replica.dump')}
                className="p-4 rounded-2xl bg-[#120C08] border border-[#FF6A00]/15 hover:border-[#FF6A00]/40 cursor-pointer transition-all space-y-1 text-xs"
              >
                <div className="flex items-center gap-2 font-mono text-[#FF8A24] font-semibold">
                  <Icon className="w-4 h-4 text-[#FF6A00]" />
                  <span>{conn.name}</span>
                </div>
                <p className="text-[#6F665F] leading-tight">{conn.desc}</p>
              </div>
            );
          })}
        </div>

        {/* Action Controls */}
        <div className="pt-4 flex justify-between items-center">
          <button
            onClick={() => onNavigate('/demo')}
            className="text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
          >
            Or browse 15 pre-loaded demo environments →
          </button>
          <GlowButton
            size="md"
            showArrow
            onClick={handleStartProcessing}
          >
            Launch Ingestion Engine
          </GlowButton>
        </div>
      </div>
    </div>
  );
};

export default DataUploadPage;
