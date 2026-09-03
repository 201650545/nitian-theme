import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs'
import { join, normalize, resolve, sep } from 'node:path'

export const name = 'nitian-dsh-theme'

/** 逆天主题静态资产根 (v2.1) */
const PROJECT_ROOT = 'D:\\游戏\\逆天主题'
/** 本机 API 网关配额落盘（真实 Token 用量真源） */
const QUOTA_JSON = 'D:\\项目\\data\\search_gateway\\api_gateway\\quota.json'

/** 白名单子路径 -> 磁盘目标 */
const ALLOWED: Array<[string, string]> = [
  ['/manifest.json', join(PROJECT_ROOT, 'workers', 'asset-manifest.schema.json')],
  ['/realms/', join(PROJECT_ROOT, 'assets', 'realms') + sep],
  ['/ui/', join(PROJECT_ROOT, 'assets', 'ui') + sep],
  ['/collected/', join(PROJECT_ROOT, 'workers', 'collected') + sep],
  ['/officials/', join(PROJECT_ROOT, 'workers', 'officials') + sep],
  ['/animations/', join(PROJECT_ROOT, 'assets', 'animations') + sep],
]

const MIME: Record<string, string> = {
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.js': 'application/javascript',
  '.mjs': 'application/javascript',
  '.glb': 'model/gltf-binary',
  '.mp4': 'video/mp4',
  '.zip': 'application/zip',
  '.json': 'application/json; charset=utf-8',
}

function urlPath(reqUrl: string | undefined): string {
  const raw = (reqUrl || '/').split('?')[0]
  try {
    return decodeURIComponent(raw)
  } catch {
    return raw
  }
}

function json(res: any, code: number, body: unknown) {
  res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' })
  res.end(JSON.stringify(body))
}

let lastReadErr = ''
function readRealTokens(): { total: number; today: number; byDateDays: number; err?: string } {
  let total = 0
  let today = 0
  let days = 0
  try {
    const raw = readFileSync(QUOTA_JSON, 'utf8')
    const data = JSON.parse(raw.replace(/^\uFEFF/, '')) as Record<
      string,
      Record<string, { input_tokens?: number; output_tokens?: number }>
    >
    const todayKey = new Date().toISOString().slice(0, 10)
    for (const [date, channels] of Object.entries(data)) {
      let daySum = 0
      for (const ch of Object.values(channels || {})) daySum += (ch.input_tokens || 0) + (ch.output_tokens || 0)
      total += daySum
      days++
      if (date === todayKey) today = daySum
    }
    lastReadErr = ''
  } catch (e: any) {
    lastReadErr = String(e?.message || e).slice(0, 160)
  }
  return { total, today, byDateDays: days, ...(lastReadErr ? { err: lastReadErr } : {}) }
}

export const inject = ['webServer'] as unknown as string[]

export function apply(ctx: any) {
  const webServer = ctx.webServer

  webServer.register({
    kind: 'exact',
    path: '/api/nitian/ping',
    handler: (_req: any, res: any) => json(res, 200, { ok: true, theme: 'nitian' }),
  })

  webServer.register({
    kind: 'exact',
    path: '/api/nitian/usage',
    handler: (_req: any, res: any) => json(res, 200, { ok: true, real: readRealTokens() }),
  })

  const disposerAssets = webServer.register({
    kind: 'prefix',
    path: '/nitian-assets',
    handler: (req: any, res: any) => {
      const relRaw = urlPath(req.url).replace(/^\/nitian-assets\/?/, '/')
      let target: string | undefined
      for (const [prefix, root] of ALLOWED) {
        if (relRaw === prefix) {
          target = root
          break
        }
        if (prefix.endsWith('/') && relRaw.startsWith(prefix)) {
          target = resolve(root, '.' + relRaw.slice(prefix.length - 1))
          break
        }
      }
      const safe = target ? normalize(target) : undefined
      if (!safe || !existsSync(safe) || !statSync(safe).isFile()) {
        res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' })
        res.end('not found')
        return
      }
      const ext = safe.slice(safe.lastIndexOf('.')).toLowerCase()
      res.writeHead(200, {
        'content-type': MIME[ext] || 'application/octet-stream',
        'cache-control': 'no-cache',
      })
      createReadStream(safe).pipe(res)
    },
  })

  ctx.effect(() => disposerAssets)
  console.log('[nitian-dsh-theme] routes mounted: /nitian-assets/* + /api/nitian/{ping,usage}')
}
