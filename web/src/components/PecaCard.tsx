import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, Check } from 'lucide-react';
import type { PecaBuild } from '../lib/supabase';
import { Sparkline } from './Sparkline';

interface PecaCardProps {
  peca: PecaBuild;
}

export const PecaCard: React.FC<PecaCardProps> = ({ peca }) => {
  const [expanded, setExpanded] = useState(true);

  const melhor = peca.melhor_oferta;
  const bateuMeta = melhor && melhor.preco_pix <= peca.preco_alvo;

  return (
    <div className="rounded-xl bg-zinc-950/80 border border-zinc-800/80 hover:border-zinc-700/80 transition-all flex flex-col justify-between overflow-hidden group">
      {/* Top Banner / Tags */}
      <div className="p-5 pb-3">
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-[11px] font-mono uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300">
            {peca.categoria}
          </span>

          {bateuMeta ? (
            <span className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
              <Check className="w-3 h-3" /> Meta Batida
            </span>
          ) : (
            <span className="text-[11px] font-mono text-zinc-500">
              Alvo: {peca.preco_alvo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </span>
          )}
        </div>

        {/* Product Media & Title */}
        <div className="flex gap-4 items-center mb-3">
          <div className="w-24 h-24 sm:w-28 sm:h-28 aspect-square rounded-xl bg-[#18181b] border border-zinc-800/80 p-1.5 flex-shrink-0 flex items-center justify-center overflow-hidden">
            <img
              src={peca.imagem_url}
              alt={peca.nome}
              className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
              onError={(e) => {
                // Fallback image se link externo expirar
                (e.target as HTMLImageElement).src = 'https://placehold.co/150x150/18181b/fff?text=' + peca.categoria;
              }}
            />
          </div>

          <div className="flex-1 min-w-0">
            <h3 className="text-sm sm:text-base font-semibold text-white tracking-tight line-clamp-2 leading-snug">
              {peca.nome}
            </h3>
            <p className="text-xs text-zinc-400 mt-1 line-clamp-2 leading-relaxed">
              {peca.especificacoes}
            </p>
          </div>
        </div>

        {/* Preço em Destaque (Campeão) */}
        <div className="mt-4 pt-3 border-t border-zinc-900 flex items-end justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-zinc-400 font-mono">Melhor valor:</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-300">
                {melhor?.loja || 'Kabum'}
              </span>
            </div>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-2xl font-bold font-mono tracking-tight text-white">
                {melhor?.preco_pix.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
              </span>
              <span className="text-[11px] font-mono text-zinc-500">no PIX</span>
            </div>
            {melhor?.preco_parcelado && (
              <span className="text-[11px] text-zinc-500 font-mono block">
                ou {melhor.preco_parcelado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })} a prazo
              </span>
            )}
          </div>

          {/* Botão de Compra Direta */}
          {melhor && (
            <a
              href={melhor.url_produto}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold bg-white hover:bg-zinc-200 text-black transition-colors shadow-sm cursor-pointer"
            >
              <span>Comprar</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>

      {/* Comparativo de Lojas e Gráfico de Oscilação (Visível por padrão) */}
      <div className="border-t border-zinc-900 bg-zinc-950/40">
        <div className="px-5 pt-3 pb-2 flex items-center justify-between">
          <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider">
            Comparativo ({peca.ofertas.length} lojas) & Histórico
          </span>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-[11px] font-mono text-zinc-500 hover:text-zinc-300 flex items-center gap-1 transition-colors cursor-pointer"
          >
            <span>{expanded ? 'Recolher' : 'Expandir'}</span>
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>

        {expanded && (
          <div className="px-5 pb-5 pt-1 space-y-4">
            {/* Tabela de Ofertas nas 5 Lojas */}
            <div className="space-y-1.5">
              <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider block">
                Preços por Loja:
              </span>
              <div className="divide-y divide-zinc-900 border border-zinc-900 rounded-lg overflow-hidden bg-black/40">
                {peca.ofertas.map((of, idx) => (
                  <div
                    key={idx}
                    className={`p-2.5 flex items-center justify-between text-xs font-mono ${
                      of.is_melhor_preco ? 'bg-emerald-500/5' : ''
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${of.is_melhor_preco ? 'text-emerald-400' : 'text-zinc-300'}`}>
                        {of.loja}
                      </span>
                      {of.is_melhor_preco && (
                        <span className="text-[9px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 uppercase">
                          Mais Barato
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-3">
                      <span className={of.preco_pix > 3000 && peca.categoria !== 'Placa de Vídeo' ? 'text-rose-400 line-through' : 'text-zinc-200'}>
                        {of.preco_pix.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                      </span>
                      <a
                        href={of.url_produto}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-zinc-500 hover:text-white transition-colors"
                        title={`Abrir na ${of.loja}`}
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Gráfico Sparkline de Histórico */}
            <Sparkline historico={peca.historico} />
          </div>
        )}
      </div>
    </div>
  );
};
