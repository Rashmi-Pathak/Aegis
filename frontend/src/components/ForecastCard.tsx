import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import GlowCard from './GlowCard';
import { ForecastItem } from '@/types';

interface ForecastCardProps {
  forecast: ForecastItem;
  className?: string;
}

export const ForecastCard: React.FC<ForecastCardProps> = ({ forecast, className = '' }) => {
  // Combine historical and forecast data for continuous area chart
  const chartData = [
    ...forecast.historical.map((d) => ({
      date: d.date,
      actual: d.value,
      forecast: null,
      lower: null,
      upper: null,
    })),
    // Stitch connection point
    {
      date: forecast.historical[forecast.historical.length - 1].date,
      actual: forecast.historical[forecast.historical.length - 1].value,
      forecast: forecast.historical[forecast.historical.length - 1].value,
      lower: forecast.historical[forecast.historical.length - 1].value,
      upper: forecast.historical[forecast.historical.length - 1].value,
    },
    ...forecast.forecast.map((d) => ({
      date: d.date,
      actual: null,
      forecast: d.value,
      lower: d.lowerBound,
      upper: d.upperBound,
    })),
  ];

  return (
    <GlowCard className={`flex flex-col justify-between ${className}`}>
      <div>
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-semibold text-[#F5F0EA]">{forecast.metric}</h4>
            <p className="text-xs text-[#A89D92] mt-0.5 font-mono">
              Horizon: {forecast.horizonDays} days • {forecast.modelUsed}
            </p>
          </div>
          <div className="text-right">
            <span className="text-[10px] font-mono text-[#6F665F] uppercase block">Confidence</span>
            <span className="text-xs font-mono font-bold text-[#FFB15A]">
              {(forecast.confidenceScore * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-4 flex items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#FF6A00]" />
            <span className="text-[#A89D92]">Actuals</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#FFB15A]" />
            <span className="text-[#A89D92]">Forecast</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-1.5 rounded-sm bg-[#FF6A00]/25 border border-[#FF6A00]/40" />
            <span className="text-[#6F665F]">Confidence Band</span>
          </div>
        </div>
      </div>

      {/* Interactive Micro Chart */}
      <div className="h-44 w-full mt-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="actualsGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#FF6A00" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#FF6A00" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="forecastGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#FFB15A" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#FFB15A" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="date" stroke="#6F665F" fontSize={11} tickLine={false} />
            <YAxis stroke="#6F665F" fontSize={11} tickLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#120C08',
                borderColor: 'rgba(255,106,0,0.3)',
                borderRadius: '8px',
                color: '#F5F0EA',
                fontSize: '12px',
                fontFamily: 'monospace',
              }}
            />
            {/* Confidence Area */}
            <Area
              type="monotone"
              dataKey="upper"
              stroke="none"
              fill="rgba(255, 106, 0, 0.12)"
              connectNulls
            />
            {/* Historical Actuals */}
            <Area
              type="monotone"
              dataKey="actual"
              stroke="#FF6A00"
              strokeWidth={2}
              fill="url(#actualsGrad)"
              connectNulls
            />
            {/* Projected Forecast */}
            <Area
              type="monotone"
              dataKey="forecast"
              stroke="#FFB15A"
              strokeWidth={2}
              strokeDasharray="4 4"
              fill="url(#forecastGrad)"
              connectNulls
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Model accuracy footer */}
      <div className="mt-3 pt-2.5 border-t border-[#FF6A00]/10 flex items-center justify-between text-[11px] font-mono text-[#A89D92]">
        <span>MAE: {forecast.accuracyMetrics.mae}</span>
        <span>RMSE: {forecast.accuracyMetrics.rmse}</span>
        <span className="text-[#FF8A24]">MAPE: {forecast.accuracyMetrics.mape}</span>
      </div>
    </GlowCard>
  );
};

export default ForecastCard;
