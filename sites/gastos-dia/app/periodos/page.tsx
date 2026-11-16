import Dashboard from '../dashboard';
import { canOpenPage, AccessDenied } from '../page-access';
export const dynamic='force-dynamic';
export default async function PeriodsPage(){
 if(!await canOpenPage('/periodos','periods'))return <AccessDenied/>;
 return <Dashboard initialTab="periods"/>;
}
