import { validateInvestigationBrief } from './investigationBriefValidator';
import type { InvestigationBrief } from '../types/investigationBrief';

// Use Vite's import.meta.glob to synchronously load JSON files
const rawJsonFiles = import.meta.glob('./investigations/**/*.json', { query: '?raw', import: 'default', eager: true });

export function loadAllInvestigationBriefs(): InvestigationBrief[] {
  const briefs: InvestigationBrief[] = [];

  for (const [path, content] of Object.entries(rawJsonFiles)) {
    try {
      const data = JSON.parse(content as string);
      const validation = validateInvestigationBrief(data);

      if (validation.valid && validation.brief) {
        briefs.push(validation.brief);
      } else {
        console.error(`Validation failed for ${path}:`, validation.errors);
        throw new Error(`Validation failed for ${path}: AIL cannot render this Investigation Brief.`);
      }
    } catch (e) {
      console.error(`Failed to parse or validate ${path}:`, e);
      throw e;
    }
  }

  return briefs;
}
