import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.VITE_SUPABASE_URL || 'https://zwfecsnodhxbzbagdxng.supabase.co';
const SUPABASE_KEY =
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  process.env.VITE_SUPABASE_ANON_KEY ||
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3ZmVjc25vZGh4YnpiYWdkeG5nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgwMzgxODAsImV4cCI6MjEwMzYxNDE4MH0.DxMNm0pD-Mm-nyNFLjVsoBHuo-aLxhU9eA7JhyCYU5s';

const supabaseAdmin = createClient(SUPABASE_URL, SUPABASE_KEY);

const HEADERS = {
  'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'pt-BR,pt;q=0.9',
};

// Regras estritas de validação e auto-substituição (Self-Healing) por peça
export const CATALOG_RULES = {
  'cpu-ryzen-7800x3d': {
    mustMatch: ['7800x3d'],
    mustNotMatch: ['5800x3d', '9800x3d', 'kit upgrade', 'pc gamer', 'computador'],
    minPrice: 1200,
    maxPrice: 3200,
    kabumQuery: 'processador-amd-ryzen-7-7800x3d',
  },
  'gpu-rtx-5070': {
    mustMatch: ['5070', 'gigabyte'],
    mustNotMatch: ['5070 ti', '5070ti', 'notebook', 'pc gamer', 'computador', 'open box', 'cadeira', 'gabinete'],
    minPrice: 4200,
    maxPrice: 7500,
    kabumQuery: 'rtx-5070-gigabyte',
  },
  'placa-mae-b650em': {
    mustMatch: ['asus', 'tuf', 'b650'],
    mustNotMatch: ['kit upgrade', 'pc gamer', 'computador', 'b550', 'open box'],
    minPrice: 900,
    maxPrice: 2400,
    kabumQuery: 'placa-mae-asus-tuf-b650',
  },
  'ram-corsair-vengeance-32gb': {
    mustMatch: ['corsair', 'vengeance', 'rgb', '32gb', '6000'],
    mustNotMatch: ['1x16gb', '16gb (1x16gb)', 'ddr4', 'notebook'],
    minPrice: 1000,
    maxPrice: 5800,
    kabumQuery: 'cmh32gx5m2d6000z38',
  },
  'ram-corsair-vengeance-32gb-sem-rgb': {
    mustMatch: ['corsair', 'vengeance', '32gb', '6000'],
    mustNotMatch: ['rgb', '1x16gb', '16gb (1x16gb)', 'ddr4', 'notebook'],
    minPrice: 1000,
    maxPrice: 5800,
    kabumQuery: 'cmk32gx5m2d6000z38',
  },
  'ram-corsair-vengeance-rgb-16gb': {
    mustMatch: ['corsair', 'vengeance', 'rgb', '16gb', '6000'],
    mustNotMatch: ['32gb', '2x16gb', 'ddr4', 'notebook'],
    minPrice: 600,
    maxPrice: 3400,
    kabumQuery: 'cmh16gx5m1d6000z38',
  },
  'ssd-lexar-nm790-1tb': {
    mustMatch: ['nvme'],
    mustNotMatch: ['250gb', '256gb', '480gb', '500gb', '512gb', 'sata', 'externo', 'cartao'],
    minPrice: 450,
    maxPrice: 1900,
    kabumQuery: 'ssd-kingston-nv3-1tb',
  },
  'fonte-msi-mag-850w': {
    mustMatch: ['msi', '850w'],
    mustNotMatch: ['550w', '600w', '650w', '750w'],
    minPrice: 400,
    maxPrice: 1200,
    kabumQuery: 'fonte-msi-mag-a850gl-850w',
  },
  'cooler-corsair-nautilus-360': {
    mustMatch: ['corsair', 'nautilus', '360'],
    mustNotMatch: ['240mm', '120mm'],
    minPrice: 300,
    maxPrice: 1100,
    kabumQuery: 'water-cooler-corsair-nautilus-360',
  },
  'monitor-asus-tuf-27': {
    mustMatch: ['asus', 'tuf', '27'],
    mustNotMatch: ['24 pol', '23.8', 'suporte'],
    minPrice: 900,
    maxPrice: 2200,
    kabumQuery: 'vg27aqme5f',
  },
};

function matchesRule(title, rule) {
  if (!title || !rule) return false;
  const lower = title.toLowerCase();
  for (const kw of rule.mustMatch) {
    if (!lower.includes(kw.toLowerCase())) return false;
  }
  for (const bad of rule.mustNotMatch) {
    if (lower.includes(bad.toLowerCase())) return false;
  }
  return true;
}

