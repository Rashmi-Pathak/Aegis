import React from 'react';
import SearchInput from './SearchInput';

interface FilterOption {
  id: string;
  label: string;
}

interface FilterBarProps {
  categories: FilterOption[];
  activeCategory: string;
  onSelectCategory: (id: string) => void;
  onSearch?: (term: string) => void;
  searchPlaceholder?: string;
  className?: string;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  categories,
  activeCategory,
  onSelectCategory,
  onSearch,
  searchPlaceholder,
  className = '',
}) => {
  return (
    <div className={`flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 ${className}`}>
      {/* Category Pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
        {categories.map((cat) => {
          const isActive = activeCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(cat.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition-all duration-200 ${
                isActive
                  ? 'bg-[#FF6A00] text-white font-semibold shadow-[0_0_12px_rgba(255,106,0,0.35)]'
                  : 'bg-[#120C08] text-[#A89D92] hover:text-[#F5F0EA] border border-[#FF6A00]/14 hover:border-[#FF6A00]/30'
              }`}
            >
              {cat.label}
            </button>
          );
        })}
      </div>

      {/* Search Filter */}
      {onSearch && (
        <div className="w-full sm:w-72">
          <SearchInput onSearch={onSearch} placeholder={searchPlaceholder} />
        </div>
      )}
    </div>
  );
};

export default FilterBar;
