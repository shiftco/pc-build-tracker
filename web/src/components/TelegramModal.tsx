import React, { useState } from 'react';
import { X, Bell, Send, Check, ShieldCheck } from 'lucide-react';

interface TelegramModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TelegramModal: React.FC<TelegramModalProps> = ({ isOpen, onClose }) => {
  const [simulated, setSimulated] = useState(false);

  if (!isOpen) return null;

  const handleSimulate = () => {
    setSimulated(true);
    setTimeout(() => setSimulated(false), 4000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-md rounded-2xl bg-zinc-950 border border-zinc-800 p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <Bell className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white tracking-tight">
              Alertas de Preço no Telegram
            </h3>
            <p className="text-xs text-zinc-400 font-mono">
              Notificações push em tempo real
            </p>
          </div>
        </div>

        <div className="space-y-3 my-5 text-xs text-zinc-300">
          <div className="p-3 rounded-lg bg-zinc-900/60 border border-zinc-800/80 space-y-2">
            <div className="flex items-center gap-2 text-white font-medium">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Como funciona a caça de ofertas:</span>
            </div>
            <p className="text-zinc-400 leading-relaxed font-mono text-[11px]">
              O robô monitora 4 vezes ao dia (08h, 12h, 18h e 22h) a Kabum, Pichau, Terabyte, Mercado Livre e Shopee.
            </p>
            <p className="text-zinc-400 leading-relaxed font-mono text-[11px]">
              Assim que o preço de qualquer peça cair ou bater a meta de compra, um card chega no Telegram do seu primo com o link direto para comprar antes de esgotar o estoque.
            </p>
          </div>
        </div>

        {simulated ? (
          <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono flex items-center justify-center gap-2">
            <Check className="w-4 h-4" />
            <span>Alerta de teste enviado com sucesso!</span>
          </div>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={handleSimulate}
              className="flex-1 py-2.5 px-4 rounded-lg bg-white hover:bg-zinc-200 text-black text-xs font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Testar Envio de Alerta</span>
            </button>
            <button
              onClick={onClose}
              className="py-2.5 px-4 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 text-xs font-medium transition-colors"
            >
              Fechar
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
