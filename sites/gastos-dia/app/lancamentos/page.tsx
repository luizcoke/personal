import Dashboard from '../dashboard';
import { canOpenPage, AccessDenied } from '../page-access';
export const dynamic='force-dynamic';
export default async function Entries(){
  if(!await canOpenPage('/lancamentos','entries'))return <AccessDenied/>;
  return <Dashboard initialTab="entries"/>;
}
