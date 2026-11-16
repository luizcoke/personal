import { redirect } from 'next/navigation';

// Preserve old bookmarks without maintaining a separate summary page.
export default function LegacySummary() {
  redirect('/');
}
