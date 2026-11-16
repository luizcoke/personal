import Dashboard from '../dashboard';
import { canOpenPage, AccessDenied } from '../page-access';
export const dynamic='force-dynamic';
export default async function Connect(){
  if(!await canOpenPage('/conectar','setup'))return <AccessDenied/>;
  return <Dashboard initialTab="setup"/>;
}
