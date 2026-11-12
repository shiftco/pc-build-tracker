import React from 'react';
import { Bell, RefreshCw, Cpu } from 'lucide-react';

interface HeaderProps {
  onRefresh: () => void;
  isRefreshing: boolean;
  onOpenTelegramModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onRefresh, isRefreshing, onOpenTelegramModal }) => {
  return (
    <header className="border-b border-zinc-800/80 bg-black/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-zinc-900 border border-zinc-700/80 flex items-center justify-center text-white shadow-inner">
            <Cpu className="w-5 h-5 text-zinc-100" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm sm:text-base tracking-tight text-white font-mono">
                RIG.TRACKER
              </span>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-400">
                v1.0 Pro
              </span>
            </div>
            <p className="text-xs text-zinc-400 hidden sm:block">
              Monitor de Peças & Ofertas em Tempo Real
            </p>
          </div>
        </div>

        {/* Live Status + Actions */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Status Live */}
          <div className="hidden sm:inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-zinc-900/90 border border-zinc-800 text-zinc-300">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>5 Lojas Ativas</span>
          </div>

          {/* Telegram Alert Button */}
          <button
            onClick={onOpenTelegramModal}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 hover:bg-zinc-800 border border-zinc-700/80 text-zinc-200 transition-colors cursor-pointer"
          >
            <Bell className="w-3.5 h-3.5 text-blue-400" />
            <span className="hidden sm:inline">Alertas Telegram</span>
          </button>

          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-white hover:bg-zinc-200 text-black transition-colors disabled:opacity-50 cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">{isRefreshing ? 'Atualizando...' : 'Atualizar'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
