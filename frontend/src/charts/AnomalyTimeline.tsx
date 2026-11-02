import React, { useState } from 'react';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

interface AnomalyEvent {
  id: string;
  timestamp: string;
  isAnomaly: boolean;
  metric: string;
  value: string;
  deviation: string;
  explanation?: string;
}

const sampleTimeline: AnomalyEvent[] = [
  { id: '1', timestamp: '08:00', isAnomaly: false, metric: 'Engine Idle Rate', value: '4.2%', deviation: '0.1σ' },
  { id: '2', timestamp: '09:15', isAnomaly: false, metric: 'Dispatch Transit Time', value: '1.4h', deviation: '0.3σ' },
  { id: '3', timestamp: '10:42', isAnomaly: true, metric: 'Fuel Expense Spike', value: '$0.84/mi', deviation: '3.8σ', explanation: 'Sudden wholesale pump surge detected in Houston depot' },
  { id: '4', timestamp: '11:30', isAnomaly: false, metric: 'Trailer Temperature', value: '-18°C', deviation: '0.2σ' },
  { id: '5', timestamp: '13:05', isAnomaly: true, metric: 'Port Demurrage Hold', value: '$18.6K/day', deviation: '2.9σ', explanation: 'Container gate hold exceeded 72-hour free dwell SLA' },
  { id: '6', timestamp: '14:20', isAnomaly: false, metric: 'Highway Speed Avg', value: '62 mph', deviation: '0.4σ' },
  { id: '7', timestamp: '16:10', isAnomaly: true, metric: 'Order Cancellation', value: '3.7%', deviation: '2.2σ', explanation: 'Shipper load drop cascade triggered by border delay' },
  { id: '8', timestamp: '17:45', isAnomaly: false, metric: 'Terminal Fuel Surcharge', value: '18.4%', deviation: '0.5σ' },
];

export const AnomalyTimeline: React.FC = () => {
  const [activeEvent, setActiveEvent] = useState<AnomalyEvent | null>(sampleTimeline[2]);

  return (
    <div className="w-full space-y-4">
      {/* Horizontal Interactive Timeline Track */}
      <div className="relative py-8 px-4 bg-[#120C08]/80 border border-[#FF6A00]/16 rounded-2xl backdrop-blur-md">
        {/* Connecting Track Line */}
        <div className="absolute top-1/2 left-8 right-8 h-[2px] bg-gradient-to-r from-[#FF6A00]/10 via-[#FF6A00]/40 to-[#FF6A00]/10 -translate-y-1/2" />

        <div className="relative flex items-center justify-between z-10">
          {sampleTimeline.map((ev) => {
            const isSelected = activeEvent?.id === ev.id;
            return (
              <div
                key={ev.id}
                onClick={() => setActiveEvent(ev)}
                className="flex flex-col items-center cursor-pointer group"
              >
                {/* Time Label */}
                <span className="text-[10px] font-mono text-[#6F665F] mb-3 group-hover:text-[#A89D92]">
                  {ev.timestamp}
                </span>

                {/* Node Dot */}
                <div
                  className={`w-4 h-4 rounded-full flex items-center justify-center transition-all duration-300 ${
                    ev.isAnomaly
                      ? 'bg-[#FF4500] ring-4 ring-[#FF6A00]/30 shadow-[0_0_12px_#FF6A00] animate-pulse'
                      : 'bg-[#17100B] border border-[#FF6A00]/25 group-hover:border-[#FF6A00]/60'
                  } ${isSelected ? 'scale-125 ring-2 ring-[#FFB15A]' : ''}`}
                >
                  {ev.isAnomaly ? (
                    <div className="w-1.5 h-1.5 rounded-full bg-white" />
                  ) : (
                    <div className="w-1 h-1 rounded-full bg-[#A89D92]" />
                  )}
                </div>

                {/* Status indicator */}
                <span
                  className={`text-[9px] font-mono mt-3 uppercase tracking-wider ${
                    ev.isAnomaly ? 'text-[#FF8A24] font-bold' : 'text-[#6F665F]'
                  }`}
                >
                  {ev.isAnomaly ? 'Anomaly' : 'Normal'}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Selected Anomaly Deep-Dive Callout */}
      {activeEvent && (
        <div className="p-4 rounded-xl bg-[#0D0906] border border-[#FF6A00]/25 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div
              className={`p-2 rounded-lg ${
                activeEvent.isAnomaly
                  ? 'bg-[#FF4500]/15 text-[#FF6A00] border border-[#FF6A00]/30'
                  : 'bg-[#6F665F]/15 text-[#A89D92]'
              }`}
            >
              {activeEvent.isAnomaly ? (
                <AlertCircle className="w-5 h-5" />
              ) : (
                <CheckCircle2 className="w-5 h-5" />
              )}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h5 className="text-sm font-semibold text-[#F5F0EA]">{activeEvent.metric}</h5>
                <span className="text-xs font-mono text-[#FFB15A]">({activeEvent.timestamp})</span>
              </div>
              <p className="text-xs text-[#A89D92] mt-0.5 font-mono">
                Observed: <strong className="text-[#F5F0EA]">{activeEvent.value}</strong> • Deviation: {activeEvent.deviation}
              </p>
              {activeEvent.explanation && (
                <p className="text-xs text-[#FF8A24] mt-1">{activeEvent.explanation}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnomalyTimeline;
