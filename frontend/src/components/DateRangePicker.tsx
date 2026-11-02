import React, { useState } from 'react';
import { Calendar } from 'lucide-react';

interface DateRangePickerProps {
  initialRange?: string;
  onRangeChange?: (range: string) => void;
  className?: string;
}

export const DateRangePicker: React.FC<DateRangePickerProps> = ({
  initialRange = 'Trailing 30 Days',
  onRangeChange,
  className = '',
}) => {
  const [selected, setSelected] = useState(initialRange);
  const options = ['Last 7 Days', 'Trailing 30 Days', 'Quarter to Date (Q1)', 'Full Year 2026', '90-Day Outlook'];

  const handleSelect = (val: string) => {
    setSelected(val);
    onRangeChange?.(val);
  };

  return (
    <div className={`relative inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#0D0906] border border-[#FF6A00]/20 text-xs font-mono text-[#F5F0EA] ${className}`}>
      <Calendar className="w-3.5 h-3.5 text-[#FF6A00]" />
      <select
        value={selected}
        onChange={(e) => handleSelect(e.target.value)}
        className="bg-transparent text-xs text-[#F5F0EA] focus:outline-none cursor-pointer"
      >
        {options.map((opt) => (
          <option key={opt} value={opt} className="bg-[#120C08] text-[#F5F0EA]">
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DateRangePicker;
