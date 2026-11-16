import { redirect } from 'next/navigation';
import { pageAccess, AccessDenied } from './page-access';
import Dashboard from './dashboard';
export const dynamic = 'force-dynamic';
export default async function Home() {
  const access=await pageAccess('/');
  if(!access.isOwner&&!access.canSummary){
    if(access.canEntries)redirect('/lancamentos');
    if(access.canPeriods)redirect('/periodos');
    return <AccessDenied/>;
  }
  return <Dashboard />;
}
