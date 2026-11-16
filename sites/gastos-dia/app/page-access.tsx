import { requireChatGPTUser } from './chatgpt-auth';
import { resolveAccess, permits, type AccessPage } from '@/lib/access';

export async function pageAccess(path:string) {
  const user=await requireChatGPTUser(path);
  return resolveAccess(user.userId,user.email);
}
export async function canOpenPage(path:string,page:AccessPage) {
  const access=await pageAccess(path);return permits(access,page);
}
export function AccessDenied() {
  return <main className="shell"><section className="panel" style={{marginTop:60}}><h1>Acesso não autorizado</h1><p style={{marginTop:20}}>Esta página não foi liberada para sua conta. Peça ao administrador para revisar suas permissões.</p><a className="button" href="/">Voltar ao início</a></section></main>;
}
