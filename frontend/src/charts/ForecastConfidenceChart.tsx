import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const confData = [
  { horizon: 'Day 10', confidence: 98, interval: 2 },
  { horizon: 'Day 30', confidence: 95, interval: 4 },
  { horizon: 'Day 60', confidence: 91, interval: 7 },
  { horizon: 'Day 90', confidence: 86, interval: 11 },
  { horizon: 'Day 120', confidence: 81, interval: 15 },
];

export const ForecastConfidenceChart: React.FC<{ height?: number }> = ({ height = 240 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={confData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="horizon" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} domain={[70, 100]} tickFormatter={(v) => `${v}%`} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#120C08',
              borderColor: 'rgba(255,106,0,0.3)',
              borderRadius: '12px',
              color: '#F5F0EA',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
          />
          <Area type="monotone" dataKey="confidence" stroke="#FF8A24" strokeWidth={2} fill="rgba(255,138,36,0.2)" name="Model Confidence %" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ForecastConfidenceChart;
