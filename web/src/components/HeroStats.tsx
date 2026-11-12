import React from 'react';
import { DollarSign, TrendingDown, CheckCircle2, ShoppingBag } from 'lucide-react';
import type { PecaBuild } from '../lib/supabase';

interface HeroStatsProps {
  pecas: PecaBuild[];
}

export const HeroStats: React.FC<HeroStatsProps> = ({ pecas }) => {
  const totalPix = pecas.reduce((acc, p) => acc + (p.melhor_oferta?.preco_pix || p.preco_referencia), 0);
  const totalParcelado = pecas.reduce((acc, p) => acc + (p.melhor_oferta?.preco_parcelado || (p.melhor_oferta?.preco_pix ? p.melhor_oferta.preco_pix * 1.15 : p.preco_referencia * 1.15)), 0);
  
  // Cálculo de pior preço registrado em lojas vs melhor preço
  const piorTotal = pecas.reduce((acc, p) => {
    const precosValidos = p.ofertas.map(o => o.preco_pix).filter(pr => pr < 4000 || p.categoria === 'Placa de Vídeo'); // ignora anomalias absurdas
    const max = precosValidos.length ? Math.max(...precosValidos) : p.preco_referencia;
    return acc + max;
  }, 0);

  const economiaPotencial = Math.max(0, piorTotal - totalPix);
  const totalAlvo = pecas.reduce((acc, p) => acc + p.preco_alvo, 0);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {/* Total da Build à Vista (PIX) */}
      <div className="p-5 rounded-xl bg-zinc-950/90 border border-zinc-800/80 hover:border-zinc-700/80 transition-all">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">Total à Vista (PIX)</span>
          <div className="w-7 h-7 rounded-md bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <DollarSign className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl sm:text-3xl font-bold font-mono tracking-tight text-white">
            {totalPix.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </span>
        </div>
        <p className="text-xs text-zinc-500 mt-1 font-mono">
          Somatório das menores ofertas atuais
        </p>
      </div>

      {/* Economia Consolidada */}
      <div className="p-5 rounded-xl bg-zinc-950/90 border border-zinc-800/80 hover:border-zinc-700/80 transition-all">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">Economia no Radar</span>
          <div className="w-7 h-7 rounded-md bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <TrendingDown className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl sm:text-3xl font-bold font-mono tracking-tight text-emerald-400">
            -{economiaPotencial.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </span>
        </div>
        <p className="text-xs text-zinc-500 mt-1 font-mono">
          vs comprar tudo na loja mais cara
        </p>
      </div>

      {/* Total a Prazo (Cartão 10x/12x) */}
      <div className="p-5 rounded-xl bg-zinc-950/90 border border-zinc-800/80 hover:border-zinc-700/80 transition-all">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">Total Parcelado</span>
          <div className="w-7 h-7 rounded-md bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <ShoppingBag className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl sm:text-3xl font-bold font-mono tracking-tight text-zinc-200">
            {totalParcelado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </span>
        </div>
        <p className="text-xs text-zinc-500 mt-1 font-mono">
          em até 10x ou 12x no cartão
        </p>
      </div>

      {/* Meta Total da Máquina */}
      <div className="p-5 rounded-xl bg-zinc-950/90 border border-zinc-800/80 hover:border-zinc-700/80 transition-all">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">Status dos Itens</span>
          <div className="w-7 h-7 rounded-md bg-zinc-800/80 border border-zinc-700 flex items-center justify-center text-zinc-300">
            <CheckCircle2 className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl sm:text-3xl font-bold font-mono tracking-tight text-white">
            {pecas.length}/8
          </span>
          <span className="text-xs font-mono text-zinc-400">rastreados</span>
        </div>
        <p className="text-xs text-zinc-500 mt-1 font-mono">
          Meta de compra: {totalAlvo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
        </p>
      </div>
    </div>
  );
};
