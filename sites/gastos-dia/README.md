# Dia a dia · Gastos

Controle privado de compras recebidas por SMS. Primeira versão para validar a
captura pelo Atalhos do iPhone antes de acrescentar foto de nota ou integração bancária.

## Produto

- `/`: totais de hoje, da semana (segunda-feira até hoje) e do mês; filtro de alimentação.
- Lançamentos: SMS original, conferência de valor/data/categoria, regra por loja e exclusão reversível.
- Conectar iPhone: conexão revogável por aparelho e tutorial de configuração.
- `/`: Visão geral para proprietário e convidados com permissão, limitada aos cartões autorizados. `/resumo` redireciona para `/` para preservar links antigos.
- Testes ficam separados dos totais reais. Não há dados de exemplo na base publicada.

Valores são armazenados em centavos. Datas usam America/Sao_Paulo. Compras parceladas
usam o valor integral informado, ficam sinalizadas e precisam de conferência. O resumo
representa compras registradas, não saldo bancário ou fluxo de caixa conciliado.
Pagamento de fatura e compras recusadas são ignorados. Estornos e valores ambíguos
ficam pendentes, sem alterar automaticamente compras anteriores.

## Recebimento

`POST /api/sms`, corpo JSON com `message` (texto, até 4.000 caracteres).
Opcionalmente: `isTest` (booleano), `eventId` (identificador estável para reenvio)
e `receivedAt` (data ISO original). Nunca gere um novo eventId para cada tentativa
de reenvio da mesma mensagem.

O Atalhos usa dois cabeçalhos provisionados na área privada:
`OAI-Sites-Authorization` e `X-Device-Key`. As chaves não ficam no código-fonte.
A chave por aparelho só permite captura; as APIs de leitura exigem identidade assinada.
Respostas relevantes: received, needs_review, duplicate, ignored. HTTP 4xx/5xx
nunca significa que a compra foi registrada com sucesso.

Há deduplicação de mensagens idênticas por conexão: permanente quando existe data
e hora no SMS ou eventId; nos outros casos, janela de dez minutos. Não há fila de
reenvio offline ou recuperação automática do histórico. Reimportar manualmente uma
compra já capturada por um aparelho pode gerar duplicidade: confira antes de importar.

## Acesso e operação

O Site é inicialmente privado ao proprietário. A primeira sessão assinada inicializa
o proprietário na base; abra a página com essa conta antes de convidar outra pessoa.
Depois, só o proprietário corrige lançamentos e cria conexões. Convidados consultam as páginas e os cartões autorizados em Acessos.
Antes de ampliar o acesso, convide explicitamente apenas quem pode ver o resumo;
não torne o Site público. A permissão de Paloma ainda precisa ser configurada.

O segredo de hospedagem `SITE_SERVICE_TOKEN` contém o token de serviço existente do
próprio Site. Configure-o pelas ferramentas Sites. O formulário privado exibe as
credenciais somente durante a criação explícita da conexão, sem cache ou armazenamento
no navegador. Não copie chaves para o README, screenshots, logs, Git ou conversas.

## Verificação local

Com Node >=22.13 e dependências instaladas:

```text
node --test tests/domain.test.ts
node node_modules/typescript/bin/tsc --noEmit
node scripts/run-framework.mjs dev
node tests/api-smoke.mjs
```

O teste de API só aceita localhost/127.0.0.1. Precisa da migração local aplicada e de
uma `.dev.vars` ignorada contendo `SITE_SERVICE_TOKEN` com valor fictício. O teste cria
dados locais descartáveis, confere captura, autorização, totais, duplicidade, edição,
exclusão/restauração e revogação. A base local nunca integra o pacote publicado.
Detalhes do starter, migração e publicação estão abaixo. Use o fluxo da skill Sites
para publicar; este diretório deve ter seu próprio repositório, separado do projeto financeiro.

## Base técnica (Vinext / Sites)

