import React from 'react';

interface CategoryFilterProps {
  categories: string[];
  activeCategory: string;
  onSelectCategory: (cat: string) => void;
  counts: Record<string, number>;
}

export const CategoryFilter: React.FC<CategoryFilterProps> = ({
  categories,
  activeCategory,
  onSelectCategory,
  counts,
}) => {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-6 scrollbar-none">
      <button
        onClick={() => onSelectCategory('Todos')}
        className={`px-3 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition-all border ${
          activeCategory === 'Todos'
            ? 'bg-white text-black border-white font-medium'
            : 'bg-zinc-950 text-zinc-400 border-zinc-800/80 hover:text-white hover:border-zinc-700'
        }`}
      >
        Todos ({Object.values(counts).reduce((a, b) => a + b, 0)})
      </button>

      {categories.map((cat) => (
        <button
          key={cat}
          onClick={() => onSelectCategory(cat)}
          className={`px-3 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition-all border ${
            activeCategory === cat
              ? 'bg-white text-black border-white font-medium'
              : 'bg-zinc-950 text-zinc-400 border-zinc-800/80 hover:text-white hover:border-zinc-700'
          }`}
        >
          {cat} ({counts[cat] || 0})
        </button>
      ))}
    </div>
  );
};
