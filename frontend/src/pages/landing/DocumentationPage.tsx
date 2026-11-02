import React from 'react';
import { ArrowLeft, BookOpen, Code, Terminal, FileText } from 'lucide-react';

export const DocumentationPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 max-w-6xl mx-auto">
      <button
        onClick={() => onNavigate('/')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A] mb-8"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Home
      </button>

      <div className="mb-10 space-y-3">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-widest">
          DEVELOPER & ARCHITECT MANUAL
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">AEGIS Platform Docs</h1>
        <p className="text-sm text-[#A89D92] max-w-2xl">
          Complete guides for data schema integration, API endpoints, Python ML pipelines, and multi-tenant security architecture.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[
          {
            title: 'Canonical Data Ingestion & Schemas',
            desc: 'Specifications for mapping custom business records into the standardized AEGIS internal canonical models.',
            icon: FileText,
            link: '/data-center',
          },
          {
            title: 'Risk Engine & Scoring Algorithms',
            desc: 'Mathematical formulas for Probability × Impact × Exposure calculation and multi-variate threat matrices.',
            icon: Terminal,
            link: '/risk-center',
          },
          {
            title: 'Forecasting & Time-Series Models',
            desc: 'Ensemble model training, hyperparameter validation, and confidence interval estimation methods.',
            icon: Code,
            link: '/forecast-center',
          },
          {
            title: 'Causal Graph Digital Twin',
            desc: 'Topological dependency mapping with NetworkX for root-cause tracking across business nodes.',
            icon: BookOpen,
            link: '/business-graph',
          },
        ].map((doc) => {
          const Icon = doc.icon;
          return (
            <div
              key={doc.title}
              onClick={() => onNavigate(doc.link)}
              className="p-6 rounded-2xl bg-[#120C08] border border-[#FF6A00]/16 hover:border-[#FF6A00]/50 cursor-pointer transition-all space-y-3 group"
            >
              <div className="w-10 h-10 rounded-xl bg-[#FF6A00]/15 flex items-center justify-center text-[#FF6A00] group-hover:scale-110 transition-transform">
                <Icon className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-[#F5F0EA] group-hover:text-[#FFB15A] transition-colors">
                {doc.title}
              </h3>
              <p className="text-xs text-[#A89D92] leading-relaxed">{doc.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DocumentationPage;
