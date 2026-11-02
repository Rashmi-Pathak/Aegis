import React, { useState, useEffect } from 'react';
import { CheckCircle2, RefreshCw, ArrowRight, ShieldCheck, Cpu } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const DataProcessingPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const steps = [
    { id: 1, label: 'FILE RECEIVED', desc: 'PrimeLogix_Aegis_Demo.zip validated & uncompressed' },
    { id: 2, label: 'DATASETS DETECTED', desc: '8 heterogeneous operational datasets discovered' },
    { id: 3, label: 'SCHEMA ANALYZED', desc: '428,000 tabular records parsed and type-inferred' },
    { id: 4, label: 'DATA QUALITY CHECK', desc: '0 duplicate primary keys, 4 outlier records isolated' },
    { id: 5, label: 'RELATIONSHIPS FOUND', desc: '14 multi-table foreign keys and causal links mapped' },
    { id: 6, label: 'BUSINESS MODEL BUILT', desc: 'Canonical digital twin instantiated in memory' },
    { id: 7, label: 'AEGIS READY', desc: 'Executive Command Center initialized' },
  ];

  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length) {
          return prev + 1;
        } else {
          clearInterval(timer);
          return prev;
        }
      });
    }, 700);

    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <div className="w-full max-w-2xl space-y-8">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#120C08] border border-[#FF6A00]/30 text-xs font-mono text-[#FF8A24]">
            <Cpu className="w-3.5 h-3.5 text-[#FF6A00] animate-spin" />
            <span>PYTHON INGESTION WORKER EXECUTING</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA]">
            Synthesizing Business Digital Twin
          </h1>
          <p className="text-xs text-[#A89D92]">
            Please wait while AEGIS parses and structures your enterprise data pipeline.
          </p>
        </div>

        <GlowCard className="p-8 space-y-5">
          <div className="space-y-4">
            {steps.map((step) => {
              const isCompleted = step.id <= currentStep;
              const isCurrent = step.id === currentStep;

              return (
                <div
                  key={step.id}
                  className={`p-3.5 rounded-xl border transition-all duration-300 flex items-center justify-between ${
                    isCompleted
                      ? 'bg-[#17100B] border-[#FF6A00]/40 shadow-[0_0_15px_rgba(255,106,0,0.1)]'
                      : 'bg-[#080604] border-[#FF6A00]/10 opacity-40'
                  }`}
                >
                  <div className="flex items-center gap-3.5">
                    <div
                      className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-xs font-bold ${
                        isCompleted
                          ? 'bg-[#FF6A00] text-white shadow-[0_0_10px_#FF6A00]'
                          : 'bg-[#120C08] text-[#6F665F]'
                      }`}
                    >
                      {isCompleted ? <CheckCircle2 className="w-4 h-4" /> : step.id}
                    </div>
                    <div>
                      <h4
                        className={`text-xs font-mono font-bold tracking-wider ${
                          isCompleted ? 'text-[#FFB15A]' : 'text-[#6F665F]'
                        }`}
                      >
                        {step.label}
                      </h4>
                      <p className="text-[11px] text-[#A89D92]">{step.desc}</p>
                    </div>
                  </div>

                  {isCurrent && currentStep < steps.length && (
                    <RefreshCw className="w-4 h-4 text-[#FF8A24] animate-spin" />
                  )}
                </div>
              );
            })}
          </div>

          {currentStep >= steps.length && (
            <div className="pt-4 border-t border-[#FF6A00]/14 text-center animate-in fade-in duration-300">
              <GlowButton
                size="lg"
                showArrow
                className="w-full"
                onClick={() => onNavigate('/command-center')}
              >
                ENTER COMMAND CENTER
              </GlowButton>
            </div>
          )}
        </GlowCard>
      </div>
    </div>
  );
};

export default DataProcessingPage;
