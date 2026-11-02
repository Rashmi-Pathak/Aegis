import React from 'react';

interface DataFlowBackgroundProps {
  className?: string;
}

export const DataFlowBackground: React.FC<DataFlowBackgroundProps> = ({ className = '' }) => {
  return (
    <div className={`absolute inset-0 pointer-events-none overflow-hidden select-none ${className}`}>
      <svg className="w-full h-full opacity-30" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="dataFlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#FF6A00" stopOpacity="0" />
            <stop offset="50%" stopColor="#FF8A24" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#FFB15A" stopOpacity="0" />
          </linearGradient>
        </defs>

        {/* Animated circuit lines */}
        <path
          d="M 50 150 L 350 150 L 500 280 L 950 280"
          fill="none"
          stroke="url(#dataFlowGrad)"
          strokeWidth="1.5"
          strokeDasharray="12 180"
          className="animate-[dash_6s_linear_infinite]"
        />
        <path
          d="M 120 400 L 450 400 L 600 200 L 1150 200"
          fill="none"
          stroke="url(#dataFlowGrad)"
          strokeWidth="1.2"
          strokeDasharray="16 220"
          className="animate-[dash_8s_linear_infinite]"
        />
        <path
          d="M 300 650 L 650 650 L 800 480 L 1300 480"
          fill="none"
          stroke="url(#dataFlowGrad)"
          strokeWidth="1"
          strokeDasharray="10 160"
          className="animate-[dash_5s_linear_infinite]"
        />
      </svg>
    </div>
  );
};

export default DataFlowBackground;
