import React, { useState, useEffect } from 'react';
import {
  Search,
  LayoutDashboard,
  ShieldAlert,
  TrendingUp,
  Workflow,
  Sliders,
  Database,
  ArrowRight,
  X,
} from 'lucide-react';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (path: string) => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onNavigate,
}) => {
  const [query, setQuery] = useState('');

  const commands = [
    { label: 'Executive Command Center', path: '/command-center', icon: LayoutDashboard, category: 'Navigation' },
    { label: 'Risk Intelligence Matrix', path: '/risk-center', icon: ShieldAlert, category: 'Risk' },
    { label: '90-Day Revenue Forecast', path: '/forecast-center', icon: TrendingUp, category: 'Forecasting' },
    { label: 'What-If Simulation Engine', path: '/simulation', icon: Workflow, category: 'Simulation' },
    { label: 'Decision Queue & Authorizations', path: '/decision-center', icon: Sliders, category: 'Decisions' },
    { label: 'Data Ingestion & Schemas', path: '/data-center', icon: Database, category: 'Data' },
  ];

  const filtered = commands.filter((cmd) =>
    cmd.label.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/75 backdrop-blur-md">
      <div className="w-full max-w-xl rounded-2xl bg-[#120C08] border border-[#FF6A00]/30 shadow-[0_20px_60px_rgba(0,0,0,0.9)] overflow-hidden">
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3 border-b border-[#FF6A00]/15 gap-3">
          <Search className="w-5 h-5 text-[#FF6A00]" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search intelligence platform or jump to section..."
            className="w-full bg-transparent text-sm text-[#F5F0EA] placeholder-[#6F665F] font-mono focus:outline-none"
          />
          <button onClick={onClose} className="p-1 rounded-lg text-[#6F665F] hover:text-[#F5F0EA]">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="p-2 max-h-80 overflow-y-auto space-y-1">
          {filtered.length === 0 ? (
            <p className="p-4 text-center text-xs font-mono text-[#6F665F]">No matching commands found</p>
          ) : (
            filtered.map((cmd) => {
              const Icon = cmd.icon;
              return (
                <button
                  key={cmd.path}
                  onClick={() => {
                    onNavigate(cmd.path);
                    onClose();
                  }}
                  className="w-full px-3 py-2.5 rounded-xl flex items-center justify-between text-left text-xs hover:bg-[#FF6A00]/15 text-[#A89D92] hover:text-[#F5F0EA] transition-colors group font-mono"
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 text-[#FF6A00]" />
                    <span className="font-sans font-medium text-sm text-[#F5F0EA]">{cmd.label}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-[#6F665F] uppercase">{cmd.category}</span>
                    <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 text-[#FF8A24] transition-all" />
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 border-t border-[#FF6A00]/10 bg-[#080604]/50 flex items-center justify-between text-[11px] font-mono text-[#6F665F]">
          <span>Use arrow keys to navigate</span>
          <span>ESC to close</span>
        </div>
      </div>
    </div>
  );
};

export default CommandPalette;
