const alphabetical = new Intl.Collator('pt-BR', { sensitivity: 'base', numeric: true });
export const compareLabels = (a: string, b: string) => alphabetical.compare(a, b);
export function compareCardNames(a: {name: string; last4: string}, b: {name: string; last4: string}) {
  return compareLabels(a.name.trim() || `Cartão final ${a.last4}`, b.name.trim() || `Cartão final ${b.last4}`) || compareLabels(a.last4, b.last4);
}
