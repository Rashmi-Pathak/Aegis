import React from 'react';
import { Bell, AlertTriangle, Info, CheckCircle, X } from 'lucide-react';
import { AlertItem } from '@/types';

interface NotificationCenterProps {
  isOpen: boolean;
  onClose: () => void;
  alerts: AlertItem[];
  onSelectAlert?: (alert: AlertItem) => void;
}

export const NotificationCenter: React.FC<NotificationCenterProps> = ({
  isOpen,
  onClose,
  alerts,
  onSelectAlert,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-96 z-50 bg-[#0E0A07] border-l border-[#FF6A00]/25 shadow-[0_0_50px_rgba(0,0,0,0.9)] flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="h-16 px-6 border-b border-[#FF6A00]/14 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Bell className="w-4 h-4 text-[#FF6A00]" />
            <h3 className="text-sm font-bold text-[#F5F0EA] font-mono tracking-wide">
              INTELLIGENCE ALERTS
            </h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-[#6F665F] hover:text-[#F5F0EA]">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Alerts list */}
        <div className="p-4 space-y-3 overflow-y-auto max-h-[calc(100vh-140px)]">
          {alerts.length === 0 ? (
            <p className="p-8 text-center text-xs font-mono text-[#6F665F]">No active alerts</p>
          ) : (
            alerts.map((alt) => (
              <div
                key={alt.id}
                onClick={() => onSelectAlert?.(alt)}
                className="p-3.5 rounded-xl bg-[#120C08] border border-[#FF6A00]/18 hover:border-[#FF6A00]/45 cursor-pointer transition-all space-y-1.5"
              >
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <span
                    className={`font-semibold uppercase ${
                      alt.severity === 'critical'
                        ? 'text-[#FF4500]'
                        : alt.severity === 'high'
                        ? 'text-[#FF8A24]'
                        : 'text-[#FFB15A]'
                    }`}
                  >
                    {alt.severity} Priority
                  </span>
                  <span className="text-[#6F665F]">{alt.timestamp}</span>
                </div>
                <h5 className="text-xs font-medium text-[#F5F0EA] leading-snug">{alt.message}</h5>
                <p className="text-[11px] text-[#A89D92]">
                  <strong className="text-[#FFB15A]">Target:</strong> {alt.affectedMetric}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-[#FF6A00]/14 bg-[#080604]/60 flex items-center justify-between text-xs font-mono">
        <span className="text-[#6F665F]">{alerts.length} total signals</span>
        <button className="text-[#FF8A24] hover:text-[#FFB15A] transition-colors">
          Clear All
        </button>
      </div>
    </div>
  );
};

export default NotificationCenter;
