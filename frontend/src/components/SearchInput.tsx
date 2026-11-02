import React from 'react';
import { Search } from 'lucide-react';

interface SearchInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onSearch?: (value: string) => void;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  onSearch,
  className = '',
  placeholder = 'Search entities, risks, metrics, datasets...',
  ...props
}) => {
  return (
    <div className={`relative flex items-center ${className}`}>
      <Search className="absolute left-3.5 w-4 h-4 text-[#A89D92] pointer-events-none" />
      <input
        type="text"
        placeholder={placeholder}
        onChange={(e) => onSearch?.(e.target.value)}
        className="w-full pl-10 pr-4 py-2 text-xs bg-[#0D0906] border border-[#FF6A00]/20 rounded-xl text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00] focus:ring-1 focus:ring-[#FF6A00]/30 transition-all font-mono"
        {...props}
      />
    </div>
  );
};

export default SearchInput;
