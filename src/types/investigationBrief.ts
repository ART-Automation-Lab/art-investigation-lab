export type ResearchStatus = 'UNKNOWN' | 'UNVERIFIED' | 'PENDING' | 'ACTIVE' | 'PASSED' | 'FAILED' | 'BLOCKED' | 'SURVIVED' | 'KILLED';

export interface Provenance {
  source_file: string;
  section: string;
  line_start: number | null;
  line_end: number | null;
}

export interface InvestigationSource {
  id: string;
  title: string;
  url: string;
  source_type: string;
  used_by: string[];
}

export type IntelligenceType =
  | 'WORKFLOW_PATTERN'
  | 'STRATEGY_PATTERN'
  | 'DECISION_PATTERN'
  | 'IMPLEMENTATION_PATTERN'
  | 'ARCHITECTURE_PATTERN'
  | 'GUARDRAIL'
  | 'METRIC_PATTERN'
  | 'RESEARCH_METHOD'
  | 'DESIGN_PRINCIPLE'
  | 'NEGATIVE_INTELLIGENCE'
  | 'ART_IMPROVEMENT';

export type IntelligenceEvidenceStatus = 'VERIFIED' | 'PARTIAL' | 'HYPOTHESIS' | 'UNKNOWN' | 'REJECTED';
export type IntelligenceStatus = 'ACTIVE' | 'EXPERIMENTAL' | 'RETIRED';
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';
export type ReusePotential = 'HIGH' | 'MEDIUM' | 'LOW';
export type EpistemicClassification = 'EVIDENCE' | 'CLAIM' | 'INFERENCE' | 'HYPOTHESIS' | 'FALSIFICATION' | 'RESULT' | 'DECISION';

export interface IntelligenceObject {
  id: string;
  type: IntelligenceType;
  title: string;
  domain: string;
  description: string;
  pattern?: string;
  lesson?: string;
  art_learning?: string;
  art_improvement?: string;
  conditions?: string[];
  anti_pattern?: string;
  do_not_assume?: string[] | string;
  evidence_status: IntelligenceEvidenceStatus;
  status: IntelligenceStatus;
  confidence: ConfidenceLevel;
  reuse_potential: ReusePotential;
  applications: string[];
  source_checkpoint?: string;
  source_refs: string[];
  source_location?: string;
  original_source?: string;
  tags: string[];
  provenance: Provenance;
}

export interface InvestigationCheckpoint {
  id: string;
  title: string;
  status?: string;
  investigation_question?: string;
  tested: string;
  found: string;
  what_changed: string;
  resulting_state: string;
  evidence_refs?: string[];
  source_refs?: string[];
  provenance: Provenance;
}

export interface InvestigationBrief {
  title(arg0: string, title: any): unknown;
  investigationId(arg0: string, investigationId: any): unknown;
  overview: any;
  progression: any;
  reusableIntelligence: any;
  provenance: any;
  investigation_id: string;
  company: string;
  industry: string;
  opportunity: string;
  investigation_type: string;
  research_status: ResearchStatus;
  presentation: {
    investigation_summary: string;
    key_findings: {
      id: string;
      statement: string;
      classification: EpistemicClassification;
      source_refs: string[];
    }[];
  };
  decision: {
    decision: string;
    reason: string;
    reusable_intelligence: IntelligenceObject[];
    provenance: Provenance;
  };
  primary_question: string;
  sources: InvestigationSource[];
  checkpoints: InvestigationCheckpoint[];
  evidence: {
    id: string;
    statement: string;
    classification: string;
    source: string;
    provenance: Provenance;
  }[];
  claims: {
    id: string;
    statement: string;
    evidence_basis: string[];
    provenance: Provenance;
  }[];
  inferences: {
    id: string;
    statement: string;
    basis: string[];
    implication: string;
    provenance: Provenance;
  }[];
  hypotheses: {
    id: string;
    statement: string;
    status: ResearchStatus;
    supporting_basis: string[];
    falsification_basis: string[];
    provenance: Provenance;
  }[];
  results: {
    id: string;
    statement: string;
    status: ResearchStatus;
    provenance: Provenance;
  }[];
  falsification?: {
    statement: string;
    outcome: string;
    basis: string[];
    provenance: Provenance;
  }[];
  traceability: {
    statement: string;
    research_location: string;
    source_urls: string[];
    provenance: Provenance;
  }[];
}