function isRedirectedOrBrokenUrl(finalUrl) {
  if (!finalUrl) return true;
  const u = finalUrl.toLowerCase();
  if (
    u.includes('/open-box') ||
    u.includes('/kit-upgrade') ||
    u.includes('/busca') ||
    u.endsWith('kabum.com.br/') ||
    u.endsWith('pichau.com.br/') ||
    u.endsWith('terabyteshop.com.br/')
  ) {
    return true;
  }
  return false;
}

async function healKabumOffer(pecaId, rule) {
  try {
    const searchUrl = `https://www.kabum.com.br/busca/${encodeURIComponent(rule.kabumQuery)}`;
    const r = await fetch(searchUrl, { headers: HEADERS, redirect: 'follow' });
    const html = await r.text();
    const m = html.match(/<script id="__NEXT_DATA__"[^>]*>(.*?)<\/script>/);
    if (!m) return null;

    const raw = JSON.parse(m[1]).props?.pageProps?.data;
    const d2 = typeof raw === 'string' ? JSON.parse(raw) : raw;
    const items = d2?.catalogServer?.data || [];

    const valid = items
      .filter((it) => {
        const pix = Number(it.priceWithDiscount || it.price || 0);
        return (
          it.available === true &&
          matchesRule(it.name || '', rule) &&
          pix >= rule.minPrice &&
          pix <= rule.maxPrice
        );
      })
      .sort((a, b) => Number(a.priceWithDiscount) - Number(b.priceWithDiscount));

    if (valid.length === 0) return null;
    const best = valid[0];
    const slug = best.friendlyName || String(best.code);
    return {
      url_produto: `https://www.kabum.com.br/produto/${best.code}/${slug}`,
      preco_pix: Number(best.priceWithDiscount || best.price),
      preco_parcelado: Number(best.price || best.priceWithDiscount),
      disponivel: true,
      healedTitle: best.name,
    };
  } catch {
    return null;
  }
}