A clean full-stack starter running on [vinext](https://github.com/cloudflare/vinext), with optional Cloudflare D1 and Drizzle support.

## Prerequisites

- Node.js `>=22.13.0`
- Portable: Windows, macOS, or Linux; no Bash required
- Managed Linux: managed Linux runtime with Bash, `flock`, `curl`, `sha256sum`, and GNU `timeout`
- Git is required only for publishing

## Sites Lifecycle

The Sites initializer copies the shared starter and selects managed-linux only when `SITES_MANAGED_LINUX_CONTAINER=1`; otherwise it selects portable. It saves the selection only in ignored `.sites-runtime/execution-profile.json`. Both profiles copy/configure first, then use the plugin's separate `install-dependencies.mjs` step to measure installation independently. Edit source under `app/` and follow the Sites skill for installation, preview, builds, and publishing.

Run `node <plugin-root>/scripts/configure-execution-profile.mjs` only when the profile is unknown for the current checkout and environment. Profile changes do not alter tracked source or require reinstalling otherwise-valid dependencies; restart an existing preview to use the new selection. Do not commit or upload `.sites-runtime/`.

This starter does not use `wrangler.jsonc`.

`install:ci` runs `npm ci` once against the shared lockfile, disables parent-workspace discovery, and includes required dev/optional dependencies despite production/omit settings. Sharp defaults to prebuilt binaries unless explicitly configured otherwise. Do not overlap installers.

- **Portable:** Preserve host HOME, npm cache, registry, proxy, temporary paths, retry/concurrency settings, and lifecycle-script policy. Use `--prefer-offline --no-audit --no-fund`.
- **Managed Linux:** Use the existing project-local HOME/cache/tmp setup and Linux install lock, tarball preflight, and timeout. Restore the image-seeded npm cache only when its lockfile hash matches; retain network fallback. Builds keep their existing timeout. These helpers are not invoked by the portable profile.

`scripts/sites-env.mjs` preserves the caller's HOME, npm cache, proxy, XDG, and temporary-directory configuration while defaulting Wrangler and Miniflare state to the checkout. If npm reports an unwritable cache, select a writable path with `npm_config_cache` for that install. The `dev` and `start` scripts also keep Wrangler logs inside the checkout. Generated `.sites-runtime/` and `.wrangler/` directories are disposable and ignored by Git.

On portable, `npm run dev` uses `vinext dev` with HMR, starting at port 5173. Vinext records the running server in ignored `.vinext/` state, rejects an ordinary duplicate launch, and recovers stale state after a stopped process; exactly simultaneous starts can race. Pass `--port <port>` or `--hostname <host>` after `npm run dev --` when needed; keep portable previews on loopback.

For browser QA on managed Linux, use `sites-preview start`. The project's dev script runs Vite and accepts the supervisor's `--host 0.0.0.0 --port 4173 --strictPort` arguments. The internal browser uses `http://terminal.local:4173/`; it is not a user-facing URL. The supervisor owns the preview lifecycle. The ignored local profile survives the supervisor's cleared process environment.

The portable profile simulates ChatGPT sign-in only for loopback development requests. Visit `/signin-with-chatgpt?return_to=/` to sign in as `local_seedy` (`seedy@sites.test`, display name `Seedy`) and `/signout-with-chatgpt?return_to=/` to sign out. The development cookie preserves that identity across server restarts. Mock auth is disabled in the managed-linux profile and is not included in production builds; hosted authentication remains dispatch-owned.

The Worker uses `vinext/server/fetch-handler`, including Vinext's config-aware image handling. After building, `npm start` runs that Worker locally through Wrangler on `127.0.0.1`, sharing `.wrangler/state` with dev preview and local D1 migrations; it does not deploy the site or simulate sign-in. Use the URL printed by the server. Pass `npm start -- --port <port>` to select a different built-preview port.

Local previews use Miniflare's placeholder `Request.cf` metadata without a network lookup. Set `CLOUDFLARE_CF_FETCH_ENABLED=true` to opt into fetching preview metadata; this setting does not change hosted request metadata.

Local tool usage metrics are disabled by default. Set `WRANGLER_SEND_METRICS=true` to opt in.

## Included Shape

- edit site code under `app/`
- `app/chatgpt-auth.ts` provides optional dispatch-owned ChatGPT sign-in helpers
- `.openai/hosting.json` declares optional Sites D1 and R2 bindings
- `vite.config.ts` simulates declared bindings for local development
- `db/index.ts` reads the D1 binding from the Cloudflare Worker environment
- `db/schema.ts` starts intentionally empty
- `@cloudflare/workers-types` provides Worker types; `cloudflare-env.d.ts` declares optional `DB`/`BUCKET` bindings—update these declarations if binding names change
- `examples/d1/` contains an optional D1 example surface
- `drizzle.config.ts` supports local migration generation when needed

## Workspace Auth Headers

Signed-in visitors receive both `oai-authenticated-user-id` and `oai-authenticated-user-email`. Private Sites require every visitor to sign in; public Sites may also have anonymous visitors, for whom neither header is present.

The user ID is stable for the same user on the same Site and different across Sites. Use it as the durable user key; use email and name for display or contact purposes.

SIWC-authenticated workspace sites may also receive `oai-authenticated-user-full-name` when the user's SIWC profile has a non-empty `name` claim. The full-name value is percent-encoded UTF-8 and is accompanied by `oai-authenticated-user-full-name-encoding: percent-encoded-utf-8`.

Treat the full name as optional and fall back to email when it is absent:

```tsx
import { headers } from "next/headers";

export default async function Home() {
  const requestHeaders = await headers();
  const userId = requestHeaders.get("oai-authenticated-user-id");
  const email = requestHeaders.get("oai-authenticated-user-email");
  const encodedFullName = requestHeaders.get("oai-authenticated-user-full-name");
  const fullName =
    encodedFullName &&
    requestHeaders.get("oai-authenticated-user-full-name-encoding") ===
      "percent-encoded-utf-8"
      ? decodeURIComponent(encodedFullName)
      : null;

  const displayName = fullName ?? email;
  // ...
}
```

## Optional Dispatch-Owned ChatGPT Sign-In

Import the ready-to-use helpers from `app/chatgpt-auth.ts` when the site needs optional or required ChatGPT sign-in:

- Use `getChatGPTUser()` for optional signed-in UI.
- Use the returned `userId` as the stable user key for user-owned records; do not use email as a durable identifier.
- Use `requireChatGPTUser(returnTo)` for server-rendered pages that should send anonymous visitors through Sign in with ChatGPT.
- In a Server Component, start sign-in with `<a href={chatGPTSignInPath(returnTo)} target="_top">`. The auth helper module is server-only; do not import it into a Client Component.
- Do not use `fetch`, XHR, a client-side router, or a framework link that can prefetch the sign-in route. SIWC must start as a top-level navigation.
- Never request the AuthAPI authorization endpoint directly. The dispatch-owned `/signin-with-chatgpt` route must start the SIWC flow.
- Use `chatGPTSignOutPath(returnTo)` for browser sign-out links or actions.
- Pass a same-origin relative `returnTo` path for the destination after sign-in or sign-out. The helper validates and safely encodes it.
- Mark protected pages with `export const dynamic = "force-dynamic"` because they depend on per-request identity headers.

Dispatch owns `/signin-with-chatgpt`, `/signout-with-chatgpt`, `/callback`, the OAuth cookies, and identity header injection. Do not implement app routes for those reserved paths. Routes that do not import and call the helper remain anonymous-compatible.

SIWC establishes identity only; it does not prove workspace membership. Use the Sites hosting platform's access policy controls for workspace-wide restrictions, or enforce explicit server-side membership or allowlist checks.

Use SIWC for account pages, user-specific dashboards, saved records, and write actions tied to the current ChatGPT user. Leave public content anonymous.

## Local D1 migrations

For a D1-backed local preview, generate SQL with `npm run db:generate`. Build once through the Sites skill's build entrypoint (or `npm run build` for standalone use) to generate `dist/server/wrangler.json`, rebuilding if bindings change. From the project root, apply each pending migration in order:

```sh
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_example.sql
```

Replace the filename with the pending migration and `DB` with your D1 binding name if different. Use `.wrangler/state`, not `.wrangler/state/v3`; Wrangler adds the versioned directories. Do not replay migrations already applied locally. This updates only the preview database; publishing applies production migrations separately.

## Diagnostic Commands

- `npm run install:ci`: perform the one locked dependency install
- `npm run dev`: start the Vite/Vinext development server
- `npm run build`: build the deployable Sites artifact
- `npm run start`: preview the built Worker locally with D1/R2 support
- `npm run db:generate`: generate Drizzle migrations after schema changes

When using the Sites plugin, follow its skill instructions for installation, builds, and publishing. These npm commands remain available for standalone use.

The portable build runs Vinext directly without a host `timeout` command. The managed-linux build uses `scripts/build-verified.sh` and its existing `SITES_BUILD_TIMEOUT` setting.

## Learn More

- [vinext Documentation](https://github.com/cloudflare/vinext)
- [Drizzle D1 Guide](https://orm.drizzle.team/docs/get-started/d1-new)

## Períodos com categoria automática

O proprietário configura nome, categoria, início e fim em /periodos. Datas e horários
são locais de America/Sao_Paulo, com precisão de minuto e limites inclusivos.
Períodos ativos não podem se sobrepor, inclusive na gravação concorrente.

A categoria efetiva é calculada sobre a categoria original: editar ou desativar um
período recalcula os totais sem perder a classificação de origem. A regra vale
para todos os cartões, preservando o filtro de acesso dos convidados.

Novos SMS preservam o horário da compra. Ao salvar um período, horários de SMS
antigos são recuperados em lotes restritos às suas datas; horários editados pelo
proprietário não são substituídos. Nunca usamos horário de recebimento como
horário da compra. Sem horário, só dias inteiros contidos no período são
classificados automaticamente; nos limites parciais há sinalização de conferência.

Testes: node --test tests/domain.test.ts e node tests/periods-smoke.mjs (somente
localhost, após a migração 0007). A migração adiciona apenas estrutura. Nenhuma
viagem real é cadastrada automaticamente sem os horários definidos.

A permissão Períodos libera consulta a nomes, datas, horários e totais apenas dos
cartões autorizados. Ela pode ser concedida sem Visão geral ou Lançamentos.
Criar/editar períodos continua exclusivo do proprietário. A migração 0008 mantém
a nova permissão desativada nos acessos existentes até liberação explícita.

## Pix por SMS

A mesma API POST /api/sms aceita o texto completo de Pix em message, sem mudar
as chaves, eventId, receivedAt ou isTest. Saídas explicitamente confirmadas
extraem valor e destinatário e entram no resumo, sempre para conferência da
categoria e natureza do gasto. Transferências próprias e reembolsos podem ser
excluídos. Pix recebidos retornam ignored; mensagens ambíguas, agendamentos,
falhas e devoluções ficam sem valor para conferência, sem somar ao resumo.
A resposta inclui paymentMethod (pix/card). Lançamentos Pix usam source sms_pix
ou manual_sms_pix, sem cartão, e exigem a permissão Pix em Acessos para convidados. A opção de cartões
não identificados não concede acesso aos Pix.

No Atalhos, acrescente uma automação para o remetente do SMS de Pix, contendo
Pix, chamando o mesmo atalho de envio. O filtro Compra aprovada não captura Pix.
O formato foi validado com exemplos sintéticos e com o texto da notificação;
ainda é necessário validar o primeiro SMS real do Itaú.

## Filtros e permissões de Pix

Visão geral e Lançamentos oferecem Forma de pagamento, incluindo Pix separado
dos cartões não identificados. A permissão includePix nasce desativada nos
acessos existentes e pode ser concedida sem cartão. Vale para resumo,
lançamentos e totais de períodos, sempre limitada às páginas autorizadas.

GET /api/entries aceita q (até 100 caracteres) e category. A busca ignora
acentos e maiúsculas; termos alfanuméricos de 3 a 30 caracteres toleram uma
letra diferente (AZE encontra AREZZO). Busca, categoria efetiva e forma de
pagamento são combinadas antes da paginação. card=pix também vale para resumo.
Excluir abre confirmação Sim/Cancelar e mantém a restauração disponível.
A interface não oferece modo de teste, exemplos fictícios ou instruções para
registrá-los. O parâmetro isTest da API permanece para compatibilidade e
verificação técnica isolada; registros antigos de teste continuam fora dos totais.
