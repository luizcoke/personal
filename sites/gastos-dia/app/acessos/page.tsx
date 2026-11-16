import Dashboard from '../dashboard';
import { canOpenPage, AccessDenied } from '../page-access';
export const dynamic='force-dynamic';
export default async function AccessPage(){
  if(!await canOpenPage('/acessos','access'))return <AccessDenied/>;
  return <Dashboard initialTab="access"/>;
}
