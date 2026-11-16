import Dashboard from '../dashboard';
import { canOpenPage, AccessDenied } from '../page-access';
export const dynamic='force-dynamic';
export default async function CardsPage(){
  if(!await canOpenPage('/cartoes','cards'))return <AccessDenied/>;
  return <Dashboard initialTab="cards"/>;
}
