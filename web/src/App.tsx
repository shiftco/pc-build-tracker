import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { HeroStats } from './components/HeroStats';
import { CategoryFilter } from './components/CategoryFilter';
import { PecaCard } from './components/PecaCard';
import { TelegramModal } from './components/TelegramModal';
import { supabase, INITIAL_PECAS } from './lib/supabase';
import type { PecaBuild } from './lib/supabase';
import { Search, Sparkles, AlertTriangle } from 'lucide-react';

export function App() {
  const [pecas, setPecas] = useState<PecaBuild[]>(INITIAL_PECAS);
  const [activeCategory, setActiveCategory] = useState<string>('Todos');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [isTelegramModalOpen, setIsTelegramModalOpen] = useState<boolean>(false);
  const [sortBy, setSortBy] = useState<'ordem' | 'preco-asc' | 'preco-desc'>('ordem');

  // Categorias únicas
  const categories = Array.from(new Set(INITIAL_PECAS.map((p) => p.categoria)));

  // Contagem por categoria
  const categoryCounts = categories.reduce((acc, cat) => {
    acc[cat] = INITIAL_PECAS.filter((p) => p.categoria === cat).length;
    return acc;
  }, {} as Record<string, number>);

  // Tenta carregar do Supabase se online
  const fetchLivePrices = async () => {
    setIsRefreshing(true);
    try {
      const { data: dbPecas, error } = await supabase
        .from('pc_pecas')
        .select(`
          id,
          nome,
          categoria,
          especificacoes,
          imagem_url,
          preco_referencia,
          preco_alvo,
          ordem,
          pc_ofertas (
            loja,
            preco_pix,
            preco_parcelado,
            disponivel,
            url_produto
          )
        `)
        .order('ordem', { ascending: true });

      if (!error && dbPecas && dbPecas.length > 0) {
        const mapped: PecaBuild[] = dbPecas.map((p: any) => {
          const ofertas = (p.pc_ofertas || []).map((o: any) => ({
            loja: o.loja,
            preco_pix: Number(o.preco_pix),
            preco_parcelado: Number(o.preco_parcelado),
            url_produto: o.url_produto,
            disponivel: o.disponivel
          }));

          const ordenadas = [...ofertas].sort((a, b) => a.preco_pix - b.preco_pix);
          const menor = ordenadas[0] || {
            loja: 'KaBuM!',
            preco_pix: Number(p.preco_referencia),
            url_produto: '',
            disponivel: true
          };

          const fallbackPeca = INITIAL_PECAS.find(ip => ip.id === p.id);

          return {
            id: p.id,
            nome: p.nome,
            categoria: p.categoria,
            especificacoes: p.especificacoes,
            imagem_url: p.imagem_url || fallbackPeca?.imagem_url || '/images/cpu.jpg',
            preco_referencia: Number(p.preco_referencia),
            preco_alvo: Number(p.preco_alvo),
            ordem: p.ordem,
            melhor_oferta: { ...menor, is_melhor_preco: true },
            ofertas: ofertas.map((o: any) => ({ ...o, is_melhor_preco: o.loja === menor.loja })),
            historico: fallbackPeca?.historico || []
          };
        });

        setPecas(mapped);
      }
    } catch (err) {
      console.log('Utilizando cache local de ofertas compiladas:', err);
    } finally {
      setTimeout(() => setIsRefreshing(false), 500);
    }
  };

  useEffect(() => {
    fetchLivePrices();
  }, []);

  // Filtragem e busca
  const filteredPecas = pecas
    .filter((p) => {
      const matchesCategory = activeCategory === 'Todos' || p.categoria === activeCategory;
      const matchesSearch =
        p.nome.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.especificacoes.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.categoria.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
    .sort((a, b) => {
      if (sortBy === 'preco-asc') {
        return (a.melhor_oferta?.preco_pix || 0) - (b.melhor_oferta?.preco_pix || 0);
      }
      if (sortBy === 'preco-desc') {
        return (b.melhor_oferta?.preco_pix || 0) - (a.melhor_oferta?.preco_pix || 0);
      }
      return a.ordem - b.ordem;
    });

  return (
    <div className="min-h-screen bg-black text-zinc-100 flex flex-col selection:bg-zinc-800 selection:text-white">
      {/* Top Header */}
      <Header
        onRefresh={fetchLivePrices}
        isRefreshing={isRefreshing}
        onOpenTelegramModal={() => setIsTelegramModalOpen(true)}
      />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {/* Banner de Destaque / Build do Primo */}
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 p-5 rounded-2xl bg-zinc-950 border border-zinc-800/80 shadow-lg">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Sparkles className="w-3 h-3" /> Configuração High-End Selecionada
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Build Gamer: Ryzen 7 7800X3D + RTX 5070 12GB
            </h1>
            <p className="text-xs sm:text-sm text-zinc-400 mt-1 font-mono">
              Monitorando KaBuM!, Terabyte, Pichau, Shopee e Mercado Livre
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsTelegramModalOpen(true)}
              className="w-full sm:w-auto px-4 py-2 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-mono text-zinc-200 transition-colors cursor-pointer"
            >
              Configurar Alertas no Telegram
            </button>
          </div>
        </div>

        {/* Hero KPI Cards */}
        <HeroStats pecas={pecas} />

        {/* Controles de Busca e Filtro */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              placeholder="Buscar peça por nome, modelo ou especificação..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-lg bg-zinc-950 border border-zinc-800/80 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-500 font-mono transition-colors"
            />
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-zinc-500 hidden sm:inline">Ordenar:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-800/80 text-xs text-zinc-300 font-mono focus:outline-none focus:border-zinc-500 cursor-pointer"
            >
              <option value="ordem">Ordem da Build</option>
              <option value="preco-asc">Menor Preço</option>
              <option value="preco-desc">Maior Preço</option>
            </select>
          </div>
        </div>

        {/* Filtros de Categoria */}
        <CategoryFilter
          categories={categories}
          activeCategory={activeCategory}
          onSelectCategory={setActiveCategory}
          counts={categoryCounts}
        />

        {/* Grid de Componentes */}
        {filteredPecas.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-5">
            {filteredPecas.map((peca) => (
              <PecaCard key={peca.id} peca={peca} />
            ))}
          </div>
        ) : (
          <div className="p-12 text-center rounded-2xl bg-zinc-950 border border-zinc-800/80 my-8">
            <AlertTriangle className="w-8 h-8 text-zinc-600 mx-auto mb-3" />
            <p className="text-sm text-zinc-400 font-mono">Nenhum componente encontrado para essa busca.</p>
          </div>
        )}
      </main>

      {/* Footer Minimalista Vercel */}
      <footer className="border-t border-zinc-900 bg-black py-8 mt-16 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-zinc-500">
          <p>RIG.TRACKER // Desenvolvido sob medida para caça de ofertas de hardware no Brasil.</p>
          <div className="flex items-center gap-4">
            <span className="text-zinc-600">Kabum</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-600">Pichau</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-600">Terabyte</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-600">Mercado Livre</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-600">Shopee</span>
          </div>
        </div>
      </footer>

      {/* Modal Telegram */}
      <TelegramModal
        isOpen={isTelegramModalOpen}
        onClose={() => setIsTelegramModalOpen(false)}
      />
    </div>
  );
}

export default App;
