export interface CriterionResponse {
  id: string;
  name: string;
  description: string | null;
  weight: number;
  max_score: number;
  sort_order: number;
}

export interface StandardResponse {
  id: string;
  name: string;
  description: string | null;
  version: string;
  is_active: boolean;
  criteria: CriterionResponse[];
}
