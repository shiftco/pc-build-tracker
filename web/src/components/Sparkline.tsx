import React from 'react';
import type { HistoricoPonto } from '../lib/supabase';

interface SparklineProps {
  historico: HistoricoPonto[];
  height?: number;
}

export const Sparkline: React.FC<SparklineProps> = ({ historico, height = 48 }) => {
  if (!historico || historico.length < 2) {
    return <div className="text-xs text-zinc-600 font-mono py-2">Histórico em consolidação</div>;
  }

  const precos = historico.map((h) => h.preco);
  const min = Math.min(...precos);
  const max = Math.max(...precos);
  const range = max - min || 1;
  const width = 240;
  const paddingY = 8;
  const innerHeight = height - paddingY * 2;

  // Calcula coordenadas dos pontos SVG
  const points = precos.map((val, idx) => {
    const x = (idx / (precos.length - 1)) * (width - 16) + 8;
    const y = height - paddingY - ((val - min) / range) * innerHeight;
    return { x, y, val, label: historico[idx].data };
  });

  const pathD = points.reduce((acc, pt, idx) => {
    return idx === 0 ? `M ${pt.x} ${pt.y}` : `${acc} L ${pt.x} ${pt.y}`;
  }, '');

  // Preço caiu recentemente?
  const ultimoPreco = precos[precos.length - 1];
  const primeiroPreco = precos[0];
  const isCaindo = ultimoPreco <= primeiroPreco;
  const strokeColor = isCaindo ? '#10b981' : '#f43f5e'; // emerald ou rose

  return (
    <div className="flex flex-col gap-1 w-full bg-zinc-950/60 p-2.5 rounded-lg border border-zinc-900">
      <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500">
        <span>Oscilação recente:</span>
        <span className={isCaindo ? 'text-emerald-400' : 'text-rose-400'}>
          {isCaindo ? '↓ Em queda' : '↑ Em alta'} (Min: R$ {min.toFixed(0)} / Max: R$ {max.toFixed(0)})
        </span>
      </div>
      <div className="relative w-full overflow-hidden">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-12 overflow-visible">
          {/* Linha guia de fundo */}
          <line
            x1="8"
            y1={height / 2}
            x2={width - 8}
            y2={height / 2}
            stroke="#27272a"
            strokeDasharray="3 3"
            strokeWidth="1"
          />

          {/* Gráfico de Linha */}
          <path
            d={pathD}
            fill="none"
            stroke={strokeColor}
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Pontos nas pontas */}
          {points.map((pt, i) => (
            <circle
              key={i}
              cx={pt.x}
              cy={pt.y}
              r={i === points.length - 1 ? 3.5 : 2}
              fill={i === points.length - 1 ? strokeColor : "#71717a"}
            />
          ))}
        </svg>
      </div>
      <div className="flex justify-between text-[9px] font-mono text-zinc-600 px-1">
        <span>{historico[0].data}</span>
        <span>Hoje ({historico[historico.length - 1].data})</span>
      </div>
    </div>
  );
};