async function verifyOffer(oferta, rule) {
  const url = oferta.url_produto || '';

  // 1. Rejeita imediatamente links que apontem para /open-box, /kit-upgrade, /busca ou Home
  if (isRedirectedOrBrokenUrl(url)) {
    return { valid: false, reason: 'broken_url_pattern' };
  }

  // 2. Verificação + Auto-Healing em tempo real para KaBuM!
  if (url.includes('kabum.com.br')) {
    try {
      const resp = await fetch(url, { headers: HEADERS, redirect: 'follow' });
      const finalUrl = resp.url;
      if (isRedirectedOrBrokenUrl(finalUrl) || !finalUrl.includes('/produto/')) {
        const healed = await healKabumOffer(oferta.peca_id, rule);
        return healed ? { valid: true, healed: true, ...healed } : { valid: false, reason: 'redirected_to_non_product' };
      }

      const html = await resp.text();
      const m = html.match(/<script id="__NEXT_DATA__"[^>]*>(.*?)<\/script>/);
      if (!m) {
        return { valid: true, keepExisting: true };
      }

      const prod = JSON.parse(m[1]).props?.pageProps?.product;
      if (!prod) {
        const healed = await healKabumOffer(oferta.peca_id, rule);
        return healed ? { valid: true, healed: true, ...healed } : { valid: false, reason: 'missing_product_data' };
      }

      const title = prod.title || '';
      const avail = Boolean(prod.available);
      const pix = Number(prod.prices?.priceWithDiscount || prod.prices?.price || 0);
      const parc = Number(prod.prices?.price || pix);

      const titleOk = matchesRule(title, rule);
      const priceOk = pix >= rule.minPrice && pix <= rule.maxPrice;

      if (!avail || !titleOk || !priceOk) {
        // Produto esgotou, mudou para outro item ou caiu em vendedor scalper acima do teto -> Auto-Healing!
        const healed = await healKabumOffer(oferta.peca_id, rule);
        if (healed) {
          return { valid: true, healed: true, ...healed };
        }
        return {
          valid: false,
          reason: !avail ? 'out_of_stock' : !priceOk ? 'price_above_sanity_ceiling' : 'title_mismatch',
        };
      }

      return {
        valid: true,
        healed: false,
        url_produto: finalUrl,
        preco_pix: pix,
        preco_parcelado: parc,
        disponivel: true,
      };
    } catch {
      return { valid: true, keepExisting: true };
    }
  }

  // 3. Para Pichau e Terabyte: valida sanidade de preço e URL; tenta checar status HTTP/redirect
  const currentPix = Number(oferta.preco_pix || 0);
  if (rule && (currentPix < rule.minPrice || currentPix > rule.maxPrice)) {
    return { valid: false, reason: 'price_outside_sanity_range' };
  }

  try {
    const resp = await fetch(url, { headers: HEADERS, redirect: 'manual' });
    // Se a loja retornar redirect HTTP 301/302 (como a Terabyte faz quando esgota mandando para /open-box ou /kit-upgrade)
    if (resp.status >= 300 && resp.status < 400) {
      const loc = resp.headers.get('location') || '';
      if (isRedirectedOrBrokenUrl(loc) || !loc.includes(url.split('/').pop().slice(0, 12))) {
        return { valid: false, reason: `redirected_to_${loc}` };
      }
    }
    if (resp.status === 404 || resp.status === 410) {
      return { valid: false, reason: `http_${resp.status}` };
    }
  } catch {
    // Se houver bloqueio de rede, preserva desde que esteja dentro do teto de sanidade
  }

  return { valid: true, keepExisting: true };
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const { data: ofertas, error } = await supabaseAdmin
      .from('pc_ofertas')
      .select('id, peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto');

    if (error) throw error;

    const stats = { checked: 0, updated: 0, healed: 0, disabled: 0 };
    const nowIso = new Date().toISOString();

    await Promise.all(
      (ofertas || []).map(async (of) => {
        stats.checked += 1;
        const rule = CATALOG_RULES[of.peca_id];
        if (!rule) return;

        const result = await verifyOffer(of, rule);

        if (!result.valid) {
          stats.disabled += 1;
          await supabaseAdmin
            .from('pc_ofertas')
            .update({ disponivel: false, ultima_checagem: nowIso })
            .eq('id', of.id);
          return;
        }

        if (result.keepExisting) {
          await supabaseAdmin
            .from('pc_ofertas')
            .update({ ultima_checagem: nowIso })
            .eq('id', of.id);
          return;
        }

        if (result.healed) stats.healed += 1;
        stats.updated += 1;

        const priceChanged = Math.abs(Number(of.preco_pix) - Number(result.preco_pix)) >= 0.5;

        await supabaseAdmin
          .from('pc_ofertas')
          .update({
            loja: result.healed && of.loja.toLowerCase().includes('kabum') ? 'KaBuM! (Em Estoque)' : of.loja,
            url_produto: result.url_produto,
            preco_pix: result.preco_pix,
            preco_parcelado: result.preco_parcelado,
            disponivel: true,
            ultima_checagem: nowIso,
          })
          .eq('id', of.id);

        if (priceChanged) {
          await supabaseAdmin.from('pc_historico_precos').insert({
            peca_id: of.peca_id,
            loja: of.loja,
            preco_pix: result.preco_pix,
            data_hora: nowIso,
          });
        }
      })
    );

    // Se alguma peça não tiver oferta ativa na KaBuM, tenta descobrir/criar via Auto-Healing
    const { data: allPecas } = await supabaseAdmin.from('pc_pecas').select('id');
    const { data: activeOfertas } = await supabaseAdmin
      .from('pc_ofertas')
      .select('peca_id, loja, preco_pix, disponivel');

    for (const p of allPecas || []) {
      const rule = CATALOG_RULES[p.id];
      if (!rule) continue;
      const hasActiveKabum = (activeOfertas || []).some(
        (o) => o.peca_id === p.id && o.disponivel && o.loja.toLowerCase().includes('kabum')
      );
      if (!hasActiveKabum) {
        const healed = await healKabumOffer(p.id, rule);
        if (healed) {
          stats.healed += 1;
          await supabaseAdmin.from('pc_ofertas').upsert(
            {
              peca_id: p.id,
              loja: 'KaBuM! (Em Estoque)',
              preco_pix: healed.preco_pix,
              preco_parcelado: healed.preco_parcelado,
              disponivel: true,
              url_produto: healed.url_produto,
              ultima_checagem: nowIso,
            },
            { onConflict: 'peca_id,loja' }
          );
        }
      }
    }

    // Atualiza preco_referencia de cada peça com o menor preço disponível
    const { data: refreshedOfertas } = await supabaseAdmin
      .from('pc_ofertas')
      .select('peca_id, preco_pix, disponivel')
      .eq('disponivel', true);

    for (const p of allPecas || []) {
      const validPrices = (refreshedOfertas || [])
        .filter((o) => o.peca_id === p.id && o.disponivel)
        .map((o) => Number(o.preco_pix));
      if (validPrices.length > 0) {
        const minPix = Math.min(...validPrices);
        await supabaseAdmin.from('pc_pecas').update({ preco_referencia: minPix }).eq('id', p.id);
      }
    }

    return res.status(200).json({
      ok: true,
      checkedAt: nowIso,
      stats,
    });
  } catch (err) {
    return res.status(500).json({
      ok: false,
      error: err?.message || 'Erro ao verificar ofertas ao vivo',
    });
  }
}
