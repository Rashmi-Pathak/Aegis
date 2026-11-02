import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine,
} from 'recharts';

interface RevenueForecastChartProps {
  height?: number;
}

const forecastData = [
  { period: 'W1', actual: 11.2, forecast: null, lower: null, upper: null },
  { period: 'W2', actual: 11.8, forecast: null, lower: null, upper: null },
  { period: 'W3', actual: 12.1, forecast: null, lower: null, upper: null },
  { period: 'W4', actual: 12.0, forecast: null, lower: null, upper: null },
  { period: 'W5', actual: 12.5, forecast: null, lower: null, upper: null },
  { period: 'W6', actual: 12.9, forecast: 12.9, lower: 12.9, upper: 12.9 },
  { period: 'W7 (F)', actual: null, forecast: 13.4, lower: 12.6, upper: 14.1 },
  { period: 'W8 (F)', actual: null, forecast: 13.8, lower: 12.8, upper: 14.7 },
  { period: 'W9 (F)', actual: null, forecast: 14.1, lower: 13.0, upper: 15.2 },
  { period: 'W10 (F)', actual: null, forecast: 14.5, lower: 13.2, upper: 15.8 },
];

export const RevenueForecastChart: React.FC<RevenueForecastChartProps> = ({
  height = 320,
}) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={forecastData} margin={{ top: 15, right: 15, left: -10, bottom: 0 }}>
          <defs>
            <linearGradient id="actGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FF6A00" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#FF6A00" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="foreGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FFB15A" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#FFB15A" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="period" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} tickFormatter={(v) => `$${v}M`} />
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
          {/* Vertical boundary separating historical from forecast */}
          <ReferenceLine x="W6" stroke="#FF6A00" strokeDasharray="3 3" label={{ value: 'FORECAST HORIZON', fill: '#FF8A24', fontSize: 10, position: 'top' }} />

          <Area type="monotone" dataKey="upper" stroke="none" fill="rgba(255, 106, 0, 0.12)" name="95% Confidence Upper" connectNulls />
          <Area type="monotone" dataKey="lower" stroke="none" fill="rgba(255, 106, 0, 0.05)" name="95% Confidence Lower" connectNulls />
          <Area type="monotone" dataKey="actual" stroke="#FF6A00" strokeWidth={2.5} fill="url(#actGrad)" name="Historical Revenue" connectNulls />
          <Area type="monotone" dataKey="forecast" stroke="#FFB15A" strokeWidth={2.5} strokeDasharray="4 4" fill="url(#foreGrad)" name="AI Revenue Forecast" connectNulls />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RevenueForecastChart;
